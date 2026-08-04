import { useState } from 'react'
import './App.css'

function App() {
  const [message, setMessage] = useState('Loading...')

  const testConnection = async () => {
    try {
      const response = await fetch('http://localhost:8000/health')
      const data = await response.json()
      setMessage(`Backend says: ${data.status}`)
    } catch (error) {
      setMessage(`Error: ${error.message}`)
    }
  }

  return (
    <div className="App">
      <h1>SkillMatch AI</h1>
      <button onClick={testConnection}>Test Backend Connection</button>
      <p>{message}</p>
    </div>
  )
}

export default App
