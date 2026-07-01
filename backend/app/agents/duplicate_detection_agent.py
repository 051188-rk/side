from typing import Dict, Any, Optional, List
from app.agents.base_agent import BaseAgent
from app.integrations.cognee_integration import cognee_integration
from app.repositories.feedback_repository import FeedbackRepository
from app.repositories.duplicate_cluster_repository import DuplicateClusterRepository
from app.utils.helpers import calculate_similarity_score
from app.core.logging import log


class DuplicateDetectionAgent(BaseAgent):
    def __init__(self):
        super().__init__("duplicate_detection_agent")
        self.feedback_repo = FeedbackRepository()
        self.cluster_repo = DuplicateClusterRepository()
        self.similarity_threshold = 0.8

    async def _execute(
        self,
        input_data: Dict[str, Any],
        feedback_id: Optional[str] = None,
        ticket_id: Optional[str] = None
    ) -> Dict[str, Any]:
        content = input_data.get("content", "")
        category = input_data.get("category", "")
        
        if not content:
            raise ValueError("Content is required")
        
        similar_feedback = await self._find_similar_feedback(content, category)
        
        if similar_feedback:
            cluster_id = await self._add_to_cluster(feedback_id, similar_feedback, content, category)
            log.info(f"Added feedback {feedback_id} to duplicate cluster {cluster_id}")
            
            return {
                "is_duplicate": True,
                "cluster_id": cluster_id,
                "similar_feedback": similar_feedback,
                "similarity_score": similar_feedback.get("similarity_score", 0),
            }
        else:
            log.info(f"No duplicates found for feedback {feedback_id}")
            
            return {
                "is_duplicate": False,
                "cluster_id": None,
                "similar_feedback": [],
            }

    async def _find_similar_feedback(
        self,
        content: str,
        category: str,
        limit: int = 10
    ) -> Optional[Dict[str, Any]]:
        try:
            memories = await cognee_integration.retrieve_memory(
                query=content,
                memory_type=f"feedback_{category}",
                limit=limit,
                similarity_threshold=self.similarity_threshold
            )
            
            if memories:
                best_match = memories[0]
                return {
                    "feedback_id": best_match.get("metadata", {}).get("feedback_id"),
                    "similarity_score": best_match.get("similarity", 0),
                    "cluster_id": best_match.get("metadata", {}).get("cluster_id"),
                }
            
            return None
            
        except Exception as e:
            log.error(f"Error finding similar feedback: {e}")
            return None

    async def _add_to_cluster(
        self,
        feedback_id: str,
        similar_feedback: Dict[str, Any],
        content: str,
        category: str
    ) -> str:
        existing_cluster_id = similar_feedback.get("cluster_id")
        
        if existing_cluster_id:
            cluster = await self.cluster_repo.get_by_id(existing_cluster_id)
            if cluster:
                await self.cluster_repo.add_feedback(existing_cluster_id, feedback_id)
                return existing_cluster_id
        
        new_cluster_id = await self.cluster_repo.create_cluster(
            representative_feedback_id=similar_feedback.get("feedback_id"),
            similarity_threshold=self.similarity_threshold,
            feedback_ids=[similar_feedback.get("feedback_id"), feedback_id],
            title=f"Generated from {category}",
            description=content[:200]
        )
        
        return new_cluster_id

    async def store_feedback_in_memory(
        self,
        feedback_id: str,
        content: str,
        category: str,
        cluster_id: Optional[str] = None
    ) -> str:
        try:
            memory_id = await cognee_integration.store_memory(
                content=content,
                memory_type=f"feedback_{category}",
                metadata={
                    "feedback_id": feedback_id,
                    "category": category,
                    "cluster_id": cluster_id,
                }
            )
            
            log.info(f"Stored feedback {feedback_id} in memory: {memory_id}")
            return memory_id
            
        except Exception as e:
            log.error(f"Error storing feedback in memory: {e}")
            return ""

    async def find_duplicate_clusters(self, min_count: int = 5) -> List[Dict[str, Any]]:
        clusters = await self.cluster_repo.get_large_clusters(min_count)
        return clusters
