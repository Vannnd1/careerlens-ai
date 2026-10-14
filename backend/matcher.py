"""
CareerLens AI — Deterministic Skill Matcher & Normalizer.

This module provides deterministic skill normalization and matching calculations
for CareerLens AI, in strict accordance with PRD.md Section 7 and 9.
No ML or LLM guessing: strictly set-based overlap calculations.
"""

from __future__ import annotations

import ast
import json
import re
from typing import Any, Iterable, List, Sequence, Tuple


def normalize_skill(skill: str) -> str:
    """Normalize a skill token for deterministic matching.

    - Strips leading and trailing whitespace and quotes.
    - Converts to lowercase.
    - Normalizes internal hyphens, underscores, and multiple spaces to a single space.
    - Preserves technology-specific characters like '.', '+', '#' (e.g., 'c++', 'c#', 'node.js', '.net').

    Examples:
        >>> normalize_skill(" Problem-Solving ")
        'problem solving'
        >>> normalize_skill("Node.js")
        'node.js'
        >>> normalize_skill("C++")
        'c++'
    """
    if not skill or not isinstance(skill, str):
        return ""
    cleaned = skill.strip().strip("'\"").strip()
    if not cleaned:
        return ""
    # Lowercase and collapse hyphens/underscores/consecutive whitespace into a single space
    lowered = cleaned.lower()
    return re.sub(r"[\s\-_]+", " ", lowered).strip()


def parse_skill_set(raw: Any) -> list[str]:
    """Safely parse a job's or user's skill set from various representations into a list of strings.

    Supports:
    - Native Python list/tuple/set of strings.
    - Stringified Python lists (e.g. "['Python', 'SQL']").
    - JSON array strings (e.g. '["Python", "SQL"]').
    - Delimited text strings (e.g. "Python, SQL; Git").
    - Missing/NaN/None values (returns empty list).

    Preserves original casing and order of unique skills.
    """
    if raw is None:
        return []

    # If already a collection of items
    if isinstance(raw, (list, tuple, set)):
        items = raw
    elif isinstance(raw, str):
        text = raw.strip()
        if not text:
            return []
        parsed = None
        # Try Python literal eval (primary dataset format: "['skill1', 'skill2']")
        if (text.startswith("[") and text.endswith("]")) or (text.startswith("(") and text.endswith(")")):
            try:
                evaluated = ast.literal_eval(text)
                if isinstance(evaluated, (list, tuple, set)):
                    parsed = evaluated
            except (ValueError, SyntaxError):
                pass

            # If literal_eval fails, try JSON parser
            if parsed is None:
                try:
                    evaluated = json.loads(text)
                    if isinstance(evaluated, (list, tuple, set)):
                        parsed = evaluated
                except (json.JSONDecodeError, ValueError):
                    pass

        if parsed is not None:
            items = parsed
        else:
            # Fallback for comma- or semicolon-delimited plain text
            items = re.split(r"[,;]+", text)
    else:
        # Non-string scalar or unexpected type
        return []

    # Deduplicate while preserving first-seen display string and filtering empty tokens
    seen_canonical = set()
    cleaned_skills: list[str] = []
    for item in items:
        if not isinstance(item, str):
            item = str(item)
        token = item.strip().strip("'\"").strip()
        if not token:
            continue
        canonical = normalize_skill(token)
        if canonical and canonical not in seen_canonical:
            seen_canonical.add(canonical)
            cleaned_skills.append(token)

    return cleaned_skills


def calculate_match(
    user_skills: Sequence[str] | Any,
    job_skills: Sequence[str] | Any,
) -> dict[str, Any]:
    """Calculate deterministic skill overlap between user profile and a job role.

    Formula (PRD Section 7 & 9):
        match_score = (len(matched_skills) / len(job_required_skills)) * 100

    Guarantees:
    - Returns 0.0 if job has 0 required skills (no ZeroDivisionError).
    - Returns 0.0 if user has 0 skills or disjoint skills.
    - Score is capped at 100.0 and rounded to 1 decimal place.
    - Duplicate skills in user input are deduplicated and cannot inflate score.
    - Preserves job's original display labels for matched and unreported skills.

    Returns:
        {
            "match_score": float,
            "matched_skills": list[str],
            "unreported_skills": list[str],
            "total_job_skills": int,
            "total_user_skills": int,
        }
    """
    clean_user = parse_skill_set(user_skills)
    clean_job = parse_skill_set(job_skills)

    # Build canonical token mapping for user skills
    user_canonical_set = {normalize_skill(s) for s in clean_user if normalize_skill(s)}

    # Categorize job skills based on canonical token match, keeping original job labels
    matched_display: list[str] = []
    unreported_display: list[str] = []

    for job_skill in clean_job:
        canonical = normalize_skill(job_skill)
        if canonical in user_canonical_set:
            matched_display.append(job_skill)
        else:
            unreported_display.append(job_skill)

    total_job_skills = len(clean_job)
    total_user_skills = len(clean_user)

    if total_job_skills == 0:
        match_score = 0.0
    else:
        raw_score = (len(matched_display) / total_job_skills) * 100.0
        match_score = round(min(100.0, max(0.0, raw_score)), 1)

    return {
        "match_score": match_score,
        "matched_skills": matched_display,
        "unreported_skills": unreported_display,
        "total_job_skills": total_job_skills,
        "total_user_skills": total_user_skills,
    }


def match_profile_against_jobs(
    user_skills: Sequence[str] | Any,
    jobs: Sequence[dict[str, Any]],
    category_filter: str | None = None,
    limit: int | None = None,
) -> list[dict[str, Any]]:
    """Rank a list of job records against user profile skills.

    Args:
        user_skills: List of skills reported by the user.
        jobs: List of job dictionaries, each containing at minimum 'job_id', 'job_title',
              'category', and 'job_skill_set'.
        category_filter: Optional category string to filter jobs (e.g. 'INFORMATION-TECHNOLOGY').
        limit: Optional maximum number of matches to return.

    Returns:
        Ranked list of match result dictionaries sorted descending by match_score,
        then descending by total matched skills.
    """
    results: list[dict[str, Any]] = []

    for job in jobs:
        # Apply category filter if specified
        if category_filter:
            job_cat = str(job.get("category", "")).strip().upper()
            if job_cat != category_filter.strip().upper():
                continue

        raw_skills = job.get("parsed_skills", job.get("job_skill_set"))
        match_res = calculate_match(user_skills, raw_skills)
        result_item = {
            "job_id": job.get("job_id"),
            "job_title": job.get("job_title", ""),
            "category": job.get("category", ""),
            "match_score": match_res["match_score"],
            "matched_skills": match_res["matched_skills"],
            "unreported_skills": match_res["unreported_skills"],
            "total_required_skills": match_res["total_job_skills"],
        }
        results.append(result_item)

    # Sort descending by match_score, then secondary sort by count of matched skills
    results.sort(
        key=lambda r: (r["match_score"], len(r["matched_skills"])),
        reverse=True,
    )

    if limit is not None and limit > 0:
        return results[:limit]

    return results
