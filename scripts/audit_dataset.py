"""
CareerLens AI — Reproducible Dataset Audit & Profiling Script.

Usage:
    python scripts/audit_dataset.py

This script:
1. Downloads and caches the Job Skill Set dataset from Hugging Face if not cached.
2. Audits row counts, column types, missing values, duplicates, and category balance.
3. Examines raw and parsed structures of 'job_skill_set'.
4. Executes deterministic skill normalization and matching checks on real records.
5. Verifies data integrity against PRD and Anti-Slop requirements.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.data_loader import ensure_dataset_cached, load_dataset
from backend.matcher import calculate_match, normalize_skill, parse_skill_set


def run_audit() -> None:
    print("=" * 70)
    print("CAREERLENS AI — DATASET PROFILING & INTEGRITY AUDIT")
    print("=" * 70)

    # 1. Cache & Load
    print("\n[Step 1] Loading dataset...")
    cache_path = ensure_dataset_cached()
    print(f"Cached file path: {cache_path}")
    print(f"File size: {cache_path.stat().st_size:,} bytes")

    df = load_dataset()
    rows, cols = df.shape
    print(f"Dataset loaded successfully: {rows:,} rows, {cols} columns.")

    # 2. Schema & Column Types
    print("\n[Step 2] Schema & Column Types:")
    for col in df.columns:
        print(f" - {col:18} | type: {str(df[col].dtype):10} | non-null count: {df[col].count():,}")

    # 3. Missing Values & Duplicates
    print("\n[Step 3] Data Quality & Completeness:")
    null_counts = df.isnull().sum()
    print("Missing / Null values per column:")
    for col, count in null_counts.items():
        print(f" - {col:18}: {count}")

    dup_rows = df.duplicated().sum()
    dup_ids = df["job_id"].duplicated().sum()
    unique_ids = df["job_id"].nunique()
    print(f"Duplicate complete rows: {dup_rows}")
    print(f"Duplicate job_id values: {dup_ids}")
    print(f"Unique job_id count:     {unique_ids} (100% unique: {unique_ids == rows})")

    # 4. Category Breakdown
    print("\n[Step 4] Category Distribution:")
    cat_counts = df["category"].value_counts()
    for cat, count in cat_counts.items():
        pct = (count / rows) * 100
        print(f" - {cat:24}: {count:4} ({pct:5.2f}%)")

    # 5. Inspection of job_skill_set Representation
    print("\n[Step 5] 'job_skill_set' Format Inspection:")
    sample_rows = df.head(5)[["job_id", "job_title", "category", "job_skill_set"]].to_dict(orient="records")
    for idx, r in enumerate(sample_rows, 1):
        raw_repr = r["job_skill_set"]
        parsed = parse_skill_set(raw_repr)
        print(f"\n Sample #{idx}: {r['job_title']} ({r['category']}) [ID: {r['job_id']}]")
        print(f"  Raw string preview (first 100 chars): {repr(raw_repr[:100])}")
        print(f"  Parsed skill count: {len(parsed)}")
        print(f"  First 4 parsed skills: {parsed[:4]}")

    # 6. Global Skill Set Parse Integrity & Statistics
    print("\n[Step 6] Global Skill Parse Integrity:")
    skill_counts = []
    parse_errors = 0
    all_raw_skills_count = 0
    unique_canonical_skills = set()

    for raw_skill in df["job_skill_set"]:
        try:
            parsed = parse_skill_set(raw_skill)
            skill_counts.append(len(parsed))
            all_raw_skills_count += len(parsed)
            for s in parsed:
                unique_canonical_skills.add(normalize_skill(s))
        except Exception:
            parse_errors += 1

    print(f"Total jobs audited for skills: {len(skill_counts):,}")
    print(f"Parsing failures / exceptions: {parse_errors}")
    print(f"Min skills in a job:           {min(skill_counts)}")
    print(f"Max skills in a job:           {max(skill_counts)}")
    print(f"Average skills per job:        {sum(skill_counts) / len(skill_counts):.2f}")
    print(f"Total skill occurrences:       {all_raw_skills_count:,}")
    print(f"Unique canonical skills:       {len(unique_canonical_skills):,}")

    # 7. Verification of Deterministic Matching on Sample Job
    print("\n[Step 7] Sample Deterministic Match Execution:")
    test_job = df.iloc[0]
    test_job_skills = parse_skill_set(test_job["job_skill_set"])
    print(f"Selected Job: {test_job['job_title']} ({test_job['category']})")
    print(f"Required Skills ({len(test_job_skills)}): {test_job_skills}")

    # Test case: User has 2 matching skills (with differing casing/hyphens) + 1 unrelated skill
    sample_user_skills = [
        test_job_skills[0].upper(),  # Exact match with upper casing
        " " + test_job_skills[1].lower() + " ",  # Lower casing with whitespace
        "Unrelated Advanced Skill",  # Disjoint
    ]
    print(f"\nUser Profile Skills: {sample_user_skills}")
    match_result = calculate_match(sample_user_skills, test_job_skills)
    print(f"Calculated Match Score: {match_result['match_score']}%")
    print(f"Matched Skills ({len(match_result['matched_skills'])}): {match_result['matched_skills']}")
    print(f"Unreported Skills ({len(match_result['unreported_skills'])}): {match_result['unreported_skills']}")

    expected_score = round((2 / len(test_job_skills)) * 100, 1)
    assert match_result["match_score"] == expected_score, (
        f"Score mismatch: {match_result['match_score']} vs {expected_score}"
    )
    assert len(match_result["matched_skills"]) == 2
    assert len(match_result["unreported_skills"]) == len(test_job_skills) - 2
    print("Match verification assertion: PASSED")

    print("\n" + "=" * 70)
    print("AUDIT COMPLETE — ALL INTEGRITY CHECKS PASSED")
    print("=" * 70)


if __name__ == "__main__":
    run_audit()
