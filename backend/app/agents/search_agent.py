from typing import Dict, Any, Optional, List
from app.agents.base_agent import BaseAgent
from app.integrations.tinyfish_integration import tinyfish_integration
from app.core.logging import log


class SearchAgent(BaseAgent):
    def __init__(self):
        super().__init__("search_agent")

    async def _execute(
        self,
        input_data: Dict[str, Any],
        feedback_id: Optional[str] = None,
        ticket_id: Optional[str] = None
    ) -> Dict[str, Any]:
        query = input_data.get("query", "")
        search_type = input_data.get("search_type", "general")
        limit = input_data.get("limit", 10)
        
        if not query:
            raise ValueError("Query is required")
        
        if search_type == "documentation":
            results = await self._search_documentation(query, limit)
        elif search_type == "release_notes":
            results = await self._search_release_notes(query, limit)
        elif search_type == "known_issues":
            results = await self._search_known_issues(query, limit)
        elif search_type == "semantic":
            results = await self._semantic_search(query, limit)
        else:
            results = await self._general_search(query, limit)
        
        log.info(f"Search agent found {len(results)} results for query: {query}")
        
        return {
            "query": query,
            "search_type": search_type,
            "results": results,
            "result_count": len(results),
        }

    async def _general_search(self, query: str, limit: int) -> List[Dict[str, Any]]:
        return await tinyfish_integration.search(query, limit=limit)

    async def _semantic_search(self, query: str, limit: int) -> List[Dict[str, Any]]:
        return await tinyfish_integration.semantic_search(query, limit=limit)

    async def _search_documentation(self, query: str, limit: int) -> List[Dict[str, Any]]:
        filters = {
            "content_type": "documentation",
            "source": "docs"
        }
        return await tinyfish_integration.search(query, limit=limit, filters=filters)

    async def _search_release_notes(self, query: str, limit: int) -> List[Dict[str, Any]]:
        filters = {
            "content_type": "release_notes",
            "source": "releases"
        }
        return await tinyfish_integration.search(query, limit=limit, filters=filters)

    async def _search_known_issues(self, query: str, limit: int) -> List[Dict[str, Any]]:
        filters = {
            "content_type": "known_issues",
            "source": "issues"
        }
        return await tinyfish_integration.search(query, limit=limit, filters=filters)

    async def batch_search(self, queries: List[str], limit_per_query: int = 5) -> Dict[str, Any]:
        results = await tinyfish_integration.batch_search(queries, limit_per_query)
        
        total_results = sum(len(r) for r in results.values())
        
        log.info(f"Batch search completed for {len(queries)} queries, total results: {total_results}")
        
        return {
            "queries": queries,
            "results": results,
            "total_results": total_results,
        }

    async def search_with_context(
        self,
        query: str,
        context: Dict[str, Any],
        limit: int = 10
    ) -> Dict[str, Any]:
        enhanced_query = f"{query} {context.get('category', '')} {context.get('feature', '')}"
        
        results = await self._general_search(enhanced_query, limit)
        
        return {
            "original_query": query,
            "enhanced_query": enhanced_query,
            "context": context,
            "results": results,
            "result_count": len(results),
        }
