# 🔄 Complete Workflow Guide

Detailed explanation of the MCP Research Agent workflow with diagrams and code examples.

---

## 📊 **Workflow Overview**

```
┌─────────────────────────────────────────────────────────────────┐
│                     Research Workflow                            │
└─────────────────────────────────────────────────────────────────┘

User Input: "Latest developments in quantum computing"
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 1: TOPIC VALIDATION (0.5-1s)                               │
│                                                                  │
│ Agent: Topic Validator                                          │
│ Model: Claude Sonnet 4                                          │
│                                                                  │
│ ┌──────────────────────────────────────────────────────────┐   │
│ │ Input: "Latest developments in quantum computing"        │   │
│ │                                                           │   │
│ │ Checks:                                                   │   │
│ │ ✓ Not a personal question                                │   │
│ │ ✓ Length > 10 characters                                 │   │
│ │ ✓ Researchable topic                                     │   │
│ │ ✓ Not inappropriate                                      │   │
│ │                                                           │   │
│ │ Result: ✅ VALID                                          │   │
│ └──────────────────────────────────────────────────────────┘   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 2: RESEARCH PLANNING (2-5s)                                │
│                                                                  │
│ Agent: Planner                                                   │
│ Model: Claude Sonnet 4                                          │
│                                                                  │
│ ┌──────────────────────────────────────────────────────────┐   │
│ │ Input: "Latest developments in quantum computing"        │   │
│ │                                                           │   │
│ │ Output: Research Plan                                    │   │
│ │ {                                                         │   │
│ │   "strategy": "Multi-faceted quantum computing research",│   │
│ │   "sub_queries": [                                       │   │
│ │     "Quantum computing breakthroughs 2026",              │   │
│ │     "Latest quantum algorithms and applications",        │   │
│ │     "Quantum hardware advances 2026",                    │   │
│ │     "Quantum computing industry developments",           │   │
│ │     "Future of quantum computing research"               │   │
│ │   ]                                                       │   │
│ │ }                                                         │   │
│ └──────────────────────────────────────────────────────────┘   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 3: WEB RETRIEVAL (5-10s)                                   │
│                                                                  │
│ Agent: Retriever                                                 │
│ Tool: Tavily AI Search                                          │
│                                                                  │
│ ┌──────────────────────────────────────────────────────────┐   │
│ │ For each sub-query:                                      │   │
│ │                                                           │   │
│ │ Query 1: "Quantum computing breakthroughs 2026"         │   │
│ │ ├─ Search Tavily                                         │   │
│ │ ├─ Get 5 results                                         │   │
│ │ └─ Extract: title, url, content                          │   │
│ │                                                           │   │
│ │ Query 2: "Latest quantum algorithms..."                 │   │
│ │ ├─ Search Tavily                                         │   │
│ │ ├─ Get 5 results                                         │   │
│ │ └─ Extract: title, url, content                          │   │
│ │                                                           │   │
│ │ ... (repeat for all 5 queries)                           │   │
│ │                                                           │   │
│ │ Total Results: 25 articles from 20+ sources              │   │
│ └──────────────────────────────────────────────────────────┘   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 4: CONTENT SYNTHESIS (15-30s)                              │
│                                                                  │
│ Agent: Summarizer                                                │
│ Model: Claude Sonnet 4                                          │
│                                                                  │
│ ┌──────────────────────────────────────────────────────────┐   │
│ │ Input: 25 search results                                 │   │
│ │                                                           │   │
│ │ Process:                                                  │   │
│ │ 1. Analyze all content                                   │   │
│ │ 2. Identify key themes                                   │   │
│ │ 3. Extract important facts                               │   │
│ │ 4. Create structured summary                             │   │
│ │ 5. Generate citations                                    │   │
│ │                                                           │   │
│ │ Output: ResearchSummary                                  │   │
│ │ {                                                         │   │
│ │   "summary": "Quantum computing has seen...",            │   │
│ │   "key_findings": [...],                                 │   │
│ │   "citations": [                                         │   │
│ │     {                                                     │   │
│ │       "claim": "IBM announced 1000-qubit processor",     │   │
│ │       "source_url": "https://...",                       │   │
│ │       "source_title": "IBM Quantum Breakthrough"         │   │
│ │     }                                                     │   │
│ │   ]                                                       │   │
│ │ }                                                         │   │
│ └──────────────────────────────────────────────────────────┘   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 5: QUALITY VERIFICATION (5-10s)                            │
│                                                                  │
│ Agent: Verifier                                                  │
│ Model: Claude Sonnet 4                                          │
│                                                                  │
│ ┌──────────────────────────────────────────────────────────┐   │
│ │ Input: Summary + Citations + Sources                     │   │
│ │                                                           │   │
│ │ Checks:                                                   │   │
│ │ ✓ Citations match sources                                │   │
│ │ ✓ Claims are supported                                   │   │
│ │ ✓ No hallucinations                                      │   │
│ │ ✓ Accuracy assessment                                    │   │
│ │                                                           │   │
│ │ Output: VerificationResult                               │   │
│ │ {                                                         │   │
│ │   "status": "pass",                                      │   │
│ │   "confidence": 0.85,                                    │   │
│ │   "issues_found": [],                                    │   │
│ │   "feedback": "Summary is accurate and well-cited"       │   │
│ │ }                                                         │   │
│ │                                                           │   │
│ │ Decision:                                                 │   │
│ │ ├─ Pass (confidence > 0.7) → Continue                    │   │
│ │ └─ Fail → Retry once → Force pass                        │   │
│ └──────────────────────────────────────────────────────────┘   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 6: DELIVERY (instant)                                      │
│                                                                  │
│ Agent: Email Sender (if email provided)                         │
│                                                                  │
│ ┌──────────────────────────────────────────────────────────┐   │
│ │ Options:                                                  │   │
│ │                                                           │   │
│ │ 1. Display in UI (default)                               │   │
│ │    └─ Show summary, citations, verification badge        │   │
│ │                                                           │   │
│ │ 2. Send via Email (if EMAIL_ENABLED=true)                │   │
│ │    └─ Format as HTML email                               │   │
│ │    └─ Send via Gmail MCP                                 │   │
│ │                                                           │   │
│ │ 3. Cache for future (if Redis enabled)                   │   │
│ │    └─ Store with 24h TTL                                 │   │
│ └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔍 **Step-by-Step Breakdown**

### **Step 1: Topic Validation**

**Purpose:** Prevent invalid queries from wasting API calls

**Code Example:**
```python
# backend/agents/topic_validator.py

async def validate_topic(topic: str) -> Dict[str, Any]:
    """Validate if topic is appropriate for research."""
    
    llm = ChatAnthropic(
        model="claude-sonnet-4-20250514",
        temperature=0
    )
    
    structured_llm = llm.with_structured_output(TopicValidation)
    
    result = await structured_llm.ainvoke({
        "topic": topic
    })
    
    return {
        "is_valid": result.is_valid,
        "reason": result.reason,
        "suggestion": result.suggestion
    }
```

**Rejection Examples:**
```
❌ "What is my name?" 
   → Personal question

❌ "AI"
   → Too vague

❌ "the latest"
   → Fragmented/incomplete

✅ "Latest AI developments in 2026"
   → Valid research topic
```

---

### **Step 2: Research Planning**

**Purpose:** Create strategic sub-queries for comprehensive research

**Code Example:**
```python
# backend/agents/planner.py

async def plan_research(topic: str) -> Dict[str, Any]:
    """Generate research plan with sub-queries."""
    
    llm = ChatAnthropic(
        model="claude-sonnet-4-20250514",
        temperature=0.3
    )
    
    structured_llm = llm.with_structured_output(ResearchPlan)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a research planning expert.
        Create 3-5 specific sub-queries that will comprehensively 
        cover the research topic."""),
        ("human", "Topic: {topic}")
    ])
    
    result = await (prompt | structured_llm).ainvoke({
        "topic": topic
    })
    
    return {
        "research_plan": result.dict(),
        "sub_queries": result.sub_queries
    }
```

**Example Output:**
```json
{
  "strategy": "Multi-faceted quantum computing research",
  "sub_queries": [
    "Quantum computing breakthroughs 2026",
    "Latest quantum algorithms and applications",
    "Quantum hardware advances 2026",
    "Quantum computing industry developments",
    "Future of quantum computing research"
  ],
  "key_areas": [
    "Hardware developments",
    "Algorithm innovations",
    "Industry applications"
  ]
}
```

---

### **Step 3: Web Retrieval**

**Purpose:** Gather information from multiple sources

**Code Example:**
```python
# backend/agents/retriever.py

async def retrieve_information(sub_queries: List[str]) -> Dict[str, Any]:
    """Search web for each sub-query."""
    
    all_results = []
    all_sources = set()
    
    for query in sub_queries:
        # Search with Tavily
        results = await tavily_search(
            query=query,
            max_results=5
        )
        
        for result in results:
            all_results.append({
                "query": query,
                "title": result["title"],
                "url": result["url"],
                "content": result["content"],
                "score": result.get("score", 0.0)
            })
            all_sources.add(result["url"])
    
    return {
        "raw_data": all_results,
        "sources": list(all_sources)
    }
```

**Example Result:**
```json
{
  "raw_data": [
    {
      "query": "Quantum computing breakthroughs 2026",
      "title": "IBM Unveils 1000-Qubit Quantum Processor",
      "url": "https://techcrunch.com/...",
      "content": "IBM has announced...",
      "score": 0.95
    },
    // ... 24 more results
  ],
  "sources": [
    "https://techcrunch.com/...",
    "https://nature.com/...",
    // ... 20+ unique sources
  ]
}
```

---

### **Step 4: Content Synthesis**

**Purpose:** Create coherent summary from multiple sources

**Code Example:**
```python
# backend/agents/summarizer.py

async def summarize_research(
    topic: str,
    raw_data: List[Dict],
    sources: List[str]
) -> Dict[str, Any]:
    """Synthesize research findings."""
    
    # Format research context
    research_context = "\n\n".join([
        f"Source: {item['title']}\n{item['content']}"
        for item in raw_data
    ])
    
    llm = ChatAnthropic(
        model="claude-sonnet-4-20250514",
        temperature=0.2
    )
    
    structured_llm = llm.with_structured_output(ResearchSummary)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a research synthesis expert.
        Create a comprehensive summary with proper citations."""),
        ("human", """Topic: {topic}
        
        Research Data:
        {research_context}
        
        Create a well-structured summary with citations.""")
    ])
    
    result = await (prompt | structured_llm).ainvoke({
        "topic": topic,
        "research_context": research_context
    })
    
    return {
        "summary": result.summary,
        "key_findings": result.key_findings,
        "citations": result.citations
    }
```

**Example Output:**
```json
{
  "summary": "Quantum computing has experienced significant...",
  "key_findings": [
    "IBM announced 1000-qubit processor",
    "Google achieved quantum advantage in optimization",
    "New error correction techniques developed"
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

### **Step 5: Quality Verification**

**Purpose:** Ensure accuracy and proper citations

**Code Example:**
```python
# backend/agents/verifier.py

async def verify_research(
    state: ResearchState,
    summary: str,
    citations: List[Dict],
    sources: List[str]
) -> Dict[str, Any]:
    """Verify summary accuracy and citations."""
    
    llm = ChatAnthropic(
        model="claude-sonnet-4-20250514",
        temperature=0
    )
    
    structured_llm = llm.with_structured_output(VerificationResult)
    
    # Circuit breaker: max 1 retry
    if state.get("retry_count", 0) >= 1:
        logger.warning("⚠️ Max retries reached, forcing pass")
        return {
            "verification_status": "pass",
            "verification_confidence": 0.7,
            "verified": False  # Mark as "Not Verified"
        }
    
    result = await structured_llm.ainvoke({
        "summary": summary,
        "citations": citations,
        "sources": sources
    })
    
    # Pass if confidence > 0.7
    passed = result.confidence >= 0.7
    
    return {
        "verification_status": "pass" if passed else "fail",
        "verification_confidence": result.confidence,
        "verification_feedback": result.feedback,
        "verified": passed
    }
```

**Verification Flow:**
```
Verify Summary
    │
    ├─ Check citations match sources
    ├─ Assess claim accuracy
    ├─ Calculate confidence score
    │
    ▼
Confidence >= 0.7?
    │
    ├─ YES → Pass → Continue
    │
    └─ NO → Fail
         │
         ├─ Retry count < 1?
         │   │
         │   ├─ YES → Retry summarization
         │   │
         │   └─ NO → Force pass (mark "Not Verified")
         │
         └─ Continue to delivery
```

---

### **Step 6: Delivery**

**Purpose:** Present results to user

**Code Example:**
```python
# backend/agents/email_sender.py

async def send_research_email(
    topic: str,
    client_email: str,
    summary: str,
    key_findings: List[str],
    citations: List[Dict]
) -> Dict[str, Any]:
    """Send research via email or display in UI."""
    
    # Skip if display@ui.local (UI display only)
    if client_email == "display@ui.local":
        return {
            "email_sent": False,
            "email_timestamp": None
        }
    
    # Check if email feature enabled
    if not settings.email_enabled:
        return {
            "email_sent": False,
            "email_timestamp": None
        }
    
    # Format email
    html_content = format_research_email(
        topic, summary, key_findings, citations
    )
    
    # Send via Gmail MCP
    result = await gmail_mcp_send(
        to=client_email,
        subject=f"Research: {topic}",
        html=html_content
    )
    
    return {
        "email_sent": result.success,
        "email_timestamp": datetime.now().isoformat()
    }
```

---

## 🔄 **State Transitions**

```python
# backend/graph/state.py

class ResearchState(TypedDict):
    """Workflow state that flows through all agents."""
    
    # Input
    topic: str
    client_email: str
    
    # Planning (after planner)
    research_plan: Optional[Dict]
    sub_queries: List[str]
    
    # Retrieval (after retriever)
    raw_data: List[Dict]
    sources: List[str]
    
    # Summarization (after summarizer)
    summary: str
    citations: List[Dict]
    
    # Verification (after verifier)
    verification_status: str
    verification_confidence: float
    verification_feedback: str
    verified: bool
    
    # Delivery (after email_sender)
    final_output: str
    email_sent: bool
    email_timestamp: Optional[str]
    
    # Metadata
    workflow_id: str
    current_step: str
    errors: List[str]
    retry_count: int
    status_messages: List[str]
```

**State Evolution:**
```
Initial State:
{
  "topic": "Latest quantum computing",
  "client_email": "display@ui.local",
  "current_step": "planner",
  "retry_count": 0,
  ...
}

After Planner:
{
  ...
  "research_plan": {...},
  "sub_queries": [...],
  "current_step": "retriever"
}

After Retriever:
{
  ...
  "raw_data": [...],
  "sources": [...],
  "current_step": "summarizer"
}

After Summarizer:
{
  ...
  "summary": "...",
  "citations": [...],
  "current_step": "verifier"
}

After Verifier:
{
  ...
  "verification_status": "pass",
  "verified": true,
  "current_step": "email_sender"
}

Final State:
{
  ...
  "email_sent": false,
  "current_step": "complete"
}
```

---

## 🎯 **Error Handling**

### **Validation Errors**

```python
# Rejected at validation
{
  "type": "validation_error",
  "error": "This appears to be a personal question...",
  "suggestion": "Try asking about..."
}
```

### **Workflow Errors**

```python
# Error during workflow
try:
    result = await agent_function(state)
except Exception as e:
    logger.error(f"Agent error: {e}")
    state["errors"].append(str(e))
    # Continue with degraded functionality
```

### **Retry Logic**

```python
# In verifier
if verification_failed and retry_count < 1:
    return "summarizer"  # Retry
else:
    return "email_sender"  # Force pass
```

---

## 📊 **Performance Metrics**

| Step | Time | API Calls | Cost |
|------|------|-----------|------|
| Validation | 0.5-1s | 1 | $0.001 |
| Planning | 2-5s | 1 | $0.02 |
| Retrieval | 5-10s | 5 | $0.05 |
| Summarization | 15-30s | 1 | $0.12 |
| Verification | 5-10s | 1 | $0.03 |
| **Total** | **30-60s** | **9** | **$0.22** |

---

**Next:** [Agent Guide](./AGENT_GUIDE.md) for detailed agent explanations.
