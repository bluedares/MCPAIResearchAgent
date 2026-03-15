# 📦 Data Models & Schemas

Complete data model documentation for the MCP Research Agent.

---

## 🔄 **State Models**

### **ResearchState**

The main state object that flows through the LangGraph workflow.

```python
from typing import TypedDict, Optional, List, Dict

class ResearchState(TypedDict):
    """Complete workflow state."""
    
    # Input
    topic: str                          # Research topic
    client_email: str                   # Email or "display@ui.local"
    
    # Planning
    research_plan: Optional[Dict]       # Research strategy
    sub_queries: List[str]              # 3-5 sub-queries
    
    # Retrieval
    raw_data: List[Dict]                # Search results
    sources: List[str]                  # Unique URLs
    
    # Summarization
    summary: str                        # Final summary
    key_findings: List[str]             # Key findings
    citations: List[Dict]               # Citations
    
    # Verification
    verification_status: str            # "pass" or "fail"
    verification_confidence: float      # 0.0-1.0
    verification_feedback: str          # Feedback text
    verified: bool                      # True if passed
    
    # Delivery
    final_output: str                   # Formatted output
    email_sent: bool                    # Email sent flag
    email_timestamp: Optional[str]      # ISO timestamp
    
    # Metadata
    workflow_id: str                    # Unique workflow ID
    current_step: str                   # Current agent
    errors: List[str]                   # Error messages
    retry_count: int                    # Retry counter
    status_messages: List[str]          # Status updates
```

**Example:**
```json
{
  "topic": "Latest AI developments",
  "client_email": "display@ui.local",
  "research_plan": {
    "strategy": "Multi-faceted AI research",
    "key_areas": ["LLMs", "Applications", "Ethics"]
  },
  "sub_queries": [
    "Latest LLM breakthroughs 2026",
    "AI applications in healthcare"
  ],
  "raw_data": [...],
  "sources": ["https://..."],
  "summary": "AI has experienced...",
  "citations": [...],
  "verification_status": "pass",
  "verified": true,
  "workflow_id": "workflow-1234567890",
  "current_step": "complete",
  "retry_count": 0
}
```

---

## 📝 **Request Models**

### **ResearchRequest**

Request to start a research workflow.

```python
from pydantic import BaseModel, EmailStr, Field

class ResearchRequest(BaseModel):
    """Research request model."""
    
    topic: str = Field(
        ...,
        min_length=10,
        max_length=500,
        description="Research topic"
    )
    
    client_email: EmailStr = Field(
        ...,
        description="Client email address"
    )
```

**Example:**
```json
{
  "topic": "Latest developments in quantum computing",
  "client_email": "user@example.com"
}
```

**Validation:**
- `topic`: 10-500 characters
- `client_email`: Valid email format

---

### **SendEmailRequest**

Request to send research results via email.

```python
class SendEmailRequest(BaseModel):
    """Send email request model."""
    
    email: EmailStr = Field(
        ...,
        description="Recipient email address"
    )
    
    topic: str = Field(
        ...,
        description="Research topic"
    )
    
    summary: str = Field(
        ...,
        description="Research summary"
    )
    
    citations: list = Field(
        default=[],
        description="Citations"
    )
```

**Example:**
```json
{
  "email": "user@example.com",
  "topic": "Latest AI developments",
  "summary": "Artificial intelligence has...",
  "citations": [
    {
      "claim": "GPT-5 released",
      "source_url": "https://...",
      "source_title": "OpenAI News"
    }
  ]
}
```

---

## 📤 **Response Models**

### **ConfigResponse**

Configuration response with feature flags.

```python
class ConfigResponse(BaseModel):
    """Configuration response model."""
    
    email_enabled: bool
```

**Example:**
```json
{
  "email_enabled": false
}
```

---

### **ResearchResponse**

Response when starting a research workflow.

```python
class ResearchResponse(BaseModel):
    """Research response model."""
    
    workflow_id: str
    status: str
    message: str
```

**Example:**
```json
{
  "workflow_id": "workflow-1234567890",
  "status": "started",
  "message": "Research workflow started for topic: Latest AI"
}
```

---

## 🤖 **Agent Models**

### **TopicValidation**

Topic validation result.

```python
class TopicValidation(BaseModel):
    """Topic validation result."""
    
    is_valid: bool = Field(
        description="Whether the topic is valid for research"
    )
    
    reason: str = Field(
        description="Reason for validation decision"
    )
    
    suggestion: str = Field(
        default="",
        description="Suggestion for improvement if invalid"
    )
```

**Example (Invalid):**
```json
{
  "is_valid": false,
  "reason": "This appears to be a personal question about your identity",
  "suggestion": "Try asking about 'History of identity verification systems'"
}
```

**Example (Valid):**
```json
{
  "is_valid": true,
  "reason": "This is a valid research topic about current technology",
  "suggestion": ""
}
```

---

### **ResearchPlan**

Research planning output.

```python
class ResearchPlan(BaseModel):
    """Research plan model."""
    
    strategy: str = Field(
        description="Overall research strategy"
    )
    
    key_areas: List[str] = Field(
        description="Key areas to cover"
    )
    
    approach: str = Field(
        description="Research approach"
    )
    
    sub_queries: List[str] = Field(
        min_items=3,
        max_items=5,
        description="Specific sub-queries"
    )
```

**Example:**
```json
{
  "strategy": "Multi-faceted quantum computing research",
  "key_areas": [
    "Hardware developments",
    "Algorithm innovations",
    "Industry applications"
  ],
  "approach": "Comprehensive coverage of technical and business aspects",
  "sub_queries": [
    "Quantum computing breakthroughs 2026",
    "Latest quantum algorithms",
    "Quantum hardware advances",
    "Industry quantum adoption",
    "Future quantum research"
  ]
}
```

---

### **Citation**

Citation model for research sources.

```python
class Citation(BaseModel):
    """Citation model."""
    
    claim: str = Field(
        description="Claim being cited"
    )
    
    source_url: str = Field(
        description="Source URL"
    )
    
    source_title: str = Field(
        description="Source title"
    )
```

**Example:**
```json
{
  "claim": "IBM announced 1000-qubit quantum processor",
  "source_url": "https://techcrunch.com/ibm-quantum-1000",
  "source_title": "IBM Unveils 1000-Qubit Quantum Processor"
}
```

---

### **ResearchSummary**

Summarization output.

```python
class ResearchSummary(BaseModel):
    """Research summary model."""
    
    summary: str = Field(
        min_length=300,
        max_length=2000,
        description="Comprehensive summary"
    )
    
    key_findings: List[str] = Field(
        default=[],
        description="Key findings"
    )
    
    citations: List[Citation] = Field(
        default=[],
        description="Citations"
    )
```

**Example:**
```json
{
  "summary": "Quantum computing has experienced significant progress in 2026...",
  "key_findings": [
    "IBM announced 1000-qubit processor",
    "Google achieved quantum advantage",
    "New error correction techniques"
  ],
  "citations": [
    {
      "claim": "IBM announced 1000-qubit processor",
      "source_url": "https://techcrunch.com/...",
      "source_title": "IBM Quantum Breakthrough"
    }
  ]
}
```

---

### **VerificationResult**

Verification output.

```python
class VerificationResult(BaseModel):
    """Verification result model."""
    
    status: str = Field(
        description="Verification status: pass or fail"
    )
    
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence score"
    )
    
    issues_found: List[str] = Field(
        default=[],
        description="Issues found during verification"
    )
    
    feedback: str = Field(
        description="Verification feedback"
    )
```

**Example (Pass):**
```json
{
  "status": "pass",
  "confidence": 0.85,
  "issues_found": [],
  "feedback": "Summary is accurate and well-cited"
}
```

**Example (Fail):**
```json
{
  "status": "fail",
  "confidence": 0.45,
  "issues_found": [
    "Missing citation for claim about quantum advantage",
    "Unclear source for hardware statistics"
  ],
  "feedback": "Some claims lack proper citations"
}
```

---

## 📡 **SSE Event Models**

### **Start Event**

```typescript
interface StartEvent {
  type: 'start'
  workflow_id: string
  from_cache?: boolean
}
```

### **Update Event**

```typescript
interface UpdateEvent {
  type: 'update'
  step: string
  messages: string[]
}
```

### **Complete Event**

```typescript
interface CompleteEvent {
  type: 'complete'
  summary: string
  citations: Citation[]
  email_sent: boolean
  verified: boolean
  verification_status: string
  verification_confidence: number
  from_cache?: boolean
}
```

### **Validation Error Event**

```typescript
interface ValidationErrorEvent {
  type: 'validation_error'
  error: string
  suggestion: string
}
```

### **Error Event**

```typescript
interface ErrorEvent {
  type: 'error'
  error: string
}
```

---

## 🔍 **Search Result Models**

### **TavilySearchResult**

```python
class TavilySearchResult(TypedDict):
    """Tavily search result."""
    
    query: str              # Original query
    title: str              # Article title
    url: str                # Article URL
    content: str            # Article content
    score: float            # Relevance score (0.0-1.0)
    published_date: str     # Publication date (optional)
```

**Example:**
```json
{
  "query": "Latest AI developments",
  "title": "GPT-5 Released with Multimodal Capabilities",
  "url": "https://techcrunch.com/gpt5-release",
  "content": "OpenAI has announced GPT-5...",
  "score": 0.95,
  "published_date": "2026-01-15"
}
```

---

## 💾 **Cache Models**

### **CachedResearch**

```python
class CachedResearch(TypedDict):
    """Cached research result."""
    
    summary: str
    citations: List[Dict]
    verified: bool
    cached_at: str          # ISO timestamp
    ttl: int                # Time to live in seconds
```

**Example:**
```json
{
  "summary": "Quantum computing has...",
  "citations": [...],
  "verified": true,
  "cached_at": "2026-03-12T20:00:00Z",
  "ttl": 86400
}
```

---

## 🎯 **Frontend Models**

### **Citation (TypeScript)**

```typescript
interface Citation {
  claim: string
  source_url: string
  source_title: string
}
```

### **ResearchFormProps**

```typescript
interface ResearchFormProps {
  onSubmit: (topic: string, email: string) => void
  isLoading: boolean
  emailEnabled?: boolean
}
```

### **ResultDisplayProps**

```typescript
interface ResultDisplayProps {
  summary: string
  citations: Citation[]
  emailSent: boolean
  clientEmail?: string
  verified?: boolean
  emailEnabled?: boolean
  topic?: string
}
```

---

## 📊 **Validation Rules**

### **Topic Validation**

```python
# Length
min_length = 10
max_length = 500

# Pattern
allowed_characters = "alphanumeric + spaces + punctuation"

# Content
must_not_be = [
    "personal_question",
    "too_vague",
    "non_researchable",
    "inappropriate"
]
```

### **Email Validation**

```python
# Format
pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'

# Examples
valid = [
    "user@example.com",
    "test.user@domain.co.uk"
]

invalid = [
    "invalid",
    "@example.com",
    "user@"
]
```

---

## 🔄 **State Transitions**

```
Initial → Planning → Retrieval → Summarization → Verification → Delivery
   ↓         ↓           ↓             ↓              ↓            ↓
Empty    Plan Set   Data Set    Summary Set    Verified    Complete
```

**State Fields by Step:**

| Step | Fields Added |
|------|-------------|
| Initial | `topic`, `client_email`, `workflow_id` |
| Planning | `research_plan`, `sub_queries` |
| Retrieval | `raw_data`, `sources` |
| Summarization | `summary`, `citations` |
| Verification | `verification_status`, `verified` |
| Delivery | `email_sent`, `final_output` |

---

## 📚 **Related Documentation**

- [API Endpoints](./ENDPOINTS.md) - API reference
- [Architecture](../architecture/OVERVIEW.md) - System design
- [Workflow Guide](../guides/WORKFLOW_GUIDE.md) - Workflow details

---

**Schema Version:** 1.0.0  
**Last Updated:** March 2026
