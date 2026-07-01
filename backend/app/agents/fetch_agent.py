from typing import Dict, Any, Optional, List
from app.agents.base_agent import BaseAgent
from app.integrations.tinyfish_integration import tinyfish_integration
from app.core.logging import log


class FetchAgent(BaseAgent):
    def __init__(self):
        super().__init__("fetch_agent")

    async def _execute(
        self,
        input_data: Dict[str, Any],
        feedback_id: Optional[str] = None,
        ticket_id: Optional[str] = None
    ) -> Dict[str, Any]:
        url = input_data.get("url", "")
        extract_content = input_data.get("extract_content", True)
        extract_links = input_data.get("extract_links", True)
        extract_images = input_data.get("extract_images", False)
        
        if not url:
            raise ValueError("URL is required")
        
        result = await tinyfish_integration.fetch(
            url=url,
            extract_content=extract_content,
            extract_links=extract_links,
            extract_images=extract_images
        )
        
        log.info(f"Fetched content from {url}")
        
        return {
            "url": url,
            "content": result.get("content", ""),
            "title": result.get("title", ""),
            "links": result.get("links", []),
            "images": result.get("images", []),
            "metadata": result.get("metadata", {}),
        }

    async def fetch_multiple(self, urls: List[str]) -> Dict[str, Any]:
        results = []
        failed = []
        
        for url in urls:
            try:
                result = await self.execute({"url": url})
                results.append(result)
            except Exception as e:
                log.error(f"Failed to fetch {url}: {e}")
                failed.append({"url": url, "error": str(e)})
        
        log.info(f"Fetched {len(results)}/{len(urls)} URLs successfully")
        
        return {
            "total_urls": len(urls),
            "successful": len(results),
            "failed": len(failed),
            "results": results,
            "failed_urls": failed,
        }

    async def fetch_and_summarize(self, url: str) -> Dict[str, Any]:
        from app.integrations.llm_provider import llm_provider
        
        fetch_result = await self.execute({"url": url})
        content = fetch_result.get("content", "")
        
        if not content:
            return {
                "url": url,
                "summary": "No content to summarize",
                "error": "Empty content",
            }
        
        system_prompt = "Summarize the fetched content concisely, highlighting key points."
        prompt = f"Summarize this content:\n\n{content[:4000]}"
        
        summary = await llm_provider.generate(prompt, system_prompt)
        
        return {
            "url": url,
            "title": fetch_result.get("title", ""),
            "summary": summary,
            "original_length": len(content),
        }

    async def fetch_for_context(self, query: str, limit: int = 5) -> Dict[str, Any]:
        from app.integrations.tinyfish_integration import tinyfish_integration
        
        search_results = await tinyfish_integration.search(query, limit=limit)
        
        if not search_results:
            return {
                "query": query,
                "fetched_content": [],
                "message": "No search results to fetch",
            }
        
        urls = [r.get("url", "") for r in search_results if r.get("url")]
        urls = urls[:3]
        
        fetch_results = await self.fetch_multiple(urls)
        
        return {
            "query": query,
            "search_results": search_results,
            "fetched_content": fetch_results.get("results", []),
        }
