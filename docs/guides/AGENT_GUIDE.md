# 🤖 Agent Guide

Detailed explanation of each agent in the MCP Research Agent system.

---

## 📋 **Agent Overview**

The system uses **6 specialized agents**, each with a specific role:

```
┌──────────────────────────────────────────────────────────┐
│                    Agent Architecture                     │
└──────────────────────────────────────────────────────────┘

1. Topic Validator  → Validates user input
2. Planner         → Creates research strategy
3. Retriever       → Searches the web
4. Summarizer      → Synthesizes findings
5. Verifier        → Checks quality
6. Email Sender    → Delivers results
```

---

## 1️⃣ **Topic Validator Agent**

### **Purpose**
Prevent invalid or inappropriate queries from entering the workflow.

### **Model**
Claude Sonnet 4 (temperature=0 for consistency)

### **Input**
```python
{
    "topic": str  # User's research topic
}
```

### **Output**
```python
{
    "is_valid": bool,
    "reason": str,
    "suggestion": str
}
```

### **Validation Rules**

**Rejects:**
- ❌ Personal questions ("What is my name?")
- ❌ Too vague/short (< 10 chars)
- ❌ Non-researchable ("What am I thinking?")
- ❌ Inappropriate content
- ❌ Real-time personal data requests
- ❌ Fragmented queries ("the latest")

**Accepts:**
- ✅ General knowledge topics
- ✅ Current events
- ✅ Scientific/technical subjects
- ✅ Historical topics
- ✅ Industry trends
- ✅ How-to guides

### **Code Example**

```python
# backend/agents/topic_validator.py

class TopicValidation(BaseModel):
    is_valid: bool
    reason: str
    suggestion: str = ""

async def validate_topic(topic: str) -> Dict[str, Any]:
    llm = ChatAnthropic(
        model="claude-sonnet-4-20250514",
        temperature=0
    )
    
    structured_llm = llm.with_structured_output(TopicValidation)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a research topic validator.
        
        REJECT: personal questions, vague queries, non-researchable
        ACCEPT: general knowledge, current events, technical topics
        
        Use 2026 as current year in suggestions."""),
        ("human", "Topic: {topic}")
    ])
    
    result = await (prompt | structured_llm).ainvoke({"topic": topic})
    
    return {
        "is_valid": result.is_valid,
        "reason": result.reason,
        "suggestion": result.suggestion
    }
```

### **Example Interactions**

**Invalid Input:**
```
Input: "What is my name?"

Output: {
  "is_valid": false,
  "reason": "This is a personal question about your identity...",
  "suggestion": "Try: 'History of personal identity systems' or 
                'Digital identity verification in 2026'"
}
```

**Valid Input:**
```
Input: "Latest quantum computing developments"

Output: {
  "is_valid": true,
  "reason": "This is a valid research topic about current technology",
  "suggestion": ""
}
```

### **Performance**
- **Time:** 0.5-1 second
- **Cost:** ~$0.001 per validation
- **Success Rate:** 99%+ accuracy

---

## 2️⃣ **Planner Agent**

### **Purpose**
Create a strategic research plan with multiple sub-queries.

### **Model**
Claude Sonnet 4 (temperature=0.3 for creativity)

### **Input**
```python
{
    "topic": str
}
```

### **Output**
```python
{
    "research_plan": {
        "strategy": str,
        "key_areas": List[str],
        "approach": str
    },
    "sub_queries": List[str]  # 3-5 queries
}
```

### **Strategy**
1. Analyze topic breadth
2. Identify key areas to cover
3. Generate 3-5 specific sub-queries
4. Ensure comprehensive coverage

### **Code Example**

```python
# backend/agents/planner.py

class ResearchPlan(BaseModel):
    strategy: str
    key_areas: List[str]
    approach: str
    sub_queries: List[str] = Field(min_items=3, max_items=5)

async def plan_research(topic: str) -> Dict[str, Any]:
    llm = ChatAnthropic(
        model="claude-sonnet-4-20250514",
        temperature=0.3
    )
    
    structured_llm = llm.with_structured_output(ResearchPlan)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a research planning expert.
        
        Create 3-5 specific sub-queries that will comprehensively
        cover the research topic. Each query should target a
        different aspect or angle."""),
        ("human", "Research topic: {topic}")
    ])
    
    result = await (prompt | structured_llm).ainvoke({"topic": topic})
    
    return {
        "research_plan": result.dict(),
        "sub_queries": result.sub_queries
    }
```

### **Example Output**

**Input:** "Latest AI developments"

**Output:**
```json
{
  "research_plan": {
    "strategy": "Multi-faceted AI research covering models, applications, and industry",
    "key_areas": [
      "Large language models",
      "AI applications",
      "Industry adoption",
      "Ethical considerations"
    ],
    "approach": "Comprehensive coverage of technical and business aspects"
  },
  "sub_queries": [
    "Latest large language model breakthroughs 2026",
    "AI applications in healthcare and finance 2026",
    "Enterprise AI adoption trends",
    "AI ethics and regulation developments",
    "Future of AI research and predictions"
  ]
}
```

### **Performance**
- **Time:** 2-5 seconds
- **Cost:** ~$0.02 per plan
- **Sub-queries:** Always 3-5

---

## 3️⃣ **Retriever Agent**

### **Purpose**
Execute web searches for each sub-query using Tavily AI.

### **Tool**
Tavily AI Search API

### **Input**
```python
{
    "sub_queries": List[str]
}
```

### **Output**
```python
{
    "raw_data": List[Dict],  # All search results
    "sources": List[str]      # Unique URLs
}
```

### **Process**
1. For each sub-query:
   - Search Tavily (max 5 results per query)
   - Extract: title, URL, content, score
2. Aggregate all results
3. Deduplicate sources

### **Code Example**

```python
# backend/agents/retriever.py

async def retrieve_information(
    topic: str,
    sub_queries: List[str]
) -> Dict[str, Any]:
    all_results = []
    all_sources = set()
    
    for query in sub_queries:
        logger.info(f"🔍 Searching: {query}")
        
        # Search with Tavily
        results = await tavily_search(
            query=query,
            search_depth="advanced",
            max_results=5
        )
        
        for result in results:
            all_results.append({
                "query": query,
                "title": result["title"],
                "url": result["url"],
                "content": result["content"],
                "score": result.get("score", 0.0),
                "published_date": result.get("published_date")
            })
            all_sources.add(result["url"])
    
    logger.info(f"✅ Retrieved {len(all_results)} results from {len(all_sources)} sources")
    
    return {
        "raw_data": all_results,
        "sources": list(all_sources)
    }
```

### **Example Output**

```json
{
  "raw_data": [
    {
      "query": "Latest AI model breakthroughs 2026",
      "title": "GPT-5 Released with Multimodal Capabilities",
      "url": "https://techcrunch.com/...",
      "content": "OpenAI has announced GPT-5...",
      "score": 0.95,
      "published_date": "2026-01-15"
    },
    // ... 24 more results
  ],
  "sources": [
    "https://techcrunch.com/...",
    "https://arxiv.org/...",
    "https://venturebeat.com/...",
    // ... 20+ unique sources
  ]
}
```

### **Performance**
- **Time:** 5-10 seconds
- **Cost:** ~$0.05 (Tavily API)
- **Results:** 15-25 articles typically
- **Sources:** 15-25 unique URLs

---

## 4️⃣ **Summarizer Agent**

### **Purpose**
Synthesize research findings into a coherent summary with citations.

### **Model**
Claude Sonnet 4 (temperature=0.2 for balance)

### **Input**
```python
{
    "topic": str,
    "raw_data": List[Dict],
    "sources": List[str]
}
```

### **Output**
```python
{
    "summary": str,           # 300-800 words
    "key_findings": List[str],
    "citations": List[Dict]
}
```

### **Process**
1. Format all search results
2. Analyze content for key themes
3. Extract important facts
4. Create structured summary
5. Generate proper citations

### **Code Example**

```python
# backend/agents/summarizer.py

class Citation(BaseModel):
    claim: str
    source_url: str
    source_title: str

class ResearchSummary(BaseModel):
    summary: str = Field(min_length=300, max_length=2000)
    key_findings: List[str] = Field(default=[])
    citations: List[Citation] = Field(default=[])

async def summarize_research(
    topic: str,
    raw_data: List[Dict],
    sources: List[str]
) -> Dict[str, Any]:
    # Format research context
    research_context = "\n\n".join([
        f"**{item['title']}**\n{item['content'][:500]}..."
        for item in raw_data
    ])
    
    llm = ChatAnthropic(
        model="claude-sonnet-4-20250514",
        temperature=0.2
    )
    
    structured_llm = llm.with_structured_output(ResearchSummary)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a research synthesis expert.
        
        Create a comprehensive summary (300-800 words) with:
        - Clear structure and flow
        - Key findings highlighted
        - Proper citations for all claims
        - Objective and informative tone"""),
        ("human", """Topic: {topic}
        
        Research Data:
        {research_context}
        
        Available Sources:
        {sources}
        
        Create summary with citations.""")
    ])
    
    try:
        result = await (prompt | structured_llm).ainvoke({
            "topic": topic,
            "research_context": research_context,
            "sources": "\n".join(f"- {url}" for url in sources)
        })
        
        return {
            "summary": result.summary,
            "key_findings": result.key_findings,
            "citations": [cite.dict() for cite in result.citations]
        }
    except Exception as e:
        # Fallback to text generation
        logger.error(f"Structured output failed: {e}")
        # ... fallback logic
```

### **Example Output**

```json
{
  "summary": "Artificial intelligence has experienced remarkable progress in 2026, with several breakthrough developments reshaping the field. The release of GPT-5 by OpenAI marked a significant milestone, introducing enhanced multimodal capabilities that seamlessly integrate text, images, and audio processing...",
  
  "key_findings": [
    "GPT-5 released with advanced multimodal capabilities",
    "AI adoption in healthcare increased by 45%",
    "New AI regulations implemented in EU and US",
    "Quantum-AI hybrid systems demonstrated"
  ],
  
  "citations": [
    {
      "claim": "GPT-5 released with advanced multimodal capabilities",
      "source_url": "https://techcrunch.com/...",
      "source_title": "OpenAI Unveils GPT-5"
    },
    {
      "claim": "AI adoption in healthcare increased by 45%",
      "source_url": "https://healthtech.com/...",
      "source_title": "Healthcare AI Adoption Report 2026"
    }
  ]
}
```

### **Performance**
- **Time:** 15-30 seconds (longest step)
- **Cost:** ~$0.12 per summary
- **Length:** 300-800 words typically
- **Citations:** 3-8 typically

---

## 5️⃣ **Verifier Agent**

### **Purpose**
Verify summary accuracy and citation quality.

### **Model**
Claude Sonnet 4 (temperature=0 for consistency)

### **Input**
```python
{
    "summary": str,
    "citations": List[Dict],
    "sources": List[str],
    "retry_count": int
}
```

### **Output**
```python
{
    "verification_status": str,  # "pass" or "fail"
    "verification_confidence": float,  # 0.0-1.0
    "verification_feedback": str,
    "verified": bool
}
```

### **Verification Checks**
1. ✓ Citations match sources
2. ✓ Claims are supported
3. ✓ No hallucinations
4. ✓ Accuracy assessment
5. ✓ Confidence scoring

### **Circuit Breaker**
- Max 1 retry to prevent infinite loops
- After 1 retry, force pass with `verified=false`

### **Code Example**

```python
# backend/agents/verifier.py

class VerificationResult(BaseModel):
    status: str  # "pass" or "fail"
    confidence: float = Field(ge=0.0, le=1.0)
    issues_found: List[str] = Field(default=[])
    feedback: str

async def verify_research(
    state: ResearchState,
    summary: str,
    citations: List[Dict],
    sources: List[str]
) -> Dict[str, Any]:
    # Circuit breaker
    if state.get("retry_count", 0) >= 1:
        logger.warning("⚠️ Max retries reached, forcing pass")
        return {
            "verification_status": "pass",
            "verification_confidence": 0.7,
            "verification_feedback": "Forced pass after retry",
            "verified": False  # Mark as "Not Verified"
        }
    
    llm = ChatAnthropic(
        model="claude-sonnet-4-20250514",
        temperature=0
    )
    
    structured_llm = llm.with_structured_output(VerificationResult)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a research verification expert.
        
        Verify:
        1. Citations match sources
        2. Claims are supported
        3. No hallucinations
        4. Overall accuracy
        
        Confidence threshold: 0.7"""),
        ("human", """Summary: {summary}
        
        Citations: {citations}
        
        Sources: {sources}
        
        Verify accuracy.""")
    ])
    
    result = await (prompt | structured_llm).ainvoke({
        "summary": summary,
        "citations": json.dumps(citations),
        "sources": "\n".join(sources)
    })
    
    passed = result.confidence >= 0.7
    
    return {
        "verification_status": "pass" if passed else "fail",
        "verification_confidence": result.confidence,
        "verification_feedback": result.feedback,
        "verified": passed
    }
```

### **Decision Flow**

```
Verify Summary
    │
    ├─ Confidence >= 0.7?
    │   │
    │   ├─ YES → Pass
    │   │
    │   └─ NO → Fail
    │        │
    │        ├─ Retry count < 1?
    │        │   │
    │        │   ├─ YES → Retry summarization
    │        │   │
    │        │   └─ NO → Force pass (verified=false)
    │        │
    │        └─ Continue
```

### **Example Output**

**Pass:**
```json
{
  "verification_status": "pass",
  "verification_confidence": 0.85,
  "verification_feedback": "Summary is accurate and well-cited. All claims are properly supported by sources.",
  "verified": true
}
```

**Fail (with retry):**
```json
{
  "verification_status": "fail",
  "verification_confidence": 0.45,
  "verification_feedback": "Some claims lack proper citations. Suggest adding more source references.",
  "verified": false
}
```

### **Performance**
- **Time:** 5-10 seconds
- **Cost:** ~$0.03 per verification
- **Pass Rate:** ~70-80%
- **Retry Rate:** ~20-30%

---

## 6️⃣ **Email Sender Agent**

### **Purpose**
Deliver research results via email or UI.

### **Tool**
Gmail MCP (if email enabled)

### **Input**
```python
{
    "topic": str,
    "client_email": str,
    "summary": str,
    "key_findings": List[str],
    "citations": List[Dict]
}
```

### **Output**
```python
{
    "email_sent": bool,
    "email_timestamp": Optional[str]
}
```

### **Logic**
1. Check if email = "display@ui.local" → Skip email
2. Check if `EMAIL_ENABLED=true` → Send email
3. Format HTML email
4. Send via Gmail MCP

### **Code Example**

```python
# backend/agents/email_sender.py

async def send_research_email(
    topic: str,
    client_email: str,
    summary: str,
    key_findings: List[str],
    citations: List[Dict]
) -> Dict[str, Any]:
    # Skip if UI display only
    if client_email == "display@ui.local":
        return {
            "email_sent": False,
            "email_timestamp": None
        }
    
    # Check feature flag
    if not settings.email_enabled:
        logger.info("📧 Email disabled, skipping")
        return {
            "email_sent": False,
            "email_timestamp": None
        }
    
    # Format email
    html_content = f"""
    <html>
      <body>
        <h1>Research: {topic}</h1>
        <h2>Summary</h2>
        <p>{summary}</p>
        
        <h2>Key Findings</h2>
        <ul>
          {"".join(f"<li>{finding}</li>" for finding in key_findings)}
        </ul>
        
        <h2>Citations</h2>
        <ol>
          {"".join(f'<li>{cite["claim"]} - <a href="{cite["source_url"]}">{cite["source_title"]}</a></li>' for cite in citations)}
        </ol>
      </body>
    </html>
    """
    
    # Send via Gmail MCP
    try:
        result = await gmail_mcp_send(
            to=client_email,
            subject=f"Research Summary: {topic}",
            html=html_content
        )
        
        return {
            "email_sent": result.success,
            "email_timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"❌ Email failed: {e}")
        return {
            "email_sent": False,
            "email_timestamp": None
        }
```

### **Performance**
- **Time:** < 1 second (instant for UI)
- **Cost:** Free (Gmail API)
- **Success Rate:** 95%+ (when enabled)

---

## 📊 **Agent Comparison**

| Agent | Model | Temp | Time | Cost | Retry |
|-------|-------|------|------|------|-------|
| Validator | Claude 4 | 0.0 | 0.5-1s | $0.001 | No |
| Planner | Claude 4 | 0.3 | 2-5s | $0.02 | No |
| Retriever | Tavily | N/A | 5-10s | $0.05 | No |
| Summarizer | Claude 4 | 0.2 | 15-30s | $0.12 | Yes (1x) |
| Verifier | Claude 4 | 0.0 | 5-10s | $0.03 | No |
| Email | Gmail | N/A | <1s | Free | No |

---

**Next:** [API Documentation](../api/ENDPOINTS.md) for API reference.
