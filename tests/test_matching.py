"""
Unit and integration tests for CareerLens AI deterministic skill matcher.

Validates normal cases, edge cases, deduplication, case/whitespace normalization,
and division-by-zero protection.
"""

from __future__ import annotations

import sys
from pathlib import Path
import pytest

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.matcher import (
    calculate_match,
    match_profile_against_jobs,
    normalize_skill,
    parse_skill_set,
)
from backend.data_loader import load_dataset


class TestSkillNormalization:
    """Tests for normalize_skill function."""

    def test_basic_lowercase_and_strip(self):
        assert normalize_skill("  Python  ") == "python"
        assert normalize_skill("Machine Learning") == "machine learning"

    def test_hyphen_and_underscore_normalization(self):
        assert normalize_skill("Problem-Solving") == "problem solving"
        assert normalize_skill("problem_solving") == "problem solving"
        assert normalize_skill("front-end development") == "front end development"

    def test_tech_symbols_preserved(self):
        assert normalize_skill("C++") == "c++"
        assert normalize_skill("C#") == "c#"
        assert normalize_skill("Node.js") == "node.js"
        assert normalize_skill(".NET Core") == ".net core"

    def test_quotes_and_empty_inputs(self):
        assert normalize_skill("'Python'") == "python"
        assert normalize_skill('"SQL"') == "sql"
        assert normalize_skill("") == ""
        assert normalize_skill("   ") == ""
        assert normalize_skill(None) == ""


class TestSkillSetParsing:
    """Tests for parse_skill_set function."""

    def test_parse_python_stringified_list(self):
        raw = "['Python', 'SQL', 'Data Analysis']"
        parsed = parse_skill_set(raw)
        assert parsed == ["Python", "SQL", "Data Analysis"]

    def test_parse_json_array_string(self):
        raw = '["FastAPI", "React", "TypeScript"]'
        parsed = parse_skill_set(raw)
        assert parsed == ["FastAPI", "React", "TypeScript"]

    def test_parse_comma_delimited_string(self):
        raw = "Communication, Leadership; Teamwork, Public Speaking"
        parsed = parse_skill_set(raw)
        assert parsed == ["Communication", "Leadership", "Teamwork", "Public Speaking"]

    def test_parse_native_list(self):
        raw = ["Python", "Docker", "Kubernetes"]
        parsed = parse_skill_set(raw)
        assert parsed == ["Python", "Docker", "Kubernetes"]

    def test_parse_deduplicates_repeated_tokens(self):
        raw = "['Python', 'python', '  PYTHON  ', 'SQL']"
        parsed = parse_skill_set(raw)
        # Deduplicated to unique canonical tokens, keeping first seen display
        assert parsed == ["Python", "SQL"]

    def test_parse_none_and_empty(self):
        assert parse_skill_set(None) == []
        assert parse_skill_set("") == []
        assert parse_skill_set("   ") == []
        assert parse_skill_set("[]") == []

    def test_parse_malformed_syntax_fallback(self):
        # Unclosed bracket should fall back gracefully rather than crashing
        raw = "['Python', 'SQL'"
        parsed = parse_skill_set(raw)
        assert "Python" in parsed or "SQL" in parsed or len(parsed) > 0


class TestCalculateMatch:
    """Tests for calculate_match scoring logic and boundaries."""

    def test_normal_partial_match(self):
        job_skills = ["Python", "SQL", "Tableau", "Statistics"]
        user_skills = ["Python", "SQL", "Git"]
        res = calculate_match(user_skills, job_skills)

        assert res["match_score"] == 50.0
        assert res["matched_skills"] == ["Python", "SQL"]
        assert res["unreported_skills"] == ["Tableau", "Statistics"]
        assert res["total_job_skills"] == 4
        assert res["total_user_skills"] == 3

    def test_perfect_100_percent_match(self):
        job_skills = ["Python", "SQL"]
        user_skills = ["SQL", "Python", "Docker"]
        res = calculate_match(user_skills, job_skills)

        assert res["match_score"] == 100.0
        assert res["matched_skills"] == ["Python", "SQL"]
        assert res["unreported_skills"] == []

    def test_zero_percent_disjoint_match(self):
        job_skills = ["Accounting", "Financial Modeling"]
        user_skills = ["Python", "Machine Learning"]
        res = calculate_match(user_skills, job_skills)

        assert res["match_score"] == 0.0
        assert res["matched_skills"] == []
        assert res["unreported_skills"] == ["Accounting", "Financial Modeling"]

    def test_empty_user_skills_safe(self):
        job_skills = ["Python", "SQL"]
        res = calculate_match([], job_skills)

        assert res["match_score"] == 0.0
        assert res["matched_skills"] == []
        assert res["unreported_skills"] == ["Python", "SQL"]

    def test_empty_job_skills_prevents_zero_division(self):
        # Must return 0.0 and never raise ZeroDivisionError
        res = calculate_match(["Python"], [])
        assert res["match_score"] == 0.0
        assert res["matched_skills"] == []
        assert res["unreported_skills"] == []
        assert res["total_job_skills"] == 0

    def test_user_duplicates_do_not_inflate_score(self):
        job_skills = ["Python", "SQL", "Docker", "Kubernetes"]
        # User entered python 3 times with different casing/spaces
        user_skills = ["Python", "python", "  PYTHON  "]
        res = calculate_match(user_skills, job_skills)

        # 1 match out of 4 = 25.0%
        assert res["match_score"] == 25.0
        assert res["matched_skills"] == ["Python"]
        assert len(res["matched_skills"]) == 1

    def test_case_and_whitespace_insensitivity(self):
        job_skills = ["Machine Learning", "Problem-Solving"]
        user_skills = ["  machine learning  ", "Problem Solving"]
        res = calculate_match(user_skills, job_skills)

        assert res["match_score"] == 100.0
        assert res["matched_skills"] == ["Machine Learning", "Problem-Solving"]

    def test_preserves_original_job_casing(self):
        job_skills = ["Human Resources Management", "Talent Acquisition"]
        user_skills = ["human resources management", "talent acquisition"]
        res = calculate_match(user_skills, job_skills)

        # Display strings must come from the official job record
        assert res["matched_skills"] == ["Human Resources Management", "Talent Acquisition"]


class TestMatchProfileAgainstJobs:
    """Tests for multi-job ranking and filtering."""

    @pytest.fixture
    def mock_jobs(self):
        return [
            {
                "job_id": 1,
                "job_title": "Data Scientist",
                "category": "INFORMATION-TECHNOLOGY",
                "job_skill_set": ["Python", "SQL", "Pandas", "Scikit-Learn"],
            },
            {
                "job_id": 2,
                "job_title": "Financial Analyst",
                "category": "FINANCE",
                "job_skill_set": ["Excel", "Financial Modeling", "Accounting"],
            },
            {
                "job_id": 3,
                "job_title": "Data Engineer",
                "category": "INFORMATION-TECHNOLOGY",
                "job_skill_set": ["Python", "SQL", "Docker", "Airflow", "Kafka"],
            },
        ]

    def test_ranking_sort_order(self, mock_jobs):
        user_skills = ["Python", "SQL", "Pandas"]
        results = match_profile_against_jobs(user_skills, mock_jobs)

        # Data Scientist: 3 / 4 = 75.0%
        # Data Engineer: 2 / 5 = 40.0%
        # Financial Analyst: 0 / 3 = 0.0%
        assert results[0]["job_title"] == "Data Scientist"
        assert results[0]["match_score"] == 75.0
        assert results[1]["job_title"] == "Data Engineer"
        assert results[1]["match_score"] == 40.0
        assert results[2]["job_title"] == "Financial Analyst"
        assert results[2]["match_score"] == 0.0

    def test_category_filtering(self, mock_jobs):
        user_skills = ["Python", "SQL"]
        results = match_profile_against_jobs(
            user_skills,
            mock_jobs,
            category_filter="FINANCE",
        )
        assert len(results) == 1
        assert results[0]["job_title"] == "Financial Analyst"

    def test_limit_parameter(self, mock_jobs):
        user_skills = ["Python", "SQL"]
        results = match_profile_against_jobs(user_skills, mock_jobs, limit=1)
        assert len(results) == 1


class TestRealDatasetIntegration:
    """Integration test with the live cached dataset."""

    def test_match_against_live_dataset(self):
        df = load_dataset()
        assert len(df) == 1167

        # Test profile with common skills across IT
        sample_skills = ["Python", "SQL", "Git"]
        jobs_sample = df.to_dict(orient="records")
        results = match_profile_against_jobs(sample_skills, jobs_sample, limit=5)

        assert len(results) == 5
        for r in results:
            assert 0.0 <= r["match_score"] <= 100.0
            assert isinstance(r["matched_skills"], list)
            assert isinstance(r["unreported_skills"], list)
            assert r["total_required_skills"] == len(r["matched_skills"]) + len(r["unreported_skills"])

    def test_categories_summary(self):
        from backend.data_loader import get_categories_summary
        df = load_dataset()
        summary = get_categories_summary(df)
        assert len(summary) == 5
        total_count = sum(c["count"] for c in summary)
        assert total_count == 1167
        category_ids = {c["id"] for c in summary}
        assert "INFORMATION-TECHNOLOGY" in category_ids
        assert "HR" in category_ids

    def test_missing_required_columns_error(self, tmp_path):
        import pandas as pd
        from backend.data_loader import load_dataset

        bad_df = pd.DataFrame({"job_id": [1], "category": ["IT"]})
        bad_parquet = tmp_path / "train-00000-of-00001.parquet"
        bad_df.to_parquet(bad_parquet)

        with pytest.raises(ValueError, match="missing required columns"):
            load_dataset(cache_dir=tmp_path)

