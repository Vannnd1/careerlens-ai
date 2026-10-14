"""
CareerLens AI — Dataset Loader & Cache Manager.

Safely downloads and caches the Job Skill Set benchmark dataset from Hugging Face:
https://huggingface.co/datasets/batuhanmtl/job-skill-set

Validates schema, checks completeness, pre-parses skills for high performance,
and provides filtering and search utilities.
"""

from __future__ import annotations

import os
from pathlib import Path
import urllib.request
from typing import Any

import pandas as pd

from backend.matcher import parse_skill_set

DATASET_REMOTE_URL = (
    "https://huggingface.co/datasets/batuhanmtl/job-skill-set/resolve/main/data/train-00000-of-00001.parquet"
)
DEFAULT_CACHE_DIR = Path(__file__).resolve().parent.parent / ".cache" / "dataset"
PARQUET_FILENAME = "train-00000-of-00001.parquet"

EXPECTED_COLUMNS = [
    "job_id",
    "category",
    "job_title",
    "job_description",
    "job_skill_set",
]


def ensure_dataset_cached(
    cache_dir: Path | None = None,
    remote_url: str = DATASET_REMOTE_URL,
) -> Path:
    """Ensure the benchmark dataset parquet file is downloaded into the local cache.

    Returns the absolute path to the cached parquet file.
    """
    target_dir = Path(cache_dir) if cache_dir else DEFAULT_CACHE_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    target_file = target_dir / PARQUET_FILENAME

    if not target_file.exists() or target_file.stat().st_size == 0:
        req = urllib.request.Request(
            remote_url,
            headers={"User-Agent": "CareerLens-AI-DataLoader/1.0"},
        )
        with urllib.request.urlopen(req) as response:
            data = response.read()
            with open(target_file, "wb") as f:
                f.write(data)

    return target_file


def load_dataset(cache_dir: Path | None = None) -> pd.DataFrame:
    """Load the Job Skill Set dataset as a Pandas DataFrame.

    Validates that:
    - The file exists and is valid Parquet.
    - All expected columns are present.
    - Types are coerced safely.
    - Pre-parses job_skill_set for high-speed in-memory matching.
    """
    file_path = ensure_dataset_cached(cache_dir)
    df = pd.read_parquet(file_path)

    missing_cols = [col for col in EXPECTED_COLUMNS if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Dataset is missing required columns: {missing_cols}")

    # Ensure consistent types
    df["job_id"] = df["job_id"].astype("int64")
    for col in ["category", "job_title", "job_description", "job_skill_set"]:
        df[col] = df[col].fillna("").astype(str)

    # Pre-parse skills once for ultra-fast matching
    df["parsed_skills"] = df["job_skill_set"].apply(parse_skill_set)

    return df


def get_categories_summary(df: pd.DataFrame) -> list[dict[str, Any]]:
    """Return category summary with job counts."""
    counts = df["category"].value_counts().to_dict()
    categories = []
    for cat_name, count in sorted(counts.items(), key=lambda x: (-x[1], x[0])):
        categories.append(
            {
                "id": cat_name,
                "label": cat_name.replace("-", " ").title(),
                "count": int(count),
            }
        )
    return categories


def get_job_by_id(df: pd.DataFrame, job_id: int) -> dict[str, Any] | None:
    """Retrieve a single job record by ID."""
    match = df[df["job_id"] == job_id]
    if match.empty:
        return None
    row = match.iloc[0].to_dict()
    if "parsed_skills" not in row or not isinstance(row["parsed_skills"], list):
        row["parsed_skills"] = parse_skill_set(row.get("job_skill_set"))
    return row


def search_jobs(
    df: pd.DataFrame,
    query: str | None = None,
    category: str | None = None,
    page: int = 1,
    page_size: int = 20,
) -> tuple[int, list[dict[str, Any]]]:
    """Search and paginate job records with text and category filtering."""
    filtered = df

    if category:
        cat_clean = category.strip().upper()
        filtered = filtered[filtered["category"].str.upper() == cat_clean]

    if query:
        q = query.strip().lower()
        title_mask = filtered["job_title"].str.lower().str.contains(q, regex=False)
        desc_mask = filtered["job_description"].str.lower().str.contains(q, regex=False)
        filtered = filtered[title_mask | desc_mask]

    total = len(filtered)
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    page_df = filtered.iloc[start_idx:end_idx]

    records = []
    for _, row in page_df.iterrows():
        skills = row["parsed_skills"] if "parsed_skills" in row else parse_skill_set(row["job_skill_set"])
        desc = row["job_description"]
        snippet = (desc[:160] + "...") if len(desc) > 160 else desc
        records.append(
            {
                "job_id": int(row["job_id"]),
                "category": str(row["category"]),
                "job_title": str(row["job_title"]),
                "description_snippet": snippet,
                "skills_count": len(skills),
                "skills": skills,
            }
        )

    return total, records
