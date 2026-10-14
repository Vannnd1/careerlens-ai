import React, { useEffect, useState } from 'react'
import { fetchJobDetail, fetchRoadmap, sendCareerChat } from '../api'
import type {
  CareerProfile,
  ChatMessage,
  JobDetailRecord,
  MatchResultItem,
  RoadmapResponse,
} from '../types'

interface JobDetailModalProps {
  jobMatch: MatchResultItem
  profile: CareerProfile
  onClose: () => void
}

function renderInlineBold(text: string): React.ReactNode[] {
  const parts = text.split(/(\*\*[^*]+\*\*)/g)
  return parts.map((part, i) => {
    if (part.startsWith('**') && part.endsWith('**')) {
      return <strong key={i}>{part.slice(2, -2)}</strong>
    }
    const italicParts = part.split(/(\*[^*]+\*)/g)
    if (italicParts.length > 1) {
      return (
        <React.Fragment key={i}>
          {italicParts.map((sub, j) => {
            if (sub.startsWith('*') && sub.endsWith('*')) {
              return <em key={j}>{sub.slice(1, -1)}</em>
            }
            return sub
          })}
        </React.Fragment>
      )
    }
    return part
  })
}

function renderFormattedChatText(text: string) {
  const lines = text.split('\n')
  return (
    <div className="formatted-chat-content">
      {lines.map((line, idx) => {
        const trimmed = line.trim()
        if (!trimmed) {
          return <div key={idx} style={{ height: '6px' }} />
        }

        if (trimmed.startsWith('### ') || trimmed.startsWith('## ')) {
          const headingText = trimmed.replace(/^#+\s*/, '')
          return (
            <div key={idx} style={{ fontWeight: 700, margin: '8px 0 4px', color: 'inherit', fontSize: '13.5px' }}>
              {renderInlineBold(headingText)}
            </div>
          )
        }

        if (trimmed.startsWith('* ') || trimmed.startsWith('- ')) {
          const bulletText = trimmed.replace(/^[*-]\s*/, '')
          return (
            <div key={idx} style={{ display: 'flex', gap: '6px', marginLeft: '6px', marginBottom: '4px' }}>
              <span style={{ color: 'var(--color-accent)', fontWeight: 700 }}>•</span>
              <div style={{ flex: 1 }}>{renderInlineBold(bulletText)}</div>
            </div>
          )
        }

        return (
          <div key={idx} style={{ marginBottom: '4px', lineHeight: 1.55 }}>
            {renderInlineBold(line)}
          </div>
        )
      })}
    </div>
  )
}

export const JobDetailModal: React.FC<JobDetailModalProps> = ({
  jobMatch,
  profile,
  onClose,
}) => {
  const [jobDetail, setJobDetail] = useState<JobDetailRecord | null>(null)
  const [isLoadingDetail, setIsLoadingDetail] = useState(true)
  const [detailError, setDetailError] = useState<string | null>(null)

  // Active section tab in modal
  const [activeTab, setActiveTab] = useState<'desc' | 'chat' | 'roadmap'>('desc')

  // Career Chat state
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([
    {
      sender: 'assistant',
      text: `Halo! Saya asisten karir untuk posisi ${jobMatch.job_title}. Anda dapat menanyakan relevansi keahlian Anda, tanggung jawab pekerjaan ini, atau saran persiapan wawancara.`,
      timestamp: 'Sekarang',
    },
  ])
  const [chatQuestion, setChatQuestion] = useState('')
  const [isSendingChat, setIsSendingChat] = useState(false)

  // Learning Roadmap state
  const [roadmap, setRoadmap] = useState<RoadmapResponse | null>(null)
  const [isLoadingRoadmap, setIsLoadingRoadmap] = useState(false)
  const [roadmapError, setRoadmapError] = useState<string | null>(null)

  // Escape key listener to close modal
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose()
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [onClose])

  // Load detailed job record from API
  useEffect(() => {
    let isMounted = true
    const load = async () => {
      try {
        const data = await fetchJobDetail(jobMatch.job_id)
        if (isMounted) setJobDetail(data)
      } catch (err: unknown) {
        if (isMounted) setDetailError(err instanceof Error ? err.message : 'Gagal memuat detail pekerjaan.')
      } finally {
        if (isMounted) setIsLoadingDetail(false)
      }
    }
    load()
    return () => {
      isMounted = false
    }
  }, [jobMatch.job_id])

  const handleSendChat = async (e?: React.FormEvent) => {
    if (e) e.preventDefault()
    const q = chatQuestion.trim()
    if (!q || isSendingChat) return

    const userMsg: ChatMessage = {
      sender: 'user',
      text: q,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    }
    setChatMessages((prev) => [...prev, userMsg])
    setChatQuestion('')
    setIsSendingChat(true)

    try {
      const res = await sendCareerChat(jobMatch.job_id, q, profile, {
        match_score: jobMatch.match_score,
        matched_skills: jobMatch.matched_skills,
        unreported_skills: jobMatch.unreported_skills,
      })
      const botMsg: ChatMessage = {
        sender: 'assistant',
        text: res.answer,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        ai_available: res.ai_available,
      }
      setChatMessages((prev) => [...prev, botMsg])
    } catch (err: unknown) {
      const errorMsg = err instanceof Error ? err.message : 'Gagal menghubungi asisten AI'
      setChatMessages((prev) => [
        ...prev,
        {
          sender: 'assistant',
          text: `Maaf, terjadi kendala jaringan: ${errorMsg}`,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          ai_available: false,
        },
      ])
    } finally {
      setIsSendingChat(false)
    }
  }

  const handleGenerateRoadmap = async () => {
    if (roadmap || isLoadingRoadmap) return
    setIsLoadingRoadmap(true)
    setRoadmapError(null)
    try {
      const data = await fetchRoadmap(jobMatch.job_id, jobMatch.unreported_skills, profile)
      setRoadmap(data)
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Gagal menghasilkan roadmap'
      setRoadmapError(msg)
    } finally {
      setIsLoadingRoadmap(false)
    }
  }

  return (
    <div
      className="modal-overlay"
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-job-title"
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose()
      }}
    >
      <div className="modal-drawer">
        <div className="drawer-header">
          <div>
            <h2 id="modal-job-title" style={{ fontSize: '20px', fontWeight: 700 }}>
              {jobMatch.job_title}
            </h2>
            <div style={{ fontSize: '12px', color: 'var(--color-text-muted)', textTransform: 'uppercase', marginTop: '2px' }}>
              {jobMatch.category.replace(/-/g, ' ')} &bull; Skor Kesesuaian: {jobMatch.match_score.toFixed(1)}%
            </div>
          </div>
          <button
            type="button"
            className="drawer-close-btn"
            onClick={onClose}
            aria-label="Tutup panel detail"
          >
            &times;
          </button>
        </div>

        {/* Sub-navigation tabs */}
        <div style={{ display: 'flex', gap: '8px', borderBottom: '1px solid var(--color-border-subtle)', paddingBottom: '8px' }}>
          <button
            type="button"
            className={`nav-tab-btn ${activeTab === 'desc' ? 'active' : ''}`}
            onClick={() => setActiveTab('desc')}
          >
            Deskripsi Resmi
          </button>
          <button
            type="button"
            className={`nav-tab-btn ${activeTab === 'chat' ? 'active' : ''}`}
            onClick={() => setActiveTab('chat')}
          >
            Asisten Karir AI
          </button>
          <button
            type="button"
            className={`nav-tab-btn ${activeTab === 'roadmap' ? 'active' : ''}`}
            onClick={() => {
              setActiveTab('roadmap')
              if (!roadmap) handleGenerateRoadmap()
            }}
          >
            Roadmap Belajar
          </button>
        </div>

        {/* Tab 1: Verbatim Job Description & Skill Summary */}
        {activeTab === 'desc' && (
          <div className="section-block">
            <div className="skills-group">
              <span className="skills-group-title">Keahlian Cocok ({jobMatch.matched_skills.length}):</span>
              <div className="tags-cluster">
                {jobMatch.matched_skills.length === 0 ? (
                  <span style={{ fontSize: '13px', color: 'var(--color-text-muted)' }}>(Belum ada keahlian yang cocok)</span>
                ) : (
                  jobMatch.matched_skills.map((s) => (
                    <span key={s} className="tag-matched">&#10003; {s}</span>
                  ))
                )}
              </div>
            </div>

            <div className="skills-group" style={{ marginTop: '12px' }}>
              <span className="skills-group-title">
                Keahlian Belum Dilaporkan ({jobMatch.unreported_skills.length}):
              </span>
              <div className="tags-cluster">
                {jobMatch.unreported_skills.map((s) => (
                  <span key={s} className="tag-unreported">+ {s}</span>
                ))}
              </div>
            </div>

            <div style={{ marginTop: '16px' }}>
              <h3 className="section-heading">Deskripsi Pekerjaan Resmi (Dataset)</h3>
              {isLoadingDetail ? (
                <div style={{ padding: '20px', color: 'var(--color-text-muted)' }}>Memuat deskripsi resmi...</div>
              ) : detailError ? (
                <div className="alert-banner error" style={{ marginTop: '8px' }}>{detailError}</div>
              ) : (
                <div className="job-desc-text">
                  {jobDetail?.job_description || 'Deskripsi tidak tersedia.'}
                </div>
              )}
            </div>
          </div>
        )}

        {/* Tab 2: Grounded AI Career Assistant Chat */}
        {activeTab === 'chat' && (
          <div className="section-block">
            <p style={{ fontSize: '12px', color: 'var(--color-text-muted)', marginBottom: '4px' }}>
              Jawaban AI didasarkan secara eksklusif pada deskripsi resmi posisi ini dan keahlian yang cocok.
            </p>

            <div className="chat-transcript" role="log" aria-live="polite">
              {chatMessages.map((msg, i) => (
                <div key={i} className={`chat-bubble ${msg.sender}`}>
                  {renderFormattedChatText(msg.text)}
                  <div style={{ fontSize: '10px', opacity: 0.7, marginTop: '4px', textAlign: 'right' }}>
                    {msg.timestamp}
                    {msg.ai_available === false && ' (Mode Cadangan)'}
                  </div>
                </div>
              ))}
              {isSendingChat && (
                <div className="chat-bubble assistant" style={{ fontStyle: 'italic', opacity: 0.8 }}>
                  AI sedang menyusun jawaban berdasarkan data posisi...
                </div>
              )}
            </div>

            <form onSubmit={handleSendChat} className="chat-input-bar">
              <input
                type="text"
                className="form-input"
                placeholder="Tanyakan tentang peran ini atau cara melengkapi keahlian..."
                value={chatQuestion}
                onChange={(e) => setChatQuestion(e.target.value)}
                disabled={isSendingChat}
                maxLength={500}
              />
              <button
                type="submit"
                className="btn-primary"
                style={{ width: 'auto', minWidth: '90px' }}
                disabled={isSendingChat || !chatQuestion.trim()}
              >
                Kirim
              </button>
            </form>
          </div>
        )}

        {/* Tab 3: Personalized Learning Roadmap */}
        {activeTab === 'roadmap' && (
          <div className="section-block">
            <h3 className="section-heading">Rencana Belajar Bertahap (3 Milestone)</h3>
            <p style={{ fontSize: '13px', color: 'var(--color-text-secondary)' }}>
              Strategi belajar terstruktur untuk menjembatani {jobMatch.unreported_skills.length} keahlian yang belum dilaporkan.
            </p>

            {isLoadingRoadmap ? (
              <div style={{ padding: '30px', textAlign: 'center', color: 'var(--color-text-muted)' }}>
                Sedang menyusun milestone pembelajaran...
              </div>
            ) : roadmapError ? (
              <div className="alert-banner error">
                <span>{roadmapError}</span>
                <button type="button" className="btn-retry" onClick={handleGenerateRoadmap}>
                  Coba Lagi
                </button>
              </div>
            ) : roadmap ? (
              <div className="milestones-list">
                {roadmap.milestones.map((m, idx) => (
                  <div key={idx} className="milestone-item">
                    <div className="milestone-stage-title">{m.stage}</div>
                    <div style={{ fontSize: '12px', fontWeight: 600, color: 'var(--color-text-muted)', marginBottom: '4px' }}>
                      Keahlian Sasaran: {m.skills_targeted.join(', ')}
                    </div>
                    <div className="milestone-detail">{m.learning_objectives}</div>
                    <div className="milestone-exercise">
                      <strong>Latihan Portofolio:</strong> {m.recommended_exercise}
                    </div>
                  </div>
                ))}
                <p style={{ fontSize: '11px', color: 'var(--color-text-muted)', fontStyle: 'italic', marginTop: '8px' }}>
                  {roadmap.disclaimer}
                </p>
              </div>
            ) : (
              <button type="button" className="btn-primary" onClick={handleGenerateRoadmap}>
                Buat Roadmap Belajar
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
