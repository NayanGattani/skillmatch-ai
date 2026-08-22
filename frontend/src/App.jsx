import { useState } from 'react'
import { Upload, X, ArrowRight } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import './index.css'
import './App.css'

function App() {
  const [file, setFile] = useState(null)
  const [jobDescription, setJobDescription] = useState('')
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [dragging, setDragging] = useState(false)

  const analyzeResume = async () => {
    setError(null)
    setLoading(true)

    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('job_description', jobDescription)

      const response = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        body: formData
      })

      const data = await response.json()
      if (data.success) {
        setResults(data)
      } else {
        setError(data.error || 'Analysis failed')
      }
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleDragOver = (e) => {
    e.preventDefault()
    setDragging(true)
  }

  const handleDragLeave = () => {
    setDragging(false)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setDragging(false)
    if (e.dataTransfer.files[0]) setFile(e.dataTransfer.files[0])
  }

  return (
    <div className="app">
      <header className="header">
        <div className="container">
          <div className="nav">
            <div className="brand">
              SkillMatch<span className="lime-accent">.</span>AI
            </div>
            <button className="test-btn">Test Connection</button>
          </div>
        </div>
      </header>

      <main>
        <AnimatePresence mode="wait">
          {!results ? (
            <UploadView
              file={file}
              setFile={setFile}
              jobDescription={jobDescription}
              setJobDescription={setJobDescription}
              loading={loading}
              error={error}
              onAnalyze={analyzeResume}
              dragging={dragging}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
            />
          ) : (
            <ResultsView
              results={results}
              onNewAnalysis={() => {
                setResults(null)
                setFile(null)
                setJobDescription('')
                setError(null)
              }}
            />
          )}
        </AnimatePresence>
      </main>
    </div>
  )
}

function UploadView({
  file,
  setFile,
  jobDescription,
  setJobDescription,
  loading,
  error,
  onAnalyze,
  dragging,
  onDragOver,
  onDragLeave,
  onDrop
}) {
  const canAnalyze = file && jobDescription.trim() && !loading

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="upload-view"
    >
      {/* Hero */}
      <section className="hero">
        <div className="hero-artifacts">
          <div className="artifact artifact-1">
            <div className="artifact-content">
              <div>
                <p className="artifact-label">Score</p>
                <p className="artifact-value">78.5%</p>
              </div>
              <div className="artifact-accent" />
            </div>
          </div>

          <div className="artifact artifact-2">
            <div className="artifact-content">
              <div>
                <p className="artifact-label">Matched</p>
                <p className="artifact-value">7 / 9</p>
              </div>
              <div className="artifact-accent" />
            </div>
          </div>

          <div className="artifact artifact-3">
            <div className="artifact-content">
              <div>
                <p className="artifact-label">Gap</p>
                <p className="artifact-value">2 Skills</p>
              </div>
              <div className="artifact-accent" />
            </div>
          </div>
        </div>

        <div className="container">
          <div className="hero-content">
            <p className="eyebrow">RESUME × JOB MATCHING</p>
            <h1 className="display-1">KNOW WHERE<br />YOU STAND.</h1>
            <p className="hero-subtext">
              Upload a resume. Add a job description.<br />
              Get a weighted match score, skill gaps, and<br />
              AI-powered recommendations.
            </p>
          </div>
        </div>
      </section>

      {/* Workspace */}
      <section className="workspace">
        <div className="container">
          {/* Section Headers */}
          <div className="workspace-header">
            <div className="section-intro">
              <div className="section-number">01</div>
              <div className="section-intro-content">
                <h3>Your Resume</h3>
                <p>PDF file. Upload to extract text and identify skills.</p>
              </div>
            </div>
            <div className="section-intro">
              <div className="section-number">02</div>
              <div className="section-intro-content">
                <h3>The Opportunity</h3>
                <p>Paste the job description. We'll parse required and preferred skills.</p>
              </div>
            </div>
          </div>

          {/* Upload Grid */}
          <div className="workspace-grid">
            {/* Resume Upload */}
            <div className="upload-section">
              <div
                className={`upload-zone ${dragging ? 'dragging' : ''} ${file ? 'has-file' : ''}`}
                onDragOver={onDragOver}
                onDragLeave={onDragLeave}
                onDrop={onDrop}
              >
                {file ? (
                  <div className="file-state">
                    <div className="file-info">
                      <svg className="file-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z" />
                        <polyline points="13 2 13 9 20 9" />
                      </svg>
                      <div>
                        <div className="file-name">{file.name}</div>
                        <div className="file-size">{(file.size / 1024 / 1024).toFixed(2)} MB</div>
                      </div>
                    </div>
                    <button
                      className="remove-file"
                      onClick={() => setFile(null)}
                      disabled={loading}
                    >
                      <X size={16} />
                    </button>
                  </div>
                ) : (
                  <div className="upload-placeholder">
                    <input
                      type="file"
                      accept=".pdf"
                      onChange={(e) => e.target.files[0] && setFile(e.target.files[0])}
                      id="pdf-input"
                      disabled={loading}
                      className="file-input"
                    />
                    <label htmlFor="pdf-input" className="upload-label">
                      <Upload size={28} />
                      <p>DROP YOUR RESUME HERE</p>
                      <p className="upload-hint">or click to select • PDF • Max 10MB</p>
                    </label>
                  </div>
                )}
              </div>
            </div>

            {/* Job Description */}
            <div className="jd-section">
              <textarea
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                placeholder="Paste the job description here..."
                disabled={loading}
                className="jd-input"
              />
              <div className="char-count">{jobDescription.length} characters</div>
            </div>
          </div>

          {/* Error */}
          {error && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              className="error-message"
            >
              {error}
            </motion.div>
          )}

          {/* Analyze */}
          <div className="analyze-section">
            <button
              onClick={onAnalyze}
              disabled={!canAnalyze}
              className={`analyze-button ${loading ? 'loading' : ''}`}
            >
              {loading ? (
                <>
                  <span className="spinner" />
                  ANALYZING
                </>
              ) : (
                <>
                  ANALYZE MATCH
                  <ArrowRight size={14} />
                </>
              )}
            </button>
          </div>
        </div>
      </section>
    </motion.div>
  )
}

function ResultsView({ results, onNewAnalysis }) {
  const score = results.scoring.ats_score
  const req = results.scoring.required
  const pref = results.scoring.preferred
  const ai = results.ai_analysis

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="results-view"
    >
      {/* Header */}
      <header className="results-header">
        <div className="container">
          <button className="back-button" onClick={onNewAnalysis}>
            ← NEW ANALYSIS
          </button>
        </div>
      </header>

      {/* Score */}
      <section className="score-section">
        <div className="container">
          <div className="score-display">
            <div className="score-main">
              <p className="text-meta">MATCH SCORE</p>
              <div className="score-number">{score}</div>
            </div>
            <div className="score-breakdown">
              <div className="breakdown-item">
                <p className="text-meta">REQUIRED</p>
                <div className="breakdown-value">{req.matched_count}/{req.total_count}</div>
              </div>
              <div className="breakdown-item">
                <p className="text-meta">PREFERRED</p>
                <div className="breakdown-value">{pref.matched_count}/{pref.total_count}</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Skills */}
      <section className="skills-section">
        <div className="container">
          <div className="skills-grid">
            <SkillColumn title="REQUIRED SKILLS" matched={req.matched} missing={req.missing} />
            <SkillColumn title="PREFERRED SKILLS" matched={pref.matched} missing={pref.missing} />
          </div>
        </div>
      </section>

      {/* AI */}
      {ai && (
        <section className="ai-section">
          <div className="container">
            <h2 className="heading-1">AI ASSESSMENT</h2>
            <div className="rule" />

            <div className="assessment-block">
              <h3>SUMMARY</h3>
              <p className="text-body">{ai.summary}</p>
            </div>

            <div className="two-column">
              <div className="assessment-block">
                <h3>STRENGTHS</h3>
                <ol className="assessment-list">
                  {ai.strengths.map((s, i) => (
                    <li key={i}>
                      <span className="list-num">{String(i + 1).padStart(2, '0')}</span>
                      <span>{s}</span>
                    </li>
                  ))}
                </ol>
              </div>
              <div className="assessment-block">
                <h3>AREAS TO IMPROVE</h3>
                <ol className="assessment-list">
                  {ai.weaknesses.map((w, i) => (
                    <li key={i}>
                      <span className="list-num">{String(i + 1).padStart(2, '0')}</span>
                      <span>{w}</span>
                    </li>
                  ))}
                </ol>
              </div>
            </div>

            <div className="two-column">
              <div className="assessment-block">
                <h3>EXPERIENCE RELEVANCE</h3>
                <p className="text-body">{ai.experience_relevance}</p>
              </div>
              <div className="assessment-block">
                <h3>SKILL GAP ANALYSIS</h3>
                <p className="text-body">{ai.skill_gap_analysis}</p>
              </div>
            </div>

            <div className="assessment-block">
              <h3>RECOMMENDATIONS</h3>
              <ol className="assessment-list lime-accent-list">
                {ai.recommendations.map((r, i) => (
                  <li key={i}>
                    <span className="list-num">{String(i + 1).padStart(2, '0')}</span>
                    <span>{r}</span>
                  </li>
                ))}
              </ol>
            </div>
          </div>
        </section>
      )}
    </motion.div>
  )
}

function SkillColumn({ title, matched, missing }) {
  return (
    <div className="skill-column">
      <h3>{title}</h3>
      {matched.length > 0 && (
        <div className="skill-group">
          <p className="skill-label">MATCHED ({matched.length})</p>
          <div className="skill-tags">
            {matched.map(s => (
              <span key={s} className="skill-tag matched">✓ {s}</span>
            ))}
          </div>
        </div>
      )}
      {missing.length > 0 && (
        <div className="skill-group">
          <p className="skill-label">MISSING ({missing.length})</p>
          <div className="skill-tags">
            {missing.map(s => (
              <span key={s} className="skill-tag missing">× {s}</span>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default App