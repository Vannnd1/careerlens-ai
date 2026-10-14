import React from 'react'
import type { MatchResultItem } from '../types'

interface MatchListProps {
  matches: MatchResultItem[]
  totalEvaluated: number
  selectedCategory: string | null
  onSelectCategory: (category: string | null) => void
  onInspectJob: (job: MatchResultItem) => void
  isLoading: boolean
}

const CATEGORIES = [
  { id: null, label: 'Semua Kategori' },
  { id: 'INFORMATION-TECHNOLOGY', label: 'Information Technology' },
  { id: 'BUSINESS-DEVELOPMENT', label: 'Business Development' },
  { id: 'FINANCE', label: 'Finance' },
  { id: 'SALES', label: 'Sales' },
  { id: 'HR', label: 'Human Resources' },
]

export const MatchList: React.FC<MatchListProps> = ({
  matches,
  totalEvaluated,
  selectedCategory,
  onSelectCategory,
  onInspectJob,
  isLoading,
}) => {
  return (
    <div role="region" aria-labelledby="matches-heading">
      <div style={{ marginBottom: '16px' }}>
        <h2 id="matches-heading" style={{ fontSize: '20px', fontWeight: 700, letterSpacing: '-0.01em' }}>
          Hasil Kesesuaian Posisi Pekerjaan
        </h2>
        <p style={{ fontSize: '13px', color: 'var(--color-text-secondary)', marginTop: '4px' }}>
          Dievaluasi terhadap {totalEvaluated.toLocaleString()} catatan posisi pekerjaan dalam dataset.
        </p>
      </div>

      <nav className="category-filter-bar" aria-label="Filter Kategori Pekerjaan">
        {CATEGORIES.map((cat) => {
          const isActive = selectedCategory === cat.id
          return (
            <button
              key={cat.label}
              type="button"
              className={`cat-pill ${isActive ? 'active' : ''}`}
              onClick={() => onSelectCategory(cat.id)}
              aria-pressed={isActive}
            >
              {cat.label}
            </button>
          )
        })}
      </nav>

      {isLoading ? (
        <div className="matches-list" aria-busy="true" aria-label="Memuat hasil kecocokan">
          <div className="skeleton-card" />
          <div className="skeleton-card" />
          <div className="skeleton-card" />
        </div>
      ) : matches.length === 0 ? (
        <div className="card" style={{ textAlign: 'center', padding: '36px 20px' }} role="status">
          <h3 style={{ fontSize: '16px', fontWeight: 700, marginBottom: '8px' }}>
            Tidak Ditemukan Posisi yang Cocok
          </h3>
          <p style={{ fontSize: '13px', color: 'var(--color-text-secondary)', maxWidth: '440px', margin: '0 auto 16px' }}>
            Tidak ada posisi dalam kategori yang dipilih yang memiliki kecocokan dengan keahlian yang Anda laporkan saat ini.
          </p>
          {selectedCategory && (
            <button
              type="button"
              className="btn-secondary"
              onClick={() => onSelectCategory(null)}
            >
              Reset ke Semua Kategori
            </button>
          )}
        </div>
      ) : (
        <div className="matches-list" role="feed" aria-label="Daftar peringkat posisi yang cocok">
          {matches.map((job) => (
            <article key={job.job_id} className="job-card">
              <div className="job-card-header">
                <div>
                  <h3 className="job-title">{job.job_title}</h3>
                  <div className="job-category">{job.category.replace(/-/g, ' ')}</div>
                </div>
                <div className="score-badge" title="Persentase kesesuaian keahlian">
                  <span className="score-value">{job.match_score.toFixed(1)}%</span>
                  <span className="score-label">Kesesuaian</span>
                </div>
              </div>

              <div className="evidence-row">
                <strong>Bukti Kecocokan:</strong>{' '}
                <span>
                  {job.matched_skills.length} dari {job.total_required_skills} keahlian terpenuhi
                </span>
              </div>

              {job.matched_skills.length > 0 && (
                <div className="skills-group">
                  <span className="skills-group-title">Keahlian Cocok Terpenuhi:</span>
                  <div className="tags-cluster">
                    {job.matched_skills.map((skill) => (
                      <span key={skill} className="tag-matched">
                        &#10003; {skill}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {job.unreported_skills.length > 0 && (
                <div className="skills-group">
                  <span className="skills-group-title">
                    Keahlian Belum Dilaporkan (Potensi Dikembangkan):
                  </span>
                  <div className="tags-cluster">
                    {job.unreported_skills.slice(0, 6).map((skill) => (
                      <span key={skill} className="tag-unreported">
                        + {skill}
                      </span>
                    ))}
                    {job.unreported_skills.length > 6 && (
                      <span className="tag-unreported" style={{ fontStyle: 'italic' }}>
                        +{job.unreported_skills.length - 6} lainnya
                      </span>
                    )}
                  </div>
                </div>
              )}

              <div style={{ marginTop: '6px' }}>
                <button
                  type="button"
                  className="btn-secondary"
                  style={{ width: '100%' }}
                  onClick={() => onInspectJob(job)}
                >
                  Lihat Detail &amp; Panduan Belajar AI &rarr;
                </button>
              </div>
            </article>
          ))}
        </div>
      )}
    </div>
  )
}
