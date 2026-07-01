from typing import Optional, Dict, Any, List
import httpx
from app.config import settings
from app.core.logging import log
from app.core.exceptions import ExternalServiceException


class TinyFishIntegration:
    def __init__(self):
        self._api_key = settings.tinyfish_api_key
        self._search_endpoint = settings.tinyfish_search_endpoint
        self._fetch_endpoint = settings.tinyfish_fetch_endpoint

    async def search(
        self,
        query: str,
        limit: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        try:
            headers = {
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
            }
            
            payload = {
                "query": query,
                "limit": limit,
                "filters": filters or {},
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self._search_endpoint,
                    headers=headers,
                    json=payload,
                )
                response.raise_for_status()
                
                results = response.json()
                log.info(f"TinyFish search returned {len(results.get('results', []))} results")
                return results.get("results", [])
                
        except httpx.HTTPError as e:
            log.error(f"TinyFish search failed: {e}")
            raise ExternalServiceException("TinyFish", f"Search failed: {str(e)}")
        except Exception as e:
            log.error(f"TinyFish search error: {e}")
            raise ExternalServiceException("TinyFish", f"Search error: {str(e)}")

    async def fetch(
        self,
        url: str,
        extract_content: bool = True,
        extract_links: bool = True,
        extract_images: bool = False
    ) -> Dict[str, Any]:
        try:
            headers = {
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
            }
            
            payload = {
                "url": url,
                "extract_content": extract_content,
                "extract_links": extract_links,
                "extract_images": extract_images,
            }
            
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    self._fetch_endpoint,
                    headers=headers,
                    json=payload,
                )
                response.raise_for_status()
                
                result = response.json()
                log.info(f"TinyFish fetch completed for {url}")
                return result
                
        except httpx.HTTPError as e:
            log.error(f"TinyFish fetch failed: {e}")
            raise ExternalServiceException("TinyFish", f"Fetch failed: {str(e)}")
        except Exception as e:
            log.error(f"TinyFish fetch error: {e}")
            raise ExternalServiceException("TinyFish", f"Fetch error: {str(e)}")

    async def batch_search(
        self,
        queries: List[str],
        limit_per_query: int = 5
    ) -> Dict[str, List[Dict[str, Any]]]:
        results = {}
        for query in queries:
            try:
                results[query] = await self.search(query, limit=limit_per_query)
            except Exception as e:
                log.error(f"Batch search failed for query '{query}': {e}")
                results[query] = []
        
        log.info(f"TinyFish batch search completed for {len(queries)} queries")
        return results

    async def semantic_search(
        self,
        query: str,
        embedding: Optional[List[float]] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        try:
            headers = {
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
            }
            
            payload = {
                "query": query,
                "embedding": embedding,
                "limit": limit,
                "search_type": "semantic",
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self._search_endpoint,
                    headers=headers,
                    json=payload,
                )
                response.raise_for_status()
                
                results = response.json()
                log.info(f"TinyFish semantic search returned {len(results.get('results', []))} results")
                return results.get("results", [])
                
        except httpx.HTTPError as e:
            log.error(f"TinyFish semantic search failed: {e}")
            raise ExternalServiceException("TinyFish", f"Semantic search failed: {str(e)}")
        except Exception as e:
            log.error(f"TinyFish semantic search error: {e}")
            raise ExternalServiceException("TinyFish", f"Semantic search error: {str(e)}")


tinyfish_integration = TinyFishIntegration()
