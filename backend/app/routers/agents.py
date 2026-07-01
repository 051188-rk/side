from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.common import SuccessResponse, AgentInput, AgentOutput
from app.graphs.feedback_graph import feedback_graph
from app.graphs.insight_graph import insight_graph
from app.core.security import get_current_user, require_user
from app.core.logging import log

router = APIRouter()


@router.post("/process-feedback", response_model=SuccessResponse)
async def process_feedback_agent(
    input_data: AgentInput,
    current_user: dict = Depends(require_user())
):
    try:
        result = await feedback_graph.process(
            content=input_data.content or "",
            context=input_data.context
        )
        
        return SuccessResponse(
            success=True,
            message="Feedback processed successfully",
            data=result
        )
    except Exception as e:
        log.error(f"Feedback processing error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/generate-insights", response_model=SuccessResponse)
async def generate_insights_agent(
    insight_type: str = "daily_summary",
    time_range: str = "week",
    current_user: dict = Depends(require_user())
):
    try:
        result = await insight_graph.generate_insights(
            insight_type=insight_type,
            time_range=time_range
        )
        
        return SuccessResponse(
            success=True,
            message="Insights generated successfully",
            data=result
        )
    except Exception as e:
        log.error(f"Insight generation error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/collect-feedback", response_model=SuccessResponse)
async def collect_feedback(
    source: str,
    channel_id: str = None,
    limit: int = 100,
    current_user: dict = Depends(require_admin())
):
    try:
        from app.agents import FeedbackCollectorAgent
        collector = FeedbackCollectorAgent()
        
        if source == "discord" and channel_id:
            result = await collector.collect_from_discord(channel_id, limit)
        elif source == "telegram" and channel_id:
            result = await collector.collect_from_telegram(channel_id, limit)
        elif source == "gmail":
            result = await collector.collect_from_gmail("is:unread", limit)
        elif source == "github":
            result = await collector.collect_from_github("owner/repo", "open")
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid source")
        
        return SuccessResponse(
            success=True,
            message=f"Collected feedback from {source}",
            data=result
        )
    except Exception as e:
        log.error(f"Feedback collection error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
