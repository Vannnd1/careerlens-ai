import React, { useState } from 'react'
import type { CareerProfile, SkillItem } from '../types'


interface ProfileFormProps {
  profile: CareerProfile
  onProfileChange: (newProfile: CareerProfile) => void
  onSubmit: () => void
  isLoading: boolean
}

const POPULAR_SUGGESTIONS = [
  'Python',
  'SQL',
  'Tableau',
  'Communication',
  'Problem Solving',
  'Project Management',
  'Financial Analysis',
  'Employee Relations',
  'Sales Strategy',
  'Excel',
  'Data Analysis',
]

export const ProfileForm: React.FC<ProfileFormProps> = ({
  profile,
  onProfileChange,
  onSubmit,
  isLoading,
}) => {
  const [skillInput, setSkillInput] = useState('')
  const [proficiency, setProficiency] = useState<'Pemula' | 'Menengah' | 'Mahir'>('Menengah')
  const [inputError, setInputError] = useState<string | null>(null)

  const handleAddSkill = (skillName: string) => {
    const trimmed = skillName.trim()
    if (!trimmed) return

    if (trimmed.length > 50) {
      setInputError('Nama keahlian maksimal 50 karakter.')
      return
    }

    const exists = profile.skills.some(
      (s) => s.name.toLowerCase() === trimmed.toLowerCase(),
    )
    if (exists) {
      setInputError(`Keahlian '${trimmed}' sudah ada di profil Anda.`)
      return
    }

    if (profile.skills.length >= 30) {
      setInputError('Maksimal 30 keahlian per profil.')
      return
    }

    setInputError(null)
    const newSkills: SkillItem[] = [
      ...profile.skills,
      { name: trimmed, proficiency },
    ]
    onProfileChange({ ...profile, skills: newSkills })
    setSkillInput('')
  }

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault()
      handleAddSkill(skillInput)
    }
  }

  const handleRemoveSkill = (skillToRemove: string) => {
    const updated = profile.skills.filter(
      (s) => s.name.toLowerCase() !== skillToRemove.toLowerCase(),
    )
    onProfileChange({ ...profile, skills: updated })
  }

  return (
    <div className="card" role="region" aria-labelledby="profile-heading">
      <div className="card-header">
        <h2 id="profile-heading" className="card-title">
          Profil Keahlian Anda
        </h2>
        <p className="card-subtitle">
          Masukkan keahlian yang Anda miliki untuk mencocokkan dengan data pekerjaan.
        </p>
      </div>

      <div className="form-group">
        <label htmlFor="skill-input-field" className="form-label">
          Tambah Keahlian ({profile.skills.length}/30)
        </label>
        <div style={{ display: 'flex', gap: '8px' }}>
          <input
            id="skill-input-field"
            type="text"
            className="form-input"
            placeholder="Ketik keahlian (contoh: Python, SQL)..."
            value={skillInput}
            onChange={(e) => {
              setSkillInput(e.target.value)
              if (inputError) setInputError(null)
            }}
            onKeyDown={handleKeyDown}
            aria-describedby={inputError ? 'skill-error-msg' : undefined}
          />
          <button
            type="button"
            className="btn-secondary"
            onClick={() => handleAddSkill(skillInput)}
          >
            Tambah
          </button>
        </div>
        {inputError && (
          <p id="skill-error-msg" className="validation-msg" role="alert">
            {inputError}
          </p>
        )}
      </div>

      {profile.skills.length > 0 && (
        <div className="form-group">
          <span className="form-label">Keahlian Terpilih:</span>
          <div className="chips-container" role="list" aria-label="Daftar keahlian yang dilaporkan">
            {profile.skills.map((skill) => (
              <span
                key={skill.name}
                className="skill-chip"
                role="listitem"
              >
                <span>{skill.name}</span>
                <span style={{ fontSize: '10px', color: 'var(--color-text-muted)' }}>
                  ({skill.proficiency || 'Menengah'})
                </span>
                <button
                  type="button"
                  className="chip-btn-remove"
                  onClick={() => handleRemoveSkill(skill.name)}
                  aria-label={`Hapus keahlian ${skill.name}`}
                >
                  &times;
                </button>
              </span>
            ))}
          </div>
        </div>
      )}

      <div className="form-group">
        <span className="suggested-label">Saran Keahlian Cepat:</span>
        <div className="chips-container">
          {POPULAR_SUGGESTIONS.map((suggestion) => {
            const alreadyAdded = profile.skills.some(
              (s) => s.name.toLowerCase() === suggestion.toLowerCase(),
            )
            if (alreadyAdded) return null
            return (
              <button
                key={suggestion}
                type="button"
                className="suggestion-chip"
                onClick={() => handleAddSkill(suggestion)}
              >
                + {suggestion}
              </button>
            )
          })}
        </div>
      </div>

      <div className="form-group">
        <label htmlFor="proficiency-select" className="form-label">
          Tingkat Kemahiran Standar
        </label>
        <select
          id="proficiency-select"
          className="form-select"
          value={proficiency}
          onChange={(e) =>
            setProficiency(e.target.value as 'Pemula' | 'Menengah' | 'Mahir')
          }
        >
          <option value="Pemula">Pemula (Dasar / Belajar)</option>
          <option value="Menengah">Menengah (Praktik Mandiri)</option>
          <option value="Mahir">Mahir (Portofolio / Pengalaman Proyek)</option>
        </select>
      </div>

      <div className="form-group">
        <label htmlFor="interests-input" className="form-label">
          Minat Karir (Opsional)
        </label>
        <textarea
          id="interests-input"
          className="form-textarea"
          placeholder="Jelaskan bidang atau industri yang Anda minati (contoh: otomatisasi data, manajemen talenta)..."
          maxLength={300}
          value={profile.interests || ''}
          onChange={(e) =>
            onProfileChange({ ...profile, interests: e.target.value })
          }
        />
      </div>

      <div className="form-group">
        <label htmlFor="experience-input" className="form-label">
          Pengalaman Singkat (Opsional)
        </label>
        <textarea
          id="experience-input"
          className="form-textarea"
          placeholder="Ringkasan latar belakang (contoh: Mahasiswa tingkat akhir jurusan Sistem Informasi, magang 6 bulan)..."
          maxLength={300}
          value={profile.experience_summary || ''}
          onChange={(e) =>
            onProfileChange({ ...profile, experience_summary: e.target.value })
          }
        />
      </div>

      <button
        type="button"
        className="btn-primary"
        onClick={onSubmit}
        disabled={isLoading || profile.skills.length === 0}
      >
        {isLoading ? 'Menganalisis Kecocokan...' : 'Hitung Kesesuaian Karir'}
      </button>
    </div>
  )
}
