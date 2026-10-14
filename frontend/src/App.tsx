import React, { useEffect, useState } from 'react'
import { fetchHealth, matchProfile } from './api'
import { DatasetExplorer } from './components/DatasetExplorer'
import { Footer } from './components/Footer'
import { Header } from './components/Header'
import { JobDetailModal } from './components/JobDetailModal'
import { MatchList } from './components/MatchList'
import { ProfileForm } from './components/ProfileForm'
import type { CareerProfile, HealthStatus, MatchResultItem } from './types'

export const App: React.FC = () => {
  const [activeView, setActiveView] = useState<'workbench' | 'explorer'>('workbench')
  const [health, setHealth] = useState<HealthStatus | null>(null)
  const [serviceError, setServiceError] = useState<string | null>(null)

  // Profile Form State
  const [profile, setProfile] = useState<CareerProfile>({
    skills: [
      { name: 'Python', proficiency: 'Menengah' },
      { name: 'SQL', proficiency: 'Menengah' },
      { name: 'Communication', proficiency: 'Mahir' },
    ],
    category_filter: null,
    interests: '',
    experience_summary: '',
  })

  // Matching Results State
  const [matches, setMatches] = useState<MatchResultItem[]>([])
  const [totalEvaluated, setTotalEvaluated] = useState(0)
  const [isLoadingMatches, setIsLoadingMatches] = useState(false)

  // Selected job for detailed inspection & AI assistance
  const [inspectedJob, setInspectedJob] = useState<MatchResultItem | null>(null)

  // Load backend health on mount
  useEffect(() => {
    fetchHealth()
      .then(setHealth)
      .catch(() => {
        setServiceError(
          'Gagal terhubung ke backend FastAPI. Pastikan server backend sedang berjalan di http://127.0.0.1:8000.',
        )
      })
  }, [])

  // Execute matching calculation
  const handleCalculateMatch = async (customCategoryFilter?: string | null) => {
    if (profile.skills.length === 0) return

    setIsLoadingMatches(true)
    setServiceError(null)

    const profileToMatch: CareerProfile = {
      ...profile,
      category_filter:
        customCategoryFilter !== undefined
          ? customCategoryFilter
          : profile.category_filter,
    }

    try {
      const response = await matchProfile(profileToMatch)
      setMatches(response.matches)
      setTotalEvaluated(response.total_evaluated)
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Terjadi kesalahan saat memproses pencocokan'
      setServiceError(msg)
    } finally {
      setIsLoadingMatches(false)
    }
  }

  // Initial calculation on mount
  useEffect(() => {
    handleCalculateMatch()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const handleSelectCategory = (catId: string | null) => {
    setProfile((prev) => ({ ...prev, category_filter: catId }))
    handleCalculateMatch(catId)
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Header
        activeView={activeView}
        onSelectView={setActiveView}
        health={health}
      />

      <main className="container" style={{ flex: 1 }}>
        {serviceError && (
          <div className="alert-banner error" style={{ marginTop: '20px' }} role="alert">
            <div>
              <strong>Koneksi Layanan:</strong> {serviceError}
            </div>
            <button
              type="button"
              className="btn-retry"
              onClick={() => {
                setServiceError(null)
                fetchHealth().then(setHealth).catch(() => {})
                handleCalculateMatch()
              }}
            >
              Coba Lagi
            </button>
          </div>
        )}

        {activeView === 'workbench' ? (
          <div className="workbench-layout">
            <aside>
              <ProfileForm
                profile={profile}
                onProfileChange={setProfile}
                onSubmit={() => handleCalculateMatch()}
                isLoading={isLoadingMatches}
              />
            </aside>

            <section>
              <MatchList
                matches={matches}
                totalEvaluated={totalEvaluated}
                selectedCategory={profile.category_filter || null}
                onSelectCategory={handleSelectCategory}
                onInspectJob={setInspectedJob}
                isLoading={isLoadingMatches}
              />
            </section>
          </div>
        ) : (
          <DatasetExplorer />
        )}

        {inspectedJob && (
          <JobDetailModal
            jobMatch={inspectedJob}
            profile={profile}
            onClose={() => setInspectedJob(null)}
          />
        )}
      </main>

      <Footer />
    </div>
  )
}

export default App
