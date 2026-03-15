"""Tavily AI Search tool wrapper for web search (FREE tier: 1000 searches/month)."""
import os
import sys
from typing import List, Dict, Any
from langchain.tools import tool
import httpx

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import settings


class SearchMCPTool:
    """Tavily AI Search tool wrapper."""
    
    def __init__(
        self,
        api_key: str = None,
        use_http: bool = False,
        http_url: str = None
    ):
        """
        Initialize Tavily Search tool.
        
        Args:
            api_key: Tavily API key (get free at https://tavily.com)
            use_http: Whether to use HTTP wrapper (for Railway)
            http_url: HTTP wrapper URL (if use_http=True)
        """
        self.api_key = api_key or settings.tavily_api_key
        if not self.api_key:
            raise ValueError("TAVILY_API_KEY not set. Get free key at https://tavily.com")
        
        self.use_http = use_http
        self.http_url = http_url or os.getenv("SEARCH_MCP_URL", "http://localhost:3002")
        self.tavily_url = "https://api.tavily.com/search"
        
    async def web_search(self, query: str, count: int = 5) -> List[Dict[str, Any]]:
        """
        Search the web via Tavily AI.
        
        Args:
            query: Search query string
            count: Maximum number of results (default: 5)
            
        Returns:
            List of search results with title, url, description, content
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.tavily_url,
                json={
                    "api_key": self.api_key,
                    "query": query,
                    "max_results": count,
                    "search_depth": "basic",  # "basic" or "advanced"
                    "include_answer": False,
                    "include_raw_content": False
                },
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()
            
            # Tavily returns results in "results" key
            results = data.get("results", [])
            
            # Format to match expected structure
            formatted_results = []
            for result in results:
                formatted_results.append({
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "description": result.get("content", ""),
                    "content": result.get("content", "")
                })
            
            return formatted_results


# LangChain tool wrapper
@tool
async def search_web(query: str, max_results: int = 5) -> str:
    """
    Search the web for information using Tavily AI Search.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return (default: 5)
    
    Returns:
        Formatted string with search results including titles, URLs, and content
    """
    search = SearchMCPTool()
    results = await search.web_search(query, max_results)
    
    if not results:
        return f"No results found for query: {query}"
    
    # Format results for LLM consumption
    formatted = [f"Search results for '{query}':\n"]
    
    for i, result in enumerate(results, 1):
        title = result.get("title", "N/A")
        url = result.get("url", "N/A")
        description = result.get("description", "N/A")
        
        formatted.append(f"""
Result {i}:
Title: {title}
URL: {url}
Description: {description}
""")
    
    return "\n".join(formatted)
