import { useState } from 'react'
import { Copy, Check, Mail, FileText, Send, Loader2 } from 'lucide-react'

interface Citation {
  claim: string
  source_url: string
  source_title: string
}

interface ResultDisplayProps {
  summary: string
  citations: Citation[]
  emailSent: boolean
  clientEmail?: string
  verified?: boolean
  emailEnabled?: boolean
  topic?: string
}

export function ResultDisplay({ summary, citations, emailSent, clientEmail, verified = true, emailEnabled = false, topic = '' }: ResultDisplayProps) {
  const [copied, setCopied] = useState(false)
  const [email, setEmail] = useState('')
  const [sending, setSending] = useState(false)
  const [sendSuccess, setSendSuccess] = useState(false)
  const [sendError, setSendError] = useState('')

  const handleCopy = () => {
    navigator.clipboard.writeText(summary)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const handleSendEmail = async () => {
    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      setSendError('Please enter a valid email address')
      return
    }

    setSending(true)
    setSendError('')
    setSendSuccess(false)

    try {
      const apiUrl = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/$/, '')
      const response = await fetch(`${apiUrl}/api/send-email`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
          topic,
          summary,
          citations,
        }),
      })

      const data = await response.json()

      if (response.ok && data.success) {
        setSendSuccess(true)
        setEmail('')
        setTimeout(() => setSendSuccess(false), 5000)
      } else {
        setSendError(data.message || 'Failed to send email')
      }
    } catch (error) {
      setSendError('Network error. Please try again.')
    } finally {
      setSending(false)
    }
  }

  return (
    <div className="space-y-6">
      {emailSent && clientEmail && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-4 flex items-start gap-3">
          <Mail className="w-5 h-5 text-green-600 mt-0.5" />
          <div>
            <h3 className="font-semibold text-green-900">Email Sent Successfully!</h3>
            <p className="text-sm text-green-700 mt-1">
              Research summary has been sent to <strong>{clientEmail}</strong>
            </p>
          </div>
        </div>
      )}

      <div className="bg-white border border-gray-200 rounded-lg p-6">
        {!verified && (
          <div className="mb-4 bg-yellow-50 border border-yellow-200 rounded-lg p-3 flex items-center gap-2">
            <span className="text-yellow-600 font-semibold">⚠️ Not Verified</span>
            <span className="text-sm text-yellow-700">
              This summary could not be fully verified. Please review carefully.
            </span>
          </div>
        )}
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold text-gray-900 flex items-center gap-2">
            <FileText className="w-5 h-5" />
            Research Summary
            {verified && <span className="text-sm text-green-600 font-normal ml-2">✓ Verified</span>}
          </h2>
          <button
            onClick={handleCopy}
            className="flex items-center gap-2 px-3 py-2 text-sm bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
          >
            {copied ? (
              <>
                <Check className="w-4 h-4 text-green-600" />
                Copied!
              </>
            ) : (
              <>
                <Copy className="w-4 h-4" />
                Copy
              </>
            )}
          </button>
        </div>

        <div className="prose max-w-none">
          <div className="text-gray-700 whitespace-pre-wrap leading-relaxed">
            {summary}
          </div>
        </div>
      </div>

      {citations && citations.length > 0 && (
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <h3 className="text-lg font-bold text-gray-900 mb-4">
            📚 Citations ({citations.length})
          </h3>
          <div className="space-y-3">
            {citations.map((citation, idx) => (
              <div key={idx} className="border-l-4 border-blue-500 pl-4 py-2">
                <p className="text-sm text-gray-700 mb-1">{citation.claim}</p>
                <a
                  href={citation.source_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-sm text-blue-600 hover:text-blue-800 hover:underline"
                >
                  {citation.source_title || citation.source_url}
                </a>
              </div>
            ))}
          </div>
        </div>
      )}

      {emailEnabled && !emailSent && (
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
            <Mail className="w-5 h-5" />
            Send Results via Email
          </h3>
          
          {sendSuccess && (
            <div className="mb-4 bg-green-50 border border-green-200 rounded-lg p-3 flex items-center gap-2">
              <Check className="w-5 h-5 text-green-600" />
              <span className="text-sm text-green-700">
                Email sent successfully to <strong>{email}</strong>
              </span>
            </div>
          )}

          <div className="flex gap-3">
            <input
              type="email"
              value={email}
              onChange={(e) => {
                setEmail(e.target.value)
                setSendError('')
              }}
              placeholder="recipient@example.com"
              className={`flex-1 px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                sendError ? 'border-red-500' : 'border-gray-300'
              }`}
              disabled={sending}
            />
            <button
              onClick={handleSendEmail}
              disabled={sending || !email}
              className="px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-semibold rounded-lg transition-colors flex items-center gap-2"
            >
              {sending ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Sending...
                </>
              ) : (
                <>
                  <Send className="w-5 h-5" />
                  Send
                </>
              )}
            </button>
          </div>
          
          {sendError && (
            <p className="mt-2 text-sm text-red-600">{sendError}</p>
          )}
          
          <p className="mt-2 text-sm text-gray-500">
            The complete research summary and citations will be sent to the provided email address.
          </p>
        </div>
      )}

      {emailEnabled && !emailSent && (
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
            <Mail className="w-5 h-5" />
            Send Results via Email
          </h3>
          
          {sendSuccess && (
            <div className="mb-4 bg-green-50 border border-green-200 rounded-lg p-3 flex items-center gap-2">
              <Check className="w-5 h-5 text-green-600" />
              <span className="text-sm text-green-700">
                Email sent successfully!
              </span>
            </div>
          )}

          <div className="flex gap-3">
            <input
              type="email"
              value={email}
              onChange={(e) => {
                setEmail(e.target.value)
                setSendError('')
              }}
              placeholder="recipient@example.com"
              className={`flex-1 px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                sendError ? 'border-red-500' : 'border-gray-300'
              }`}
              disabled={sending}
            />
            <button
              onClick={handleSendEmail}
              disabled={sending || !email}
              className="px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-semibold rounded-lg transition-colors flex items-center gap-2"
            >
              {sending ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Sending...
                </>
              ) : (
                <>
                  <Send className="w-5 h-5" />
                  Send
                </>
              )}
            </button>
          </div>
          
          {sendError && (
            <p className="mt-2 text-sm text-red-600">{sendError}</p>
          )}
          
          <p className="mt-2 text-sm text-gray-500">
            The complete research summary and citations will be sent to the provided email address.
          </p>
        </div>
      )}
    </div>
  )
}
