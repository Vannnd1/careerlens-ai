export interface SkillItem {
  name: string
  proficiency?: 'Pemula' | 'Menengah' | 'Mahir' | string
}

export interface CareerProfile {
  skills: SkillItem[]
  category_filter?: string | null
  interests?: string
  experience_summary?: string
}

export interface MatchResultItem {
  job_id: number
  job_title: string
  category: string
  match_score: number
  matched_skills: string[]
  unreported_skills: string[]
  total_required_skills: number
}

export interface MatchProfileResponse {
  total_evaluated: number
  matches: MatchResultItem[]
}

export interface CategorySummary {
  id: string
  label: string
  count: number
}

export interface JobSummaryItem {
  job_id: number
  category: string
  job_title: string
  description_snippet: string
  skills_count: number
  skills: string[]
}

export interface JobListResponse {
  total: number
  page: number
  page_size: number
  jobs: JobSummaryItem[]
}

export interface JobDetailRecord {
  job_id: number
  category: string
  job_title: string
  job_description: string
  job_skill_set: string[]
}

export interface ChatMessage {
  sender: 'user' | 'assistant'
  text: string
  timestamp: string
  ai_available?: boolean
}

export interface RoadmapMilestone {
  stage: string
  skills_targeted: string[]
  learning_objectives: string
  recommended_exercise: string
}

export interface RoadmapResponse {
  job_id: number
  job_title: string
  target_skills: string[]
  milestones: RoadmapMilestone[]
  disclaimer: string
}

export interface HealthStatus {
  status: string
  dataset_loaded: boolean
  total_jobs: number
  gemini_configured: boolean
}
