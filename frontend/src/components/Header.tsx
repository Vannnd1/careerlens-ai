import React from 'react'
import type { HealthStatus } from '../types'

interface HeaderProps {
  activeView: 'workbench' | 'explorer'
  onSelectView: (view: 'workbench' | 'explorer') => void
  health: HealthStatus | null
}

export const Header: React.FC<HeaderProps> = ({
  activeView,
  onSelectView,
  health,
}) => {
  return (
    <header className="app-header" role="banner">
      <div className="container header-inner">
        <div className="brand-group">
          <span className="brand-title">CareerLens AI</span>
          <span className="brand-badge">Career Intelligence</span>
        </div>

        <nav className="nav-tabs" aria-label="Navigasi Utama">
          <button
            type="button"
            className={`nav-tab-btn ${activeView === 'workbench' ? 'active' : ''}`}
            onClick={() => onSelectView('workbench')}
            aria-current={activeView === 'workbench' ? 'page' : undefined}
          >
            Kesesuaian Karir
          </button>
          <button
            type="button"
            className={`nav-tab-btn ${activeView === 'explorer' ? 'active' : ''}`}
            onClick={() => onSelectView('explorer')}
            aria-current={activeView === 'explorer' ? 'page' : undefined}
          >
            Eksplorasi Dataset
          </button>
        </nav>

        <div className="health-pill" title="Status Layanan Data Backend">
          <span
            className={`status-dot ${health?.dataset_loaded ? '' : 'degraded'}`}
            aria-hidden="true"
          />
          <span>
            {health?.dataset_loaded
              ? `${health.total_jobs.toLocaleString()} Posisi Aktif`
              : 'Menghubungkan...'}
          </span>
        </div>
      </div>
    </header>
  )
}
