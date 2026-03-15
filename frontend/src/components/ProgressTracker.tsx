import { CheckCircle2, Circle, Loader2 } from 'lucide-react'

interface Stage {
  id: string
  label: string
  icon: string
}

const stages: Stage[] = [
  { id: 'planner', label: 'Planning', icon: '🧠' },
  { id: 'retriever', label: 'Researching', icon: '🔍' },
  { id: 'summarizer', label: 'Summarizing', icon: '📝' },
  { id: 'verifier', label: 'Verifying', icon: '✅' },
  { id: 'email_sender', label: 'Sending Email', icon: '📧' },
]

interface ProgressTrackerProps {
  currentStep: string
  messages: string[]
  emailEnabled: boolean
}

export function ProgressTracker({ currentStep, messages, emailEnabled }: ProgressTrackerProps) {
  const getStageStatus = (stageId: string) => {
    if (!emailEnabled && stageId === 'email_sender') {
      return 'skipped'
    }

    const stageIndex = stages.findIndex((s) => s.id === stageId)
    const currentIndex = stages.findIndex((s) => s.id === currentStep)

    if (currentIndex === -1) return 'pending'
    if (stageIndex < currentIndex) return 'completed'
    if (stageIndex === currentIndex) return 'active'
    return 'pending'
  }

  const filteredStages = emailEnabled 
    ? stages 
    : stages.filter(s => s.id !== 'email_sender')

  return (
    <div className="space-y-6">
      <div className="space-y-3">
        {filteredStages.map((stage, index) => {
          const status = getStageStatus(stage.id)
          
          return (
            <div key={stage.id} className="flex items-center gap-3">
              <div className="flex-shrink-0">
                {status === 'completed' && (
                  <CheckCircle2 className="w-6 h-6 text-green-500" />
                )}
                {status === 'active' && (
                  <Loader2 className="w-6 h-6 text-blue-500 animate-spin" />
                )}
                {status === 'pending' && (
                  <Circle className="w-6 h-6 text-gray-300" />
                )}
                {status === 'skipped' && (
                  <Circle className="w-6 h-6 text-gray-200" />
                )}
              </div>
              
              <div className="flex-1">
                <div className={`font-medium ${
                  status === 'completed' ? 'text-green-700' :
                  status === 'active' ? 'text-blue-700' :
                  status === 'skipped' ? 'text-gray-400' :
                  'text-gray-500'
                }`}>
                  <span className="mr-2">{stage.icon}</span>
                  {stage.label}
                </div>
              </div>

              {index < filteredStages.length - 1 && (
                <div className={`w-px h-8 -my-2 ml-3 ${
                  status === 'completed' ? 'bg-green-300' : 'bg-gray-200'
                }`} />
              )}
            </div>
          )
        })}
      </div>

      {messages.length > 0 && (
        <div className="mt-6 p-4 bg-gray-50 rounded-lg border border-gray-200">
          <h3 className="text-sm font-semibold text-gray-700 mb-2">Status Updates</h3>
          <div className="space-y-1 max-h-40 overflow-y-auto">
            {messages.slice(-5).map((msg, idx) => (
              <p key={idx} className="text-sm text-gray-600">
                {msg}
              </p>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
