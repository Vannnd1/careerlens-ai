import type {
  CareerProfile,
  CategorySummary,
  HealthStatus,
  JobDetailRecord,
  JobListResponse,
  MatchProfileResponse,
  RoadmapResponse,
} from './types'

const BASE_URL = ''

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let errorMsg = `Server error (${res.status})`
    try {
      const errJson = await res.json()
      if (errJson && errJson.detail) {
        errorMsg = errJson.detail
      }
    } catch {
      // Fallback if not json
    }
    throw new Error(errorMsg)
  }
  return res.json()
}

export async function fetchHealth(): Promise<HealthStatus> {
  const res = await fetch(`${BASE_URL}/api/health`)
  return handleResponse<HealthStatus>(res)
}

export async function fetchCategories(): Promise<CategorySummary[]> {
  const res = await fetch(`${BASE_URL}/api/categories`)
  const data = await handleResponse<{ categories: CategorySummary[] }>(res)
  return data.categories
}

export async function fetchJobs(
  query?: string,
  category?: string,
  page = 1,
  pageSize = 20,
): Promise<JobListResponse> {
  const params = new URLSearchParams()
  if (query && query.trim()) params.append('query', query.trim())
  if (category && category.trim()) params.append('category', category.trim())
  params.append('page', String(page))
  params.append('page_size', String(pageSize))

  const res = await fetch(`${BASE_URL}/api/jobs?${params.toString()}`)
  return handleResponse<JobListResponse>(res)
}

export async function fetchJobDetail(jobId: number): Promise<JobDetailRecord> {
  const res = await fetch(`${BASE_URL}/api/jobs/${jobId}`)
  return handleResponse<JobDetailRecord>(res)
}

export async function matchProfile(profile: CareerProfile): Promise<MatchProfileResponse> {
  const payload = {
    skills: profile.skills.map((s) => ({
      name: s.name,
      proficiency: s.proficiency || 'Menengah',
    })),
    category_filter: profile.category_filter || null,
    interests: profile.interests || '',
    experience_summary: profile.experience_summary || '',
    limit: 25,
  }

  const res = await fetch(`${BASE_URL}/api/match`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  return handleResponse<MatchProfileResponse>(res)
}

export async function sendCareerChat(
  jobId: number,
  question: string,
  userProfile: CareerProfile,
  matchingContext?: {
    match_score: number
    matched_skills: string[]
    unreported_skills: string[]
  },
): Promise<{ answer: string; ai_available: boolean }> {
  const payload = {
    job_id: jobId,
    question,
    user_profile: {
      skills: userProfile.skills,
      interests: userProfile.interests || '',
      experience_summary: userProfile.experience_summary || '',
    },
    matching_context: matchingContext,
  }

  const res = await fetch(`${BASE_URL}/api/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  return handleResponse<{ answer: string; ai_available: boolean }>(res)
}

export async function fetchRoadmap(
  jobId: number,
  unreportedSkills: string[],
  userProfile: CareerProfile,
): Promise<RoadmapResponse> {
  const payload = {
    job_id: jobId,
    unreported_skills: unreportedSkills,
    user_profile: {
      skills: userProfile.skills,
      experience_summary: userProfile.experience_summary || '',
    },
  }

  const res = await fetch(`${BASE_URL}/api/roadmap`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  return handleResponse<RoadmapResponse>(res)
}
