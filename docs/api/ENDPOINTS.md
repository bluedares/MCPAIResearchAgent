# 🔌 API Endpoints Reference

Complete API documentation for the MCP Research Agent backend.

---

## 📋 **Base URL**

```
http://localhost:8000
```

---

## 🔑 **Authentication**

Currently no authentication required for local development.

**Future:** API keys or JWT tokens for production deployment.

---

## 📡 **Endpoints**

### **1. Get Configuration**

Get application configuration including feature flags.

**Endpoint:** `GET /api/config`

**Request:**
```http
GET /api/config HTTP/1.1
Host: localhost:8000
```

**Response:**
```json
{
  "email_enabled": false
}
```

**Response Codes:**
- `200 OK` - Success

**Example:**
```bash
curl http://localhost:8000/api/config
```

**Frontend Usage:**
```typescript
const response = await fetch('http://localhost:8000/api/config')
const config = await response.json()
console.log(config.email_enabled) // false
```

---

### **2. Stream Research Workflow**

Execute research workflow with real-time progress updates via Server-Sent Events (SSE).

**Endpoint:** `GET /api/research/{workflow_id}/stream`

**Parameters:**
- `workflow_id` (path) - Unique workflow identifier
- `topic` (query) - Research topic (10-500 chars)
- `client_email` (query) - Email address or "display@ui.local"

**Request:**
```http
GET /api/research/workflow-1234567890/stream?topic=Latest%20AI%20developments&client_email=display@ui.local HTTP/1.1
Host: localhost:8000
Accept: text/event-stream
```

**Response:** Server-Sent Events stream

**Event Types:**

#### **Start Event**
```json
{
  "type": "start",
  "workflow_id": "workflow-1234567890",
  "from_cache": false
}
```

#### **Update Event**
```json
{
  "type": "update",
  "step": "planner",
  "messages": [
    "Analyzing research topic...",
    "Generating sub-queries..."
  ]
}
```

#### **Complete Event**
```json
{
  "type": "complete",
  "summary": "Artificial intelligence has experienced...",
  "citations": [
    {
      "claim": "GPT-5 released in 2026",
      "source_url": "https://techcrunch.com/...",
      "source_title": "OpenAI Unveils GPT-5"
    }
  ],
  "email_sent": false,
  "verified": true,
  "verification_status": "pass",
  "verification_confidence": 0.85,
  "from_cache": false
}
```

#### **Validation Error Event**
```json
{
  "type": "validation_error",
  "error": "This appears to be a personal question...",
  "suggestion": "Try asking about 'History of identity systems'"
}
```

#### **Error Event**
```json
{
  "type": "error",
  "error": "An error occurred during research"
}
```

**Response Codes:**
- `200 OK` - Stream started successfully
- `400 Bad Request` - Invalid parameters
- `500 Internal Server Error` - Server error

**Example:**
```bash
curl -N "http://localhost:8000/api/research/workflow-123/stream?topic=Latest%20AI%20developments&client_email=display@ui.local"
```

**Frontend Usage:**
```typescript
const workflowId = `workflow-${Date.now()}`
const url = `http://localhost:8000/api/research/${workflowId}/stream?topic=${encodeURIComponent(topic)}&client_email=${encodeURIComponent(email)}`

const eventSource = new EventSource(url)

eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data)
  
  switch (data.type) {
    case 'start':
      console.log('Workflow started:', data.workflow_id)
      break
    case 'update':
      console.log('Step:', data.step, 'Messages:', data.messages)
      break
    case 'complete':
      console.log('Summary:', data.summary)
      console.log('Citations:', data.citations)
      eventSource.close()
      break
    case 'validation_error':
      console.error('Validation failed:', data.error)
      console.log('Suggestion:', data.suggestion)
      eventSource.close()
      break
    case 'error':
      console.error('Error:', data.error)
      eventSource.close()
      break
  }
}

eventSource.onerror = () => {
  console.error('Connection lost')
  eventSource.close()
}
```

---

### **3. Send Email**

Send research results via email after workflow completion.

**Endpoint:** `POST /api/send-email`

**Request Body:**
```json
{
  "email": "user@example.com",
  "topic": "Latest AI developments",
  "summary": "Artificial intelligence has experienced...",
  "citations": [
    {
      "claim": "GPT-5 released",
      "source_url": "https://...",
      "source_title": "OpenAI News"
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "message": "Email sent successfully",
  "timestamp": "2026-03-12T20:30:00Z"
}
```

**Response Codes:**
- `200 OK` - Email sent successfully
- `400 Bad Request` - Invalid email or missing fields
- `403 Forbidden` - Email functionality disabled
- `500 Internal Server Error` - Email sending failed

**Example:**
```bash
curl -X POST http://localhost:8000/api/send-email \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "topic": "Latest AI developments",
    "summary": "AI has experienced...",
    "citations": []
  }'
```

**Frontend Usage:**
```typescript
const response = await fetch('http://localhost:8000/api/send-email', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    email: 'user@example.com',
    topic: topic,
    summary: summary,
    citations: citations,
  }),
})

const data = await response.json()

if (response.ok && data.success) {
  console.log('Email sent!')
} else {
  console.error('Email failed:', data.message)
}
```

---

## 📊 **Data Models**

See [Data Models](./MODELS.md) for detailed schema documentation.

---

## 🔄 **Workflow Sequence**

```
1. Frontend calls GET /api/config
   └─> Get email_enabled flag

2. User submits research form
   └─> Frontend opens EventSource to /api/research/{id}/stream

3. Backend validates topic
   ├─> Invalid: Send validation_error event
   └─> Valid: Continue

4. Backend checks Redis cache (if enabled)
   ├─> Cache HIT: Send cached complete event
   └─> Cache MISS: Execute workflow

5. Backend executes workflow
   ├─> Send start event
   ├─> Send update events (for each step)
   └─> Send complete event

6. Frontend displays results

7. (Optional) User sends email
   └─> Frontend calls POST /api/send-email
```

---

## 🛡️ **Error Handling**

### **Validation Errors**

**Scenario:** Invalid topic

**Response:**
```json
{
  "type": "validation_error",
  "error": "This topic is too vague for meaningful research",
  "suggestion": "Try 'Latest AI developments in healthcare 2026'"
}
```

### **Workflow Errors**

**Scenario:** Error during research

**Response:**
```json
{
  "type": "error",
  "error": "Failed to retrieve search results"
}
```

### **Email Errors**

**Scenario:** Email disabled

**Response:**
```json
{
  "detail": "Email functionality is disabled"
}
```

**Status Code:** `403 Forbidden`

---

## 🔧 **Configuration**

### **Environment Variables**

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-...
TAVILY_API_KEY=tvly-...

# Optional
LANGSMITH_API_KEY=ls-...
REDIS_URL=redis://localhost:6379

# Feature Flags
EMAIL_ENABLED=false
```

### **CORS Configuration**

**Allowed Origins:**
```python
cors_origins = "http://localhost:5173,http://localhost:3000"
```

**Allowed Methods:**
```
GET, POST, OPTIONS
```

**Allowed Headers:**
```
Content-Type, Authorization
```

---

## 📈 **Rate Limiting**

**Current:** No rate limiting (development)

**Future Production:**
- 100 requests per hour per IP
- 10 concurrent workflows per user
- Configurable via middleware

---

## 🔍 **Monitoring**

### **Health Check**

```bash
curl http://localhost:8000/
```

**Response:**
```json
{
  "message": "MCP Research Agent API",
  "status": "healthy"
}
```

### **Logs**

```bash
# View all logs
tail -f backend/logs/research_agent.log

# View agent logs
tail -f backend/logs/agents.log

# View workflow logs
tail -f backend/logs/workflow.log
```

### **LangSmith Tracing**

Visit: https://smith.langchain.com/

Filter by project: `mcp-research-agent`

---

## 🧪 **Testing**

### **Test Configuration Endpoint**

```bash
curl http://localhost:8000/api/config
```

**Expected:**
```json
{"email_enabled": false}
```

### **Test Research Stream**

```bash
curl -N "http://localhost:8000/api/research/test-123/stream?topic=Latest%20quantum%20computing&client_email=display@ui.local"
```

**Expected:** Stream of SSE events

### **Test Email Endpoint**

```bash
curl -X POST http://localhost:8000/api/send-email \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","topic":"Test","summary":"Test summary","citations":[]}'
```

**Expected (if EMAIL_ENABLED=false):**
```json
{"detail": "Email functionality is disabled"}
```

---

## 📚 **Related Documentation**

- [Data Models](./MODELS.md) - Request/response schemas
- [Architecture](../architecture/OVERVIEW.md) - System architecture
- [Workflow Guide](../guides/WORKFLOW_GUIDE.md) - Workflow details
- [Debug Guide](../troubleshooting/DEBUG_GUIDE.md) - Debugging tips

---

## 🆘 **Support**

**Issues with API:**
1. Check backend logs: `tail -f backend/logs/research_agent.log`
2. Verify API keys in `.env`
3. Check CORS settings
4. See [Common Issues](../troubleshooting/COMMON_ISSUES.md)

---

**API Version:** 1.0.0  
**Last Updated:** March 2026
