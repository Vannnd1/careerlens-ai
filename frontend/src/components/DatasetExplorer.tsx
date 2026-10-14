import React, { useEffect, useState } from 'react'
import { fetchCategories, fetchJobDetail, fetchJobs } from '../api'
import type { CategorySummary, JobDetailRecord, JobSummaryItem } from '../types'


export const DatasetExplorer: React.FC = () => {
  const [categories, setCategories] = useState<CategorySummary[]>([])
  const [selectedCat, setSelectedCat] = useState<string | null>(null)
  const [searchQuery, setSearchQuery] = useState('')
  const [page, setPage] = useState(1)
  const [pageSize] = useState(15)

  const [jobs, setJobs] = useState<JobSummaryItem[]>([])
  const [totalJobs, setTotalJobs] = useState(0)
  const [isLoading, setIsLoading] = useState(false)
  const [errorMsg, setErrorMsg] = useState<string | null>(null)

  // Inspector modal state
  const [inspectedJob, setInspectedJob] = useState<JobDetailRecord | null>(null)
  const [isLoadingDetail, setIsLoadingDetail] = useState(false)

  // Load categories summary on mount
  useEffect(() => {
    fetchCategories()
      .then(setCategories)
      .catch((err) => console.warn('Failed to load categories', err))
  }, [])

  // Load jobs when filter, query, or page changes
  useEffect(() => {
    let isMounted = true

    const loadJobs = async () => {
      setIsLoading(true)
      setErrorMsg(null)
      try {
        const data = await fetchJobs(searchQuery, selectedCat || undefined, page, pageSize)
        if (isMounted) {
          setJobs(data.jobs)
          setTotalJobs(data.total)
        }
      } catch (err: unknown) {
        if (isMounted) {
          setErrorMsg(err instanceof Error ? err.message : 'Gagal memuat katalog data.')
        }
      } finally {
        if (isMounted) {
          setIsLoading(false)
        }
      }
    }

    void loadJobs()

    return () => {
      isMounted = false
    }
  }, [searchQuery, selectedCat, page, pageSize])

  const handleInspect = async (jobId: number) => {
    setIsLoadingDetail(true)
    try {
      const data = await fetchJobDetail(jobId)
      setInspectedJob(data)
    } catch (err: unknown) {
      alert(err instanceof Error ? err.message : 'Gagal memuat detail pekerjaan')
    } finally {
      setIsLoadingDetail(false)
    }
  }

  const totalPages = Math.ceil(totalJobs / pageSize) || 1

  return (
    <div style={{ padding: '24px 0 48px' }} role="region" aria-labelledby="explorer-heading">
      <div style={{ marginBottom: '20px' }}>
        <h1 id="explorer-heading" style={{ fontSize: '24px', fontWeight: 700, letterSpacing: '-0.02em' }}>
          Eksplorasi Dataset Posisi &amp; Keahlian
        </h1>
        <p style={{ fontSize: '14px', color: 'var(--color-text-secondary)', marginTop: '4px' }}>
          Jelajahi 1,167 data posisi resmi dari Job Skill Set Dataset (Batuhan Mutlu, 2024 / LinkedIn Job Postings).
        </p>
      </div>

      {/* Category Pills with Real Counts */}
      <div className="category-filter-bar" aria-label="Filter kategori explorer">
        <button
          type="button"
          className={`cat-pill ${selectedCat === null ? 'active' : ''}`}
          onClick={() => {
            setSelectedCat(null)
            setPage(1)
          }}
        >
          Semua ({categories.reduce((acc, c) => acc + c.count, 0)})
        </button>
        {categories.map((c) => (
          <button
            key={c.id}
            type="button"
            className={`cat-pill ${selectedCat === c.id ? 'active' : ''}`}
            onClick={() => {
              setSelectedCat(c.id)
              setPage(1)
            }}
          >
            {c.label} ({c.count})
          </button>
        ))}
      </div>

      {/* Search Bar */}
      <div style={{ maxWidth: '500px', marginBottom: '20px' }}>
        <label htmlFor="explorer-search-input" className="form-label">
          Cari Berdasarkan Judul atau Deskripsi Pekerjaan:
        </label>
        <input
          id="explorer-search-input"
          type="text"
          className="form-input"
          placeholder="Ketik kata kunci (contoh: Python, HR Manager, Sales)..."
          value={searchQuery}
          onChange={(e) => {
            setSearchQuery(e.target.value)
            setPage(1)
          }}
        />
      </div>

      {errorMsg && (
        <div className="alert-banner error">
          <span>{errorMsg}</span>
          <button
            type="button"
            className="btn-retry"
            onClick={() => setPage((p) => p)}
          >
            Coba Lagi
          </button>
        </div>
      )}

      {/* Results Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
        <span style={{ fontSize: '13px', fontWeight: 600, color: 'var(--color-text-secondary)' }}>
          Menampilkan {jobs.length} dari {totalJobs.toLocaleString()} posisi
        </span>
        <div style={{ display: 'flex', gap: '8px' }}>
          <button
            type="button"
            className="btn-secondary"
            disabled={page <= 1 || isLoading}
            onClick={() => setPage((p) => Math.max(1, p - 1))}
          >
            &larr; Sebelumnya
          </button>
          <span style={{ fontSize: '13px', alignSelf: 'center', padding: '0 4px' }}>
            Hal {page} / {totalPages}
          </span>
          <button
            type="button"
            className="btn-secondary"
            disabled={page >= totalPages || isLoading}
            onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
          >
            Berikutnya &rarr;
          </button>
        </div>
      </div>

      {/* Job Records Table/Grid */}
      {isLoading ? (
        <div className="matches-list" aria-busy="true">
          <div className="skeleton-card" />
          <div className="skeleton-card" />
          <div className="skeleton-card" />
        </div>
      ) : jobs.length === 0 ? (
        <div className="card" style={{ textAlign: 'center', padding: '36px' }}>
          <p style={{ color: 'var(--color-text-secondary)' }}>
            Tidak ada catatan posisi yang cocok dengan kata kunci pencarian Anda.
          </p>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {jobs.map((job) => (
            <article key={job.job_id} className="card" style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <div>
                  <h2 style={{ fontSize: '16px', fontWeight: 700 }}>{job.job_title}</h2>
                  <div style={{ fontSize: '12px', color: 'var(--color-text-muted)', textTransform: 'uppercase' }}>
                    {job.category.replace(/-/g, ' ')} &bull; ID: {job.job_id}
                  </div>
                </div>
                <button
                  type="button"
                  className="btn-secondary"
                  disabled={isLoadingDetail}
                  onClick={() => handleInspect(job.job_id)}
                >
                  Lihat Deskripsi Lengkap
                </button>
              </div>

              <p style={{ fontSize: '13px', color: 'var(--color-text-secondary)', lineHeight: 1.5 }}>
                {job.description_snippet}
              </p>

              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px', marginTop: '4px' }}>
                <span style={{ fontSize: '12px', fontWeight: 600, color: 'var(--color-text-muted)', marginRight: '4px' }}>
                  {job.skills_count} Keahlian:
                </span>
                {job.skills.slice(0, 8).map((s) => (
                  <span key={s} className="tag-unreported" style={{ fontSize: '11px' }}>
                    {s}
                  </span>
                ))}
                {job.skills.length > 8 && (
                  <span className="tag-unreported" style={{ fontSize: '11px', fontStyle: 'italic' }}>
                    +{job.skills.length - 8} lainnya
                  </span>
                )}
              </div>
            </article>
          ))}
        </div>
      )}

      {/* Record Inspector Modal */}
      {inspectedJob && (
        <div
          className="modal-overlay"
          role="dialog"
          aria-modal="true"
          onClick={() => setInspectedJob(null)}
        >
          <div className="modal-drawer" onClick={(e) => e.stopPropagation()}>
            <div className="drawer-header">
              <div>
                <h2 style={{ fontSize: '18px', fontWeight: 700 }}>{inspectedJob.job_title}</h2>
                <div style={{ fontSize: '12px', color: 'var(--color-text-muted)', textTransform: 'uppercase' }}>
                  {inspectedJob.category.replace(/-/g, ' ')} &bull; ID: {inspectedJob.job_id}
                </div>
              </div>
              <button
                type="button"
                className="drawer-close-btn"
                onClick={() => setInspectedJob(null)}
                aria-label="Tutup"
              >
                &times;
              </button>
            </div>

            <div className="section-block">
              <span className="skills-group-title">
                Daftar Keahlian Resmi ({inspectedJob.job_skill_set.length}):
              </span>
              <div className="tags-cluster">
                {inspectedJob.job_skill_set.map((s) => (
                  <span key={s} className="tag-unreported">
                    {s}
                  </span>
                ))}
              </div>
            </div>

            <div className="section-block">
              <h3 className="section-heading">Deskripsi Lengkap Posisi</h3>
              <div className="job-desc-text" style={{ maxHeight: '400px' }}>
                {inspectedJob.job_description}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
