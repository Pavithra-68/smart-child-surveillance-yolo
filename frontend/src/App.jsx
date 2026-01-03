import React, { useState, useEffect } from 'react'

function App() {
  const [status, setStatus] = useState("Checking...")

  // Ping the Python backend to see if it's alive
  useEffect(() => {
    fetch('http://localhost:5000/status')
      .then(res => res.json())
      .then(data => setStatus(data.status))
      .catch(() => setStatus("OFFLINE"))
  }, [])

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-slate-950 p-6">
      <h1 className="text-3xl font-bold text-cyan-400 mb-8">GuardianAI Monitoring</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 max-w-6xl w-full">
        {/* The Live Video Feed */}
        <div className="lg:col-span-2 bg-black rounded-3xl border-4 border-slate-800 overflow-hidden shadow-2xl">
           <img 
            src="http://localhost:5000/video_feed" 
            className="w-full aspect-video object-cover" 
            alt="Safety Feed" 
           />
        </div>

        {/* Status Sidebar */}
        <div className="bg-slate-900 p-6 rounded-3xl border border-slate-800 shadow-xl">
          <h2 className="text-xl font-semibold text-slate-300 mb-4">System Status</h2>
          <div className="space-y-4">
            <div className="flex justify-between items-center bg-slate-800 p-3 rounded-xl">
              <span className="text-slate-400">AI Engine</span>
              <span className="text-green-400 font-bold">{status}</span>
            </div>
            <button className="w-full bg-red-600 hover:bg-red-500 text-white py-3 rounded-xl font-bold transition-all">
              MUTE ALERTS
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App