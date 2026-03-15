import { useState } from 'react'
import { Loader2 } from 'lucide-react'

interface ResearchFormProps {
  onSubmit: (topic: string, email: string) => void
  isLoading: boolean
  emailEnabled?: boolean
}

export function ResearchForm({ onSubmit, isLoading, emailEnabled = false }: ResearchFormProps) {
  const [topic, setTopic] = useState('')
  const [email, setEmail] = useState('')
  const [errors, setErrors] = useState<{ topic?: string; email?: string }>({})

  const validateForm = () => {
    const newErrors: { topic?: string; email?: string } = {}

    if (!topic || topic.length < 10) {
      newErrors.topic = 'Topic must be at least 10 characters'
    }
    if (topic.length > 500) {
      newErrors.topic = 'Topic must be less than 500 characters'
    }

    if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      newErrors.email = 'Please enter a valid email address'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (validateForm()) {
      onSubmit(topic, email)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <label htmlFor="topic" className="block text-sm font-medium text-gray-700 mb-2">
          Research Topic *
        </label>
        <textarea
          id="topic"
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          placeholder="Enter a topic to research (e.g., 'Latest developments in quantum computing')"
          className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none ${
            errors.topic ? 'border-red-500' : 'border-gray-300'
          }`}
          rows={4}
          disabled={isLoading}
        />
        {errors.topic && (
          <p className="mt-1 text-sm text-red-600">{errors.topic}</p>
        )}
        <p className="mt-1 text-sm text-gray-500">
          {topic.length}/500 characters
        </p>
      </div>

      {emailEnabled && (
        <div>
          <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
            Client Email (Optional)
          </label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="client@example.com"
            className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
              errors.email ? 'border-red-500' : 'border-gray-300'
            }`}
            disabled={isLoading}
          />
          {errors.email && (
            <p className="mt-1 text-sm text-red-600">{errors.email}</p>
          )}
          <p className="mt-1 text-sm text-gray-500">
            {email ? 'Research will be sent to this email' : 'Leave empty to display results here'}
          </p>
        </div>
      )}

      <button
        type="submit"
        disabled={isLoading}
        className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-semibold py-3 px-6 rounded-lg transition-colors flex items-center justify-center gap-2"
      >
        {isLoading ? (
          <>
            <Loader2 className="w-5 h-5 animate-spin" />
            Researching...
          </>
        ) : (
          'Start Research'
        )}
      </button>
    </form>
  )
}
