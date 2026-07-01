from typing import Optional, Dict, Any, List
import httpx
from app.config import settings
from app.core.logging import log
from app.core.exceptions import ExternalServiceException


class CogneeIntegration:
    def __init__(self):
        self._api_key = settings.cognee_api_key
        self._endpoint = settings.cognee_endpoint
        self._vector_db = settings.cognee_vector_db
        self._knowledge_graph = settings.cognee_knowledge_graph

    async def store_memory(
        self,
        content: str,
        memory_type: str,
        metadata: Optional[Dict[str, Any]] = None,
        embedding: Optional[List[float]] = None
    ) -> str:
        try:
            headers = {
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
            }
            
            payload = {
                "content": content,
                "memory_type": memory_type,
                "metadata": metadata or {},
                "embedding": embedding,
                "vector_db": self._vector_db,
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self._endpoint}/memory/store",
                    headers=headers,
                    json=payload,
                )
                response.raise_for_status()
                
                result = response.json()
                memory_id = result.get("memory_id")
                log.info(f"Stored memory in Cognee: {memory_id}")
                return memory_id
                
        except httpx.HTTPError as e:
            log.error(f"Cognee store memory failed: {e}")
            raise ExternalServiceException("Cognee", f"Store memory failed: {str(e)}")
        except Exception as e:
            log.error(f"Cognee store memory error: {e}")
            raise ExternalServiceException("Cognee", f"Store memory error: {str(e)}")

    async def retrieve_memory(
        self,
        query: str,
        memory_type: Optional[str] = None,
        limit: int = 10,
        similarity_threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        try:
            headers = {
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
            }
            
            payload = {
                "query": query,
                "memory_type": memory_type,
                "limit": limit,
                "similarity_threshold": similarity_threshold,
                "vector_db": self._vector_db,
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self._endpoint}/memory/retrieve",
                    headers=headers,
                    json=payload,
                )
                response.raise_for_status()
                
                result = response.json()
                memories = result.get("memories", [])
                log.info(f"Retrieved {len(memories)} memories from Cognee")
                return memories
                
        except httpx.HTTPError as e:
            log.error(f"Cognee retrieve memory failed: {e}")
            raise ExternalServiceException("Cognee", f"Retrieve memory failed: {str(e)}")
        except Exception as e:
            log.error(f"Cognee retrieve memory error: {e}")
            raise ExternalServiceException("Cognee", f"Retrieve memory error: {str(e)}")

    async def create_knowledge_graph(
        self,
        entities: List[Dict[str, Any]],
        relationships: List[Dict[str, Any]]
    ) -> str:
        try:
            headers = {
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
            }
            
            payload = {
                "entities": entities,
                "relationships": relationships,
                "knowledge_graph": self._knowledge_graph,
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self._endpoint}/graph/create",
                    headers=headers,
                    json=payload,
                )
                response.raise_for_status()
                
                result = response.json()
                graph_id = result.get("graph_id")
                log.info(f"Created knowledge graph in Cognee: {graph_id}")
                return graph_id
                
        except httpx.HTTPError as e:
            log.error(f"Cognee create knowledge graph failed: {e}")
            raise ExternalServiceException("Cognee", f"Create knowledge graph failed: {str(e)}")
        except Exception as e:
            log.error(f"Cognee create knowledge graph error: {e}")
            raise ExternalServiceException("Cognee", f"Create knowledge graph error: {str(e)}")

    async def search_knowledge_graph(
        self,
        entity: str,
        relationship_type: Optional[str] = None,
        depth: int = 2
    ) -> List[Dict[str, Any]]:
        try:
            headers = {
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
            }
            
            payload = {
                "entity": entity,
                "relationship_type": relationship_type,
                "depth": depth,
                "knowledge_graph": self._knowledge_graph,
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self._endpoint}/graph/search",
                    headers=headers,
                    json=payload,
                )
                response.raise_for_status()
                
                result = response.json()
                results = result.get("results", [])
                log.info(f"Knowledge graph search returned {len(results)} results")
                return results
                
        except httpx.HTTPError as e:
            log.error(f"Cognee knowledge graph search failed: {e}")
            raise ExternalServiceException("Cognee", f"Knowledge graph search failed: {str(e)}")
        except Exception as e:
            log.error(f"Cognee knowledge graph search error: {e}")
            raise ExternalServiceException("Cognee", f"Knowledge graph search error: {str(e)}")

    async def detect_patterns(
        self,
        memory_type: Optional[str] = None,
        time_range: Optional[Dict[str, str]] = None
    ) -> List[Dict[str, Any]]:
        try:
            headers = {
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
            }
            
            payload = {
                "memory_type": memory_type,
                "time_range": time_range or {},
            }
            
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self._endpoint}/patterns/detect",
                    headers=headers,
                    json=payload,
                )
                response.raise_for_status()
                
                result = response.json()
                patterns = result.get("patterns", [])
                log.info(f"Detected {len(patterns)} patterns in Cognee")
                return patterns
                
        except httpx.HTTPError as e:
            log.error(f"Cognee pattern detection failed: {e}")
            raise ExternalServiceException("Cognee", f"Pattern detection failed: {str(e)}")
        except Exception as e:
            log.error(f"Cognee pattern detection error: {e}")
            raise ExternalServiceException("Cognee", f"Pattern detection error: {str(e)}")

    async def delete_memory(self, memory_id: str) -> bool:
        try:
            headers = {
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.delete(
                    f"{self._endpoint}/memory/{memory_id}",
                    headers=headers,
                )
                response.raise_for_status()
                
                log.info(f"Deleted memory from Cognee: {memory_id}")
                return True
                
        except httpx.HTTPError as e:
            log.error(f"Cognee delete memory failed: {e}")
            raise ExternalServiceException("Cognee", f"Delete memory failed: {str(e)}")
        except Exception as e:
            log.error(f"Cognee delete memory error: {e}")
            raise ExternalServiceException("Cognee", f"Delete memory error: {str(e)}")


cognee_integration = CogneeIntegration()
