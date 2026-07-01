from typing import Dict, Any, Optional, List
from app.integrations.cognee_integration import cognee_integration
from app.repositories.memory_repository import MemoryRepository
from app.core.logging import log


class CogneeManager:
    def __init__(self):
        self.cognee = cognee_integration
        self.memory_repo = MemoryRepository()

    async def store_feedback_memory(
        self,
        feedback_id: str,
        content: str,
        category: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        try:
            cognee_memory_id = await self.cognee.store_memory(
                content=content,
                memory_type=f"feedback_{category}",
                metadata={
                    "feedback_id": feedback_id,
                    "category": category,
                    **(metadata or {}),
                }
            )
            
            local_memory_id = await self.memory_repo.create_memory(
                memory_type=f"feedback_{category}",
                content=content,
                metadata={
                    "cognee_memory_id": cognee_memory_id,
                    "feedback_id": feedback_id,
                    "category": category,
                    **(metadata or {}),
                }
            )
            
            log.info(f"Stored feedback memory: feedback_id={feedback_id}, cognee_id={cognee_memory_id}, local_id={local_memory_id}")
            
            return local_memory_id
            
        except Exception as e:
            log.error(f"Error storing feedback memory: {e}")
            raise

    async def store_ticket_memory(
        self,
        ticket_id: str,
        title: str,
        description: str,
        category: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        try:
            content = f"{title}\n\n{description}"
            
            cognee_memory_id = await self.cognee.store_memory(
                content=content,
                memory_type=f"ticket_{category}",
                metadata={
                    "ticket_id": ticket_id,
                    "title": title,
                    "category": category,
                    **(metadata or {}),
                }
            )
            
            local_memory_id = await self.memory_repo.create_memory(
                memory_type=f"ticket_{category}",
                content=content,
                metadata={
                    "cognee_memory_id": cognee_memory_id,
                    "ticket_id": ticket_id,
                    "title": title,
                    "category": category,
                    **(metadata or {}),
                },
                related_entities=[ticket_id]
            )
            
            log.info(f"Stored ticket memory: ticket_id={ticket_id}, cognee_id={cognee_memory_id}, local_id={local_memory_id}")
            
            return local_memory_id
            
        except Exception as e:
            log.error(f"Error storing ticket memory: {e}")
            raise

    async def retrieve_similar_feedback(
        self,
        query: str,
        category: Optional[str] = None,
        limit: int = 10,
        similarity_threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        try:
            memory_type = f"feedback_{category}" if category else "feedback"
            
            memories = await self.cognee.retrieve_memory(
                query=query,
                memory_type=memory_type,
                limit=limit,
                similarity_threshold=similarity_threshold
            )
            
            log.info(f"Retrieved {len(memories)} similar feedback items")
            
            return memories
            
        except Exception as e:
            log.error(f"Error retrieving similar feedback: {e}")
            return []

    async def retrieve_historical_issues(
        self,
        query: str,
        category: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        try:
            memory_type = f"ticket_{category}" if category else "ticket"
            
            memories = await self.cognee.retrieve_memory(
                query=query,
                memory_type=memory_type,
                limit=limit,
                similarity_threshold=0.5
            )
            
            log.info(f"Retrieved {len(memories)} historical issues")
            
            return memories
            
        except Exception as e:
            log.error(f"Error retrieving historical issues: {e}")
            return []

    async def detect_recurring_patterns(
        self,
        memory_type: Optional[str] = None,
        time_range: Optional[Dict[str, str]] = None
    ) -> List[Dict[str, Any]]:
        try:
            patterns = await self.cognee.detect_patterns(
                memory_type=memory_type,
                time_range=time_range
            )
            
            log.info(f"Detected {len(patterns)} recurring patterns")
            
            return patterns
            
        except Exception as e:
            log.error(f"Error detecting recurring patterns: {e}")
            return []

    async def create_issue_knowledge_graph(
        self,
        ticket_id: str,
        related_tickets: List[str],
        category: str
    ) -> str:
        try:
            entities = [
                {"id": ticket_id, "type": "ticket", "category": category},
            ]
            
            for related_id in related_tickets:
                entities.append({"id": related_id, "type": "ticket"})
            
            relationships = []
            for related_id in related_tickets:
                relationships.append({
                    "from": ticket_id,
                    "to": related_id,
                    "type": "related_to",
                })
            
            graph_id = await self.cognee.create_knowledge_graph(
                entities=entities,
                relationships=relationships
            )
            
            log.info(f"Created knowledge graph for ticket {ticket_id}: {graph_id}")
            
            return graph_id
            
        except Exception as e:
            log.error(f"Error creating knowledge graph: {e}")
            raise

    async def search_knowledge_graph(
        self,
        entity_id: str,
        relationship_type: Optional[str] = None,
        depth: int = 2
    ) -> List[Dict[str, Any]]:
        try:
            results = await self.cognee.search_knowledge_graph(
                entity=entity_id,
                relationship_type=relationship_type,
                depth=depth
            )
            
            log.info(f"Knowledge graph search returned {len(results)} results")
            
            return results
            
        except Exception as e:
            log.error(f"Error searching knowledge graph: {e}")
            return []

    async def get_context_for_feedback(
        self,
        content: str,
        category: Optional[str] = None
    ) -> Dict[str, Any]:
        try:
            similar_feedback = await self.retrieve_similar_feedback(content, category, limit=5)
            historical_issues = await self.retrieve_historical_issues(content, category, limit=5)
            
            return {
                "similar_feedback": similar_feedback,
                "historical_issues": historical_issues,
                "context_summary": f"Found {len(similar_feedback)} similar feedback items and {len(historical_issues)} historical issues",
            }
            
        except Exception as e:
            log.error(f"Error getting context for feedback: {e}")
            return {
                "similar_feedback": [],
                "historical_issues": [],
                "context_summary": "Error retrieving context",
            }

    async def cleanup_old_memories(self, retention_days: int = 365) -> int:
        try:
            from datetime import datetime, timedelta
            from app.utils.date_utils import utc_now, is_expired
            
            cutoff_date = utc_now() - timedelta(days=retention_days)
            
            all_memories = await self.memory_repo.list_all(limit=10000)
            
            deleted_count = 0
            for memory in all_memories:
                created_at = memory.get("created_at")
                if created_at and is_expired(created_at, retention_days * 24 * 60 * 60):
                    await self.memory_repo.delete(memory["id"])
                    deleted_count += 1
            
            log.info(f"Cleaned up {deleted_count} old memories")
            
            return deleted_count
            
        except Exception as e:
            log.error(f"Error cleaning up old memories: {e}")
            return 0


cognee_manager = CogneeManager()
