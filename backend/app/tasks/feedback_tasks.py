"""
Feedback processing tasks

This module defines async tasks for feedback processing.
"""

from app.tasks.async_tasks import AsyncTask
from app.services.feedback_service import feedback_service
from app.core.logging import log


async def process_feedback_task(feedback_id: str) -> dict:
    """Task to process a single feedback item."""
    log.info(f"Processing feedback task: {feedback_id}")
    result = await feedback_service.process_feedback(feedback_id)
    return result


async def batch_process_feedback_task(feedback_ids: list) -> dict:
    """Task to process multiple feedback items in batch."""
    log.info(f"Batch processing {len(feedback_ids)} feedback items")
    results = []
    
    for feedback_id in feedback_ids:
        try:
            result = await feedback_service.process_feedback(feedback_id)
            results.append({"feedback_id": feedback_id, "success": True, "result": result})
        except Exception as e:
            log.error(f"Failed to process feedback {feedback_id}: {e}")
            results.append({"feedback_id": feedback_id, "success": False, "error": str(e)})
    
    return {
        "total": len(feedback_ids),
        "successful": sum(1 for r in results if r["success"]),
        "failed": sum(1 for r in results if not r["success"]),
        "results": results,
    }


async def collect_and_process_feedback_task(source: str, limit: int = 100) -> dict:
    """Task to collect and process feedback from a source."""
    log.info(f"Collecting feedback from {source}")
    
    from app.agents import FeedbackCollectorAgent
    collector = FeedbackCollectorAgent()
    
    if source == "discord":
        result = await collector.collect_from_discord("test_channel", limit)
    elif source == "telegram":
        result = await collector.collect_from_telegram("test_chat", limit)
    elif source == "gmail":
        result = await collector.collect_from_gmail("is:unread", limit)
    else:
        result = {"error": f"Unknown source: {source}"}
    
    return result


# Create task objects
process_feedback_async_task = AsyncTask(
    name="process_feedback",
    func=process_feedback_task,
    max_retries=3
)

batch_process_feedback_async_task = AsyncTask(
    name="batch_process_feedback",
    func=batch_process_feedback_task,
    max_retries=2
)

collect_feedback_async_task = AsyncTask(
    name="collect_feedback",
    func=collect_and_process_feedback_task,
    max_retries=3
)
