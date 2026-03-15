import { useState, useEffect } from 'react'
import { ResearchForm } from './components/ResearchForm'
import { ProgressTracker } from './components/ProgressTracker'
import { ResultDisplay } from './components/ResultDisplay'
import { AlertCircle } from 'lucide-react'

interface Citation {
  claim: string
  source_url: string
  source_title: string
}

function App() {
  const [isResearching, setIsResearching] = useState(false)
  const [currentStep, setCurrentStep] = useState('')
  const [messages, setMessages] = useState<string[]>([])
  const [summary, setSummary] = useState('')
  const [citations, setCitations] = useState<Citation[]>([])
  const [emailSent, setEmailSent] = useState(false)
  const [clientEmail, setClientEmail] = useState('')
  const [error, setError] = useState('')
  const [verified, setVerified] = useState(true)
  const [emailEnabled, setEmailEnabled] = useState(false)
  const [topic, setTopic] = useState('')

  // Fetch config on mount
  useEffect(() => {
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    fetch(`${apiUrl}/api/config`)
      .then(res => res.json())
      .then(data => setEmailEnabled(data.email_enabled))
      .catch(err => console.error('Failed to fetch config:', err))
  }, [])

  const handleResearch = async (topic: string, email: string) => {
    setIsResearching(true)
    setCurrentStep('planner')
    setMessages([])
    setSummary('')
    setCitations([])
    setEmailSent(false)
    setClientEmail(email)
    setTopic(topic)
    setError('')

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      const workflowId = `workflow-${Date.now()}`
      const url = `${apiUrl}/api/research/${workflowId}/stream?topic=${encodeURIComponent(topic)}&client_email=${encodeURIComponent(email || 'display@ui.local')}`

      const eventSource = new EventSource(url)

      eventSource.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)

          if (data.type === 'update') {
            setCurrentStep(data.step)
            if (data.messages && data.messages.length > 0) {
              setMessages(data.messages)
            }
          } else if (data.type === 'complete') {
            setSummary(data.summary || '')
            setCitations(data.citations || [])
            setEmailSent(data.email_sent || false)
            setVerified(data.verified !== false)  // Default to true if not specified
            setCurrentStep('complete')
            setIsResearching(false)
            eventSource.close()
          } else if (data.type === 'validation_error') {
            const errorMsg = data.suggestion 
              ? `${data.error}\n\nSuggestion: ${data.suggestion}`
              : data.error
            setError(errorMsg)
            setIsResearching(false)
            eventSource.close()
          } else if (data.type === 'error') {
            setError(data.error || 'An error occurred during research')
            setIsResearching(false)
            eventSource.close()
          }
        } catch (err) {
          console.error('Error parsing SSE data:', err)
        }
      }

      eventSource.onerror = () => {
        setError('Connection to server lost. Please try again.')
        setIsResearching(false)
        eventSource.close()
      }
    } catch (err) {
      setError('Failed to start research. Please check if the backend is running.')
      setIsResearching(false)
    }
  }

  const handleReset = () => {
    setIsResearching(false)
    setCurrentStep('')
    setMessages([])
    setSummary('')
    setCitations([])
    setEmailSent(false)
    setClientEmail('')
    setError('')
    setVerified(true)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4 md:p-8">
      <div className="max-w-5xl mx-auto">
        <div className="bg-white rounded-lg shadow-xl overflow-hidden">
          {/* Header */}
          <div className="bg-gradient-to-r from-blue-600 to-indigo-600 p-6 md:p-8">
            <h1 className="text-3xl md:text-4xl font-bold text-white mb-2">
              🔍 MCP Research Agent
            </h1>
            <p className="text-blue-100">
              AI-powered multi-agent research system using LangGraph and Model Context Protocol
            </p>
          </div>

          {/* Main Content */}
          <div className="p-6 md:p-8">
            {error && (
              <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4 flex items-start gap-3">
                <AlertCircle className="w-5 h-5 text-red-600 mt-0.5 flex-shrink-0" />
                <div className="flex-1">
                  <h3 className="font-semibold text-red-900">Error</h3>
                  <p className="text-sm text-red-700 mt-1">{error}</p>
                  <button
                    onClick={handleReset}
                    className="mt-2 text-sm text-red-600 hover:text-red-800 underline"
                  >
                    Try again
                  </button>
                </div>
              </div>
            )}

            {!isResearching && !summary && (
              <ResearchForm 
                onSubmit={handleResearch} 
                isLoading={isResearching}
                emailEnabled={emailEnabled}
              />
            )}

            {isResearching && (
              <div className="space-y-6">
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <h2 className="text-lg font-semibold text-blue-900 mb-4">
                    Research in Progress...
                  </h2>
                  <ProgressTracker
                    currentStep={currentStep}
                    messages={messages}
                    emailEnabled={!!clientEmail}
                  />
                </div>
              </div>
            )}

            {summary && (
              <div className="space-y-6">
                <ResultDisplay
                  summary={summary}
                  citations={citations}
                  emailSent={emailSent}
                  clientEmail={clientEmail}
                  verified={verified}
                  emailEnabled={emailEnabled}
                  topic={topic}
                />
                <button
                  onClick={handleReset}
                  className="w-full bg-gray-100 hover:bg-gray-200 text-gray-700 font-semibold py-3 px-6 rounded-lg transition-colors"
                >
                  Start New Research
                </button>
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="mt-6 text-center text-sm text-gray-600">
          <p>Powered by Claude Sonnet 4, LangGraph, LangSmith, Brave Search, and Model Context Protocol</p>
        </div>
      </div>
    </div>
  )
}

export default App
