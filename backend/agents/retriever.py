"""Retriever agent - searches web using MCP tools."""
import asyncio
from typing import List, Dict, Any
import sys
import os
from langsmith import traceable

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp_tools.search_tool import SearchMCPTool


@traceable(name="retriever_agent", run_type="tool")
async def retrieve_information(sub_queries: List[str], max_results_per_query: int = 5) -> Dict[str, Any]:
    """
    Retrieve information for all sub-queries using web search.
    
    Args:
        sub_queries: List of search queries
        max_results_per_query: Maximum results per query
        
    Returns:
        Dictionary with raw_data and sources
    """
    search_tool = SearchMCPTool()
    
    all_results = []
    all_sources = []
    
    # Execute searches in parallel
    tasks = [
        search_tool.web_search(query, max_results_per_query)
        for query in sub_queries
    ]
    
    results_list = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Process results
    for query, results in zip(sub_queries, results_list):
        if isinstance(results, Exception):
            print(f"Error searching for '{query}': {results}")
            continue
        
        for result in results:
            # Add query context to result
            result_with_context = {
                "query": query,
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "description": result.get("description", ""),
                "content": result.get("content", result.get("description", ""))
            }
            all_results.append(result_with_context)
            
            # Track unique sources
            url = result.get("url", "")
            if url and url not in all_sources:
                all_sources.append(url)
    
    return {
        "raw_data": all_results,
        "sources": all_sources
    }
