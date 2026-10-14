import React from 'react'

export const Footer: React.FC = () => {
  return (
    <footer className="app-footer" role="contentinfo">
      <div className="container footer-inner">
        <div>
          <strong>Sumber Data:</strong> Job Skill Set oleh Batuhan Mutlu (2024), bersumber dari LinkedIn Job Postings oleh Arshkon di Kaggle via RecAI API.
        </div>
        <div>
          Lisensi: <a href="https://creativecommons.org/licenses/by-sa/4.0/" target="_blank" rel="noreferrer" style={{ color: 'inherit', textDecoration: 'underline' }}>CC BY-SA 4.0</a>. Skor kecocokan adalah indikator keselarasan kata kunci keahlian, bukan jaminan penerimaan kerja.
        </div>
      </div>
    </footer>
  )
}
