"""
Integration and behavior tests for CareerLens AI FastAPI backend.

Tests all endpoints via live HTTP requests (using uvicorn in a background thread and requests):
- /api/health
- /api/categories
- /api/jobs (search, filter, pagination)
- /api/jobs/{job_id} (detail and 404)
- /api/match (deterministic scoring, gap evidence, validation)
- Error safety and input boundary enforcement.
"""

from __future__ import annotations

import socket
import sys
import threading
import time
from pathlib import Path

import pytest
import requests
import uvicorn

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.main import app, DATASET_STATE



class TestHealthEndpoint:
    """Tests for /api/health."""

    def test_health_check_returns_healthy(self, api_server_url):
        resp = requests.get(f"{api_server_url}/api/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "healthy"
        assert data["dataset_loaded"] is True
        assert data["total_jobs"] == 1167
        assert isinstance(data["gemini_configured"], bool)


class TestCategoriesEndpoint:
    """Tests for /api/categories."""

    def test_categories_list(self, api_server_url):
        resp = requests.get(f"{api_server_url}/api/categories")
        assert resp.status_code == 200
        data = resp.json()
        assert "categories" in data
        categories = data["categories"]
        assert len(categories) == 5

        cat_ids = {c["id"] for c in categories}
        assert cat_ids == {
            "INFORMATION-TECHNOLOGY",
            "BUSINESS-DEVELOPMENT",
            "FINANCE",
            "SALES",
            "HR",
        }
        total_count = sum(c["count"] for c in categories)
        assert total_count == 1167


class TestJobsCatalogEndpoints:
    """Tests for /api/jobs and /api/jobs/{job_id}."""

    def test_jobs_list_pagination(self, api_server_url):
        resp = requests.get(f"{api_server_url}/api/jobs?page=1&page_size=10")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 1167
        assert data["page"] == 1
        assert data["page_size"] == 10
        assert len(data["jobs"]) == 10

        first_job = data["jobs"][0]
        assert "job_id" in first_job
        assert "job_title" in first_job
        assert "category" in first_job
        assert "description_snippet" in first_job
        assert "skills" in first_job
        assert isinstance(first_job["skills"], list)

    def test_jobs_category_filter(self, api_server_url):
        resp = requests.get(f"{api_server_url}/api/jobs?category=FINANCE&page_size=50")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 236  # Exactly 236 Finance jobs
        for job in data["jobs"]:
            assert job["category"] == "FINANCE"

    def test_jobs_keyword_search(self, api_server_url):
        resp = requests.get(f"{api_server_url}/api/jobs?query=analyst")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] > 0
        # All returned jobs should contain 'analyst' in title or full description
        for job in data["jobs"][:10]:
            if "analyst" in job["job_title"].lower() or "analyst" in job["description_snippet"].lower():
                assert True
            else:
                detail = requests.get(f"{api_server_url}/api/jobs/{job['job_id']}").json()
                assert "analyst" in detail["job_description"].lower()

    def test_get_valid_job_detail(self, api_server_url):
        # Retrieve the first job from catalog
        list_resp = requests.get(f"{api_server_url}/api/jobs?page_size=1")
        target_id = list_resp.json()["jobs"][0]["job_id"]

        detail_resp = requests.get(f"{api_server_url}/api/jobs/{target_id}")
        assert detail_resp.status_code == 200
        detail = detail_resp.json()
        assert detail["job_id"] == target_id
        assert len(detail["job_description"]) > 0
        assert isinstance(detail["job_skill_set"], list)
        assert len(detail["job_skill_set"]) > 0

    def test_get_nonexistent_job_returns_404(self, api_server_url):
        resp = requests.get(f"{api_server_url}/api/jobs/9999999999")
        assert resp.status_code == 404
        assert resp.json()["detail"] == "Job record not found"


class TestMatchEndpoint:
    """Tests for POST /api/match."""

    def test_match_profile_successful(self, api_server_url):
        payload = {
            "skills": [
                {"name": "Python", "proficiency": "Intermediate"},
                {"name": "SQL", "proficiency": "Advanced"},
                {"name": "Analytical Skills", "proficiency": "Intermediate"},
            ],
            "category_filter": "INFORMATION-TECHNOLOGY",
            "interests": "Data analysis and software engineering",
            "experience_summary": "1 year internship experience",
            "limit": 5,
        }
        resp = requests.post(f"{api_server_url}/api/match", json=payload)
        assert resp.status_code == 200
        data = resp.json()

        assert data["total_evaluated"] == 240  # Exactly 240 IT jobs
        assert len(data["matches"]) == 5

        # Check ranking order (descending match_score)
        scores = [m["match_score"] for m in data["matches"]]
        assert scores == sorted(scores, reverse=True)

        # Check match evidence structure
        top_match = data["matches"][0]
        assert "job_id" in top_match
        assert "job_title" in top_match
        assert top_match["category"] == "INFORMATION-TECHNOLOGY"
        assert 0.0 <= top_match["match_score"] <= 100.0
        assert isinstance(top_match["matched_skills"], list)
        assert isinstance(top_match["unreported_skills"], list)
        assert (
            top_match["total_required_skills"]
            == len(top_match["matched_skills"]) + len(top_match["unreported_skills"])
        )

    def test_match_profile_accepts_plain_string_skills(self, api_server_url):
        payload = {
            "skills": ["Python", "Docker", "Git"],
            "limit": 3,
        }
        resp = requests.post(f"{api_server_url}/api/match", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["total_evaluated"] == 1167
        assert len(data["matches"]) == 3

    def test_match_profile_rejects_empty_skills(self, api_server_url):
        payload = {"skills": []}
        resp = requests.post(f"{api_server_url}/api/match", json=payload)
        assert resp.status_code == 422
        # Verify no filesystem paths in error
        detail = resp.json().get("detail", "")
        assert "C:\\" not in detail
        assert "Users" not in detail

    def test_match_profile_rejects_too_many_skills(self, api_server_url):
        # Max is 30 skills
        excessive_skills = [f"Skill {i}" for i in range(35)]
        payload = {"skills": excessive_skills}
        resp = requests.post(f"{api_server_url}/api/match", json=payload)
        assert resp.status_code == 422

    def test_match_profile_rejects_overly_long_skill_name(self, api_server_url):
        payload = {"skills": ["A" * 60]}  # Max is 50 chars
        resp = requests.post(f"{api_server_url}/api/match", json=payload)
        assert resp.status_code == 422

    def test_match_profile_rejects_invalid_category(self, api_server_url):
        payload = {
            "skills": ["Python"],
            "category_filter": "NON-EXISTENT-CATEGORY",
        }
        resp = requests.post(f"{api_server_url}/api/match", json=payload)
        assert resp.status_code == 400
        assert "Invalid category filter" in resp.json()["detail"]


class TestErrorSecurityAndGracefulDegradation:
    """Tests verifying safety boundaries and error masking."""

    def test_no_stack_traces_on_invalid_endpoint(self, api_server_url):
        resp = requests.get(f"{api_server_url}/api/non_existent_route")
        assert resp.status_code == 404
        content = resp.text
        assert "Traceback" not in content
        assert "File \"" not in content

    def test_unreported_skills_terminology(self, api_server_url):
        """Verifies that missing skills are explicitly labeled as 'unreported_skills'."""
        payload = {"skills": ["Python"], "limit": 1}
        resp = requests.post(f"{api_server_url}/api/match", json=payload)
        assert resp.status_code == 200
        match = resp.json()["matches"][0]
        # Must be named 'unreported_skills'
        assert "unreported_skills" in match
        assert "missing_skills" not in match
        assert "deficient_skills" not in match
