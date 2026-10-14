"""
CareerLens AI — Minimal Complete FastAPI Backend.

Implements deterministic career matching, dataset catalog exploration, and health checks.
Grounded in PRD.md specifications: zero database, in-memory dataset, transparent set math.
"""

from __future__ import annotations

import logging
import os
from contextlib import asynccontextmanager
from typing import Annotated, Any, List, Optional, Union

import pandas as pd
from fastapi import FastAPI, HTTPException, Query, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from backend.data_loader import (
    get_categories_summary,
    get_job_by_id,
    load_dataset,
    search_jobs,
)
from backend.matcher import calculate_match, match_profile_against_jobs, parse_skill_set
from backend.ai_assistant import generate_career_chat_answer, generate_learning_roadmap

# Configure logging without leaking system paths
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("careerlens")

# In-memory global state
DATASET_STATE: dict[str, Any] = {
    "df": None,
    "jobs_cache": None,
    "loaded": False,
    "categories": [],
}


def get_dataset() -> pd.DataFrame:
    """Retrieve the in-memory dataset or raise 503 if unavailable."""
    df = DATASET_STATE.get("df")
    if df is None or not DATASET_STATE.get("loaded"):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Job dataset is currently unavailable. Please verify dataset cache.",
        )
    return df


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load and validate dataset at application startup."""
    try:
        logger.info("Initializing CareerLens AI backend dataset...")
        df = load_dataset()
        DATASET_STATE["df"] = df
        DATASET_STATE["jobs_cache"] = df.to_dict(orient="records")
        DATASET_STATE["categories"] = get_categories_summary(df)
        DATASET_STATE["loaded"] = True
        logger.info("Dataset successfully loaded with %d records.", len(df))
    except Exception as exc:
        DATASET_STATE["loaded"] = False
        logger.error("Failed to load dataset at startup: %s", str(exc))
    yield
    # Cleanup if needed
    DATASET_STATE.clear()


app = FastAPI(
    title="CareerLens AI API",
    version="1.0.0",
    description="Deterministic career-exploration matching API for students and early-career seekers.",
    lifespan=lifespan,
)

# CORS Middleware (supports local development frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global Exception Handlers (Security & Anti-Slop: No internal traces exposed)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Extract clean field errors without internal code context
    errors = []
    for err in exc.errors():
        field = " -> ".join(str(loc) for loc in err.get("loc", []))
        errors.append(f"{field}: {err.get('msg', 'Invalid value')}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Validation error: " + "; ".join(errors)},
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled exception processing request: %s", str(exc), exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal server error occurred. Please try again later."},
    )


# ---------------------------------------------------------------------------
# Request & Response Models (Strictly PRD-Compliant)
# ---------------------------------------------------------------------------

class HealthResponse(BaseModel):
    status: str
    dataset_loaded: bool
    total_jobs: int
    gemini_configured: bool


class CategoryItem(BaseModel):
    id: str
    label: str
    count: int


class CategoriesResponse(BaseModel):
    categories: list[CategoryItem]


class JobSummaryItem(BaseModel):
    job_id: int
    category: str
    job_title: str
    description_snippet: str
    skills_count: int
    skills: list[str]


class JobListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    jobs: list[JobSummaryItem]


class JobDetailResponse(BaseModel):
    job_id: int
    category: str
    job_title: str
    job_description: str
    job_skill_set: list[str]


class SkillInputItem(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    proficiency: Optional[str] = Field(None, max_length=50)


SkillStr = Field(..., min_length=1, max_length=50)


class MatchProfileRequest(BaseModel):
    skills: list[Union[SkillInputItem, Annotated[str, Field(min_length=1, max_length=50)]]] = Field(
        ..., min_length=1, max_length=30
    )
    category_filter: Optional[str] = Field(None, max_length=50)
    interests: Optional[str] = Field(None, max_length=500)
    experience_summary: Optional[str] = Field(None, max_length=500)
    limit: Optional[int] = Field(20, ge=1, le=100)



class MatchResultItem(BaseModel):
    job_id: int
    job_title: str
    category: str
    match_score: float
    matched_skills: list[str]
    unreported_skills: list[str]
    total_required_skills: int


class MatchProfileResponse(BaseModel):
    total_evaluated: int
    matches: list[MatchResultItem]


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/api/health", response_model=HealthResponse)
def get_health():
    """Service health and dataset status check."""
    loaded = DATASET_STATE.get("loaded", False)
    total_jobs = len(DATASET_STATE["df"]) if loaded and DATASET_STATE.get("df") is not None else 0
    gemini_key = bool(os.getenv("GEMINI_API_KEY"))

    return {
        "status": "healthy" if loaded else "degraded",
        "dataset_loaded": loaded,
        "total_jobs": total_jobs,
        "gemini_configured": gemini_key,
    }


@app.get("/api/categories", response_model=CategoriesResponse)
def get_categories():
    """List available job categories and record counts."""
    get_dataset()  # Ensure dataset is loaded
    return {"categories": DATASET_STATE.get("categories", [])}


@app.get("/api/jobs", response_model=JobListResponse)
def get_jobs(
    query: Optional[str] = Query(None, max_length=100, description="Keyword search in title and description"),
    category: Optional[str] = Query(None, max_length=50, description="Filter by category"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Records per page"),
):
    """Search, filter, and paginate catalog job records."""
    df = get_dataset()
    total, records = search_jobs(df, query=query, category=category, page=page, page_size=page_size)
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "jobs": records,
    }


@app.get("/api/jobs/{job_id}", response_model=JobDetailResponse)
def get_job_detail(job_id: int):
    """Retrieve full record and raw description for a specific job."""
    df = get_dataset()
    record = get_job_by_id(df, job_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job record not found",
        )

    skills = record.get("parsed_skills")
    if not isinstance(skills, list):
        skills = parse_skill_set(record.get("job_skill_set"))

    return {
        "job_id": int(record["job_id"]),
        "category": str(record["category"]),
        "job_title": str(record["job_title"]),
        "job_description": str(record["job_description"]),
        "job_skill_set": skills,
    }


@app.post("/api/match", response_model=MatchProfileResponse)
def match_profile(payload: MatchProfileRequest):
    """Execute deterministic career skill matching against the dataset.

    Returns ranked jobs with exact match scores, matched skills, and unreported skills.
    No LLM hallucination: 100% transparent set math.
    """
    df = get_dataset()
    jobs_cache = DATASET_STATE.get("jobs_cache")
    if not jobs_cache:
        jobs_cache = df.to_dict(orient="records")
        DATASET_STATE["jobs_cache"] = jobs_cache

    # Normalize extracted skill names from payload
    extracted_user_skills: list[str] = []
    for item in payload.skills:
        if isinstance(item, str):
            token = item.strip()
            if token:
                extracted_user_skills.append(token)
        elif isinstance(item, SkillInputItem):
            token = item.name.strip()
            if token:
                extracted_user_skills.append(token)
        elif isinstance(item, dict):
            token = str(item.get("name", "")).strip()
            if token:
                extracted_user_skills.append(token)

    if not extracted_user_skills:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="At least one valid non-empty skill is required.",
        )

    # Optional category filter check
    cat_filter = payload.category_filter.strip() if payload.category_filter else None
    if cat_filter:
        valid_cats = {c["id"].upper() for c in DATASET_STATE.get("categories", [])}
        if valid_cats and cat_filter.upper() not in valid_cats:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid category filter. Allowed categories: {sorted(valid_cats)}",
            )

    ranked_matches = match_profile_against_jobs(
        user_skills=extracted_user_skills,
        jobs=jobs_cache,
        category_filter=cat_filter,
        limit=payload.limit or 20,
    )

    # Calculate total evaluated jobs count in the filtered scope
    if cat_filter:
        total_eval = sum(1 for j in jobs_cache if str(j.get("category", "")).upper() == cat_filter.upper())
    else:
        total_eval = len(jobs_cache)

    return {
        "total_evaluated": total_eval,
        "matches": ranked_matches,
    }


# ---------------------------------------------------------------------------
# AI Career Assistant & Roadmap Schemas and Endpoints
# ---------------------------------------------------------------------------

class ChatUserProfile(BaseModel):
    skills: list[Union[SkillInputItem, str]] = Field(default_factory=list)
    interests: Optional[str] = Field(None, max_length=500)
    experience_summary: Optional[str] = Field(None, max_length=500)


class ChatMatchingContext(BaseModel):
    match_score: float = Field(0.0, ge=0.0, le=100.0)
    matched_skills: list[str] = Field(default_factory=list)
    unreported_skills: list[str] = Field(default_factory=list)


class ChatRequest(BaseModel):
    job_id: int
    question: str = Field(..., min_length=1, max_length=500)
    user_profile: Optional[ChatUserProfile] = None
    matching_context: Optional[ChatMatchingContext] = None


class GroundingSources(BaseModel):
    job_title: str
    matched_skills_count: int
    unreported_skills_count: int


class ChatResponse(BaseModel):
    job_id: int
    answer: str
    grounding_sources: GroundingSources
    ai_available: bool


class RoadmapRequest(BaseModel):
    job_id: int
    user_profile: Optional[ChatUserProfile] = None
    unreported_skills: list[str] = Field(default_factory=list)


class RoadmapMilestoneItem(BaseModel):
    stage: str
    skills_targeted: list[str]
    learning_objectives: str
    recommended_exercise: str


class RoadmapResponse(BaseModel):
    job_id: int
    job_title: str
    target_skills: list[str]
    milestones: list[RoadmapMilestoneItem]
    disclaimer: str


@app.post("/api/chat", response_model=ChatResponse)
def chat_career_assistant(payload: ChatRequest):
    """Contextually grounded AI career Q&A in natural Indonesian.

    Grounded strictly in the official job record and deterministic match results.
    Never hallucinates salaries, hiring probabilities, or ungrounded statistics.
    """
    df = get_dataset()
    job_record = get_job_by_id(df, payload.job_id)
    if not job_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job record not found",
        )

    # Extract user profile dict
    user_profile_dict: dict[str, Any] = {}
    if payload.user_profile:
        user_profile_dict = {
            "skills": payload.user_profile.skills,
            "interests": payload.user_profile.interests or "",
            "experience_summary": payload.user_profile.experience_summary or "",
        }

    # Extract or dynamically compute matching context
    if payload.matching_context:
        matching_ctx = {
            "match_score": payload.matching_context.match_score,
            "matched_skills": payload.matching_context.matched_skills,
            "unreported_skills": payload.matching_context.unreported_skills,
        }
    else:
        # Compute on the fly if not provided
        user_skills_list = [
            s.name if isinstance(s, SkillInputItem) else str(s)
            for s in user_profile_dict.get("skills", [])
        ]
        calc = calculate_match(user_skills_list, job_record.get("job_skill_set"))
        matching_ctx = {
            "match_score": calc["match_score"],
            "matched_skills": calc["matched_skills"],
            "unreported_skills": calc["unreported_skills"],
        }

    result = generate_career_chat_answer(
        job_id=payload.job_id,
        job_record=job_record,
        question=payload.question,
        user_profile=user_profile_dict,
        matching_context=matching_ctx,
    )
    return result


@app.post("/api/roadmap", response_model=RoadmapResponse)
def get_learning_roadmap(payload: RoadmapRequest):
    """Generate a structured 3-stage learning roadmap targeting unreported skills."""
    df = get_dataset()
    job_record = get_job_by_id(df, payload.job_id)
    if not job_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job record not found",
        )

    user_profile_dict: dict[str, Any] = {}
    if payload.user_profile:
        user_profile_dict = {
            "skills": payload.user_profile.skills,
            "interests": payload.user_profile.interests or "",
            "experience_summary": payload.user_profile.experience_summary or "",
        }

    target_skills = payload.unreported_skills
    if not target_skills:
        # Derive target skills from job skills vs user skills
        user_skills_list = [
            s.name if isinstance(s, SkillInputItem) else str(s)
            for s in user_profile_dict.get("skills", [])
        ]
        calc = calculate_match(user_skills_list, job_record.get("job_skill_set"))
        target_skills = calc["unreported_skills"]

    result = generate_learning_roadmap(
        job_id=payload.job_id,
        job_record=job_record,
        target_skills=target_skills,
        user_profile=user_profile_dict,
    )
    return result

