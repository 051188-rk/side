from typing import Dict, Any, Optional, List
from app.agents.base_agent import BaseAgent
from app.integrations.cognee_integration import cognee_integration
from app.repositories.memory_repository import MemoryRepository
from app.core.logging import log


class MemoryAgent(BaseAgent):
    def __init__(self):
        super().__init__("memory_agent")
        self.memory_repo = MemoryRepository()

    async def _execute(
        self,
        input_data: Dict[str, Any],
        feedback_id: Optional[str] = None,
        ticket_id: Optional[str] = None
    ) -> Dict[str, Any]:
        content = input_data.get("content", "")
        memory_type = input_data.get("memory_type", "general")
        related_entities = input_data.get("related_entities", [])
        
        if not content:
            raise ValueError("Content is required")
        
        memory_id = await self._store_in_memory(
            content=content,
            memory_type=memory_type,
            related_entities=related_entities,
            feedback_id=feedback_id,
            ticket_id=ticket_id
        )
        
        log.info(f"Stored memory {memory_id} for feedback {feedback_id} / ticket {ticket_id}")
        
        return {
            "memory_id": memory_id,
            "memory_type": memory_type,
            "status": "stored",
        }

    async def _store_in_memory(
        self,
        content: str,
        memory_type: str,
        related_entities: List[str],
        feedback_id: Optional[str] = None,
        ticket_id: Optional[str] = None
    ) -> str:
        try:
            cognee_memory_id = await cognee_integration.store_memory(
                content=content,
                memory_type=memory_type,
                metadata={
                    "feedback_id": feedback_id,
                    "ticket_id": ticket_id,
                }
            )
            
            local_memory_id = await self.memory_repo.create_memory(
                memory_type=memory_type,
                content=content,
                metadata={
                    "cognee_memory_id": cognee_memory_id,
                    "feedback_id": feedback_id,
                    "ticket_id": ticket_id,
                },
                related_entities=related_entities
            )
            
            return local_memory_id
            
        except Exception as e:
            log.error(f"Error storing in memory: {e}")
            return ""

    async def retrieve_relevant_memory(
        self,
        query: str,
        memory_type: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        try:
            memories = await cognee_integration.retrieve_memory(
                query=query,
                memory_type=memory_type,
                limit=limit
            )
            
            log.info(f"Retrieved {len(memories)} relevant memories")
            return memories
            
        except Exception as e:
            log.error(f"Error retrieving memory: {e}")
            return []

    async def retrieve_historical_context(
        self,
        query: str,
        entity_id: Optional[str] = None
    ) -> Dict[str, Any]:
        try:
            memories = await self.retrieve_relevant_memory(query, limit=20)
            
            if entity_id:
                entity_memories = await self.memory_repo.get_by_entity(entity_id, limit=10)
                memories.extend(entity_memories)
            
            patterns = await cognee_integration.detect_patterns(
                memory_type=query.split()[0] if query else None
            )
            
            return {
                "memories": memories,
                "patterns": patterns,
                "context_summary": self._summarize_context(memories),
            }
            
        except Exception as e:
            log.error(f"Error retrieving historical context: {e}")
            return {"memories": [], "patterns": [], "context_summary": ""}

    def _summarize_context(self, memories: List[Dict[str, Any]]) -> str:
        if not memories:
            return "No relevant historical context found."
        
        summary_parts = []
        summary_parts.append(f"Found {len(memories)} relevant historical items.")
        
        memory_types = {}
        for memory in memories:
            mem_type = memory.get("memory_type", "unknown")
            memory_types[mem_type] = memory_types.get(mem_type, 0) + 1
        
        if memory_types:
            summary_parts.append("Memory types: " + ", ".join(f"{k}: {v}" for k, v in memory_types.items()))
        
        return " ".join(summary_parts)

    async def create_knowledge_graph(
        self,
        entities: List[Dict[str, Any]],
        relationships: List[Dict[str, Any]]
    ) -> str:
        try:
            graph_id = await cognee_integration.create_knowledge_graph(
                entities=entities,
                relationships=relationships
            )
            
            log.info(f"Created knowledge graph {graph_id}")
            return graph_id
            
        except Exception as e:
            log.error(f"Error creating knowledge graph: {e}")
            return ""
