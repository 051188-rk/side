from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from typing import List
from app.schemas.feedback import FeedbackResponse, FeedbackCreate
from app.schemas.common import SuccessResponse
from app.repositories.feedback_repository import FeedbackRepository
from app.core.security import get_current_user, require_user
from app.core.logging import log
from app.graphs.feedback_graph import feedback_graph

router = APIRouter()
feedback_repo = FeedbackRepository()


@router.post("/", response_model=FeedbackResponse)
async def create_feedback(
    feedback_data: FeedbackCreate,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    feedback_id = await feedback_repo.create_feedback(
        source=feedback_data.source,
        content=feedback_data.content,
        customer_id=feedback_data.customer_id,
        metadata=feedback_data.metadata
    )
    
    background_tasks.add_task(process_feedback_async, feedback_id, feedback_data.content)
    
    feedback = await feedback_repo.get_by_id(feedback_id)
    return feedback


async def process_feedback_async(feedback_id: str, content: str):
    try:
        result = await feedback_graph.process(content, {"feedback_id": feedback_id})
        log.info(f"Processed feedback {feedback_id} via graph: {result}")
    except Exception as e:
        log.error(f"Failed to process feedback {feedback_id}: {e}")


@router.get("/{feedback_id}", response_model=FeedbackResponse)
async def get_feedback(
    feedback_id: str,
    current_user: dict = Depends(require_user())
):
    feedback = await feedback_repo.get_by_id(feedback_id)
    if not feedback:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Feedback not found")
    return feedback


@router.get("/", response_model=List[FeedbackResponse])
async def list_feedback(
    limit: int = 100,
    offset: int = 0,
    status: str = None,
    current_user: dict = Depends(require_user())
):
    if status:
        feedback_list = await feedback_repo.get_by_status(status, limit=limit)
    else:
        feedback_list = await feedback_repo.list_all(limit=limit, offset=offset)
    return feedback_list


@router.post("/{feedback_id}/process", response_model=SuccessResponse)
async def process_feedback(
    feedback_id: str,
    current_user: dict = Depends(require_user())
):
    feedback = await feedback_repo.get_by_id(feedback_id)
    if not feedback:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Feedback not found")
    
    result = await feedback_graph.process(feedback["content"], {"feedback_id": feedback_id})
    
    return SuccessResponse(
        success=True,
        message="Feedback processed successfully",
        data=result
    )
