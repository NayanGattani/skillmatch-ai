import { useState } from 'react'
import './App.css'

function App() {
  const [message, setMessage] = useState('')
  const [file, setFile] = useState(null)
  const [jobDescription, setJobDescription] = useState('')
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)

  const testConnection = async () => {
    try {
      const response = await fetch('http://localhost:8000/health')
      const data = await response.json()
      setMessage(`✅ Backend says: ${data.status}`)
    } catch (error) {
      setMessage(`❌ Error: ${error.message}`)
    }
  }

  const analyzeResume = async () => {
    if (!file) {
      setMessage('❌ Please select a resume file')
      return
    }

    if (!jobDescription.trim()) {
      setMessage('❌ Please enter a job description')
      return
    }

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
        setMessage('✅ Resume analyzed successfully')
      } else {
        setMessage(`❌ Error: ${data.error}`)
      }
    } catch (error) {
      setMessage(`❌ Error: ${error.message}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="App">
      <h1>🎯 SkillMatch AI</h1>
      <p>Analyze your resume against job descriptions</p>
      
      <hr />

      {/* Connection Test */}
      <div style={{ marginBottom: '20px' }}>
        <button onClick={testConnection}>Test Connection</button>
      </div>

      {/* Input Section */}
      <div style={{ border: '1px solid #ddd', padding: '20px', borderRadius: '8px', marginBottom: '20px' }}>
        <h3>Step 1: Upload Resume</h3>
        <input 
          type="file" 
          accept=".pdf"
          onChange={(e) => setFile(e.target.files[0])}
        />
        {file && <p>✅ Selected: {file.name}</p>}

        <h3 style={{ marginTop: '20px' }}>Step 2: Paste Job Description</h3>
        <textarea
          placeholder="Paste the job description here..."
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
          style={{ 
            width: '100%', 
            height: '150px', 
            padding: '10px',
            fontSize: '14px',
            fontFamily: 'monospace'
          }}
        />

        <button 
          onClick={analyzeResume}
          disabled={loading}
          style={{ marginTop: '10px', fontSize: '16px', padding: '10px 20px' }}
        >
          {loading ? 'Analyzing...' : 'Analyze Resume'}
        </button>
      </div>

      {/* Message Display */}
      {message && (
        <div style={{ 
          padding: '10px', 
          marginBottom: '20px',
          backgroundColor: message.includes('✅') ? '#d4edda' : '#f8d7da',
          color: message.includes('✅') ? '#155724' : '#721c24',
          borderRadius: '4px'
        }}>
          {message}
        </div>
      )}

      {/* Results Section */}
      {results && (
        <div style={{ border: '1px solid #007bff', padding: '20px', borderRadius: '8px', marginTop: '20px' }}>
          <h2>📊 Analysis Results</h2>

          {/* ATS Score */}
          <div style={{ 
            fontSize: '24px', 
            fontWeight: 'bold',
            marginBottom: '20px',
            padding: '15px',
            backgroundColor: '#f0f0f0',
            borderRadius: '8px',
            textAlign: 'center'
          }}>
            ATS Score: <span style={{ color: results.ats_score >= 70 ? '#28a745' : results.ats_score >= 50 ? '#ffc107' : '#dc3545' }}>
              {results.ats_score}%
            </span>
          </div>

          {/* Match Summary */}
          <p style={{ fontSize: '16px', marginBottom: '15px' }}>
            Matched <strong>{results.matched_skills.length}</strong> out of <strong>{results.job_skills.length}</strong> required skills
          </p>

          {/* Matched Skills */}
          <div style={{ marginBottom: '20px' }}>
            <h4>✅ Matched Skills ({results.matched_skills.length}):</h4>
            <p style={{ color: '#28a745', fontSize: '14px', lineHeight: '1.6' }}>
              {results.matched_skills.length > 0 ? results.matched_skills.join(', ') : 'None'}
            </p>
          </div>

          {/* Missing Skills */}
          <div style={{ marginBottom: '20px' }}>
            <h4>❌ Missing Skills ({results.missing_skills.length}):</h4>
            <p style={{ color: '#dc3545', fontSize: '14px', lineHeight: '1.6' }}>
              {results.missing_skills.length > 0 ? results.missing_skills.join(', ') : 'None'}
            </p>
          </div>

          {/* Extracted Text */}
          <details>
            <summary style={{ cursor: 'pointer', fontWeight: 'bold', marginTop: '15px' }}>
              📄 View Extracted Resume Text
            </summary>
            <textarea 
              value={results.text} 
              readOnly 
              style={{ 
                width: '100%', 
                height: '300px',
                marginTop: '10px',
                padding: '10px',
                fontFamily: 'monospace',
                fontSize: '12px'
              }}
            />
          </details>
        </div>
      )}
    </div>
  )
}

export default App