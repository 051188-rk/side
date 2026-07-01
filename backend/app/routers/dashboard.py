from fastapi import APIRouter, Depends
from typing import Dict, Any
from datetime import datetime, timedelta
from app.schemas.common import SuccessResponse
from app.repositories.feedback_repository import FeedbackRepository
from app.repositories.ticket_repository import TicketRepository
from app.repositories.analytics_repository import AnalyticsRepository
from app.repositories.daily_report_repository import DailyReportRepository
from app.core.security import get_current_user, require_user
from app.core.logging import log
from app.utils.date_utils import get_start_of_day, get_end_of_day, get_start_of_week, get_start_of_month, utc_now

router = APIRouter()
feedback_repo = FeedbackRepository()
ticket_repo = TicketRepository()
analytics_repo = AnalyticsRepository()
daily_report_repo = DailyReportRepository()


@router.get("/overview", response_model=SuccessResponse)
async def get_dashboard_overview(
    current_user: dict = Depends(require_user())
):
    today = utc_now()
    start_of_day = get_start_of_day(today)
    end_of_day = get_end_of_day(today)
    
    feedback_today = await feedback_repo.get_by_date_range(start_of_day, end_of_day, limit=1000)
    tickets_total = await ticket_repo.count()
    tickets_open = await ticket_repo.get_by_status("open", limit=1000)
    tickets_high_priority = await ticket_repo.get_high_priority(0.7, limit=100)
    
    return SuccessResponse(
        success=True,
        message="Dashboard overview retrieved",
        data={
            "feedback_today": len(feedback_today),
            "tickets_total": tickets_total,
            "tickets_open": len(tickets_open),
            "tickets_high_priority": len(tickets_high_priority),
            "date": today.isoformat(),
        }
    )


@router.get("/charts/feedback-volume", response_model=SuccessResponse)
async def get_feedback_volume_chart(
    days: int = 30,
    current_user: dict = Depends(require_user())
):
    today = utc_now()
    start_date = today - timedelta(days=days)
    
    daily_counts = []
    for i in range(days):
        date = start_date + timedelta(days=i)
        start = get_start_of_day(date)
        end = get_end_of_day(date)
        count = len(await feedback_repo.get_by_date_range(start, end, limit=1000))
        daily_counts.append({
            "date": date.isoformat(),
            "count": count
        })
    
    return SuccessResponse(
        success=True,
        message="Feedback volume chart retrieved",
        data={"daily_counts": daily_counts}
    )


@router.get("/charts/trending-issues", response_model=SuccessResponse)
async def get_trending_issues_chart(
    limit: int = 10,
    current_user: dict = Depends(require_user())
):
    from app.agents import InsightAgent
    insight_agent = InsightAgent()
    
    result = await insight_agent.execute({
        "insight_type": "trending_issues",
        "time_range": "week"
    })
    
    return SuccessResponse(
        success=True,
        message="Trending issues retrieved",
        data=result.get("result", {})
    )


@router.get("/charts/sentiment-graph", response_model=SuccessResponse)
async def get_sentiment_graph(
    current_user: dict = Depends(require_user())
):
    feedback_list = await feedback_repo.list_all(limit=1000)
    
    sentiment_counts = {
        "Positive": 0,
        "Neutral": 0,
        "Negative": 0,
        "Angry": 0,
        "Frustrated": 0,
        "Urgent": 0,
    }
    
    for feedback in feedback_list:
        sentiment = feedback.get("metadata", {}).get("sentiment", "Neutral")
        if sentiment in sentiment_counts:
            sentiment_counts[sentiment] += 1
    
    return SuccessResponse(
        success=True,
        message="Sentiment graph retrieved",
        data={"sentiment_counts": sentiment_counts}
    )


@router.get("/charts/category-breakdown", response_model=SuccessResponse)
async def get_category_breakdown(
    current_user: dict = Depends(require_user())
):
    tickets = await ticket_repo.list_all(limit=1000)
    
    category_counts = {}
    for ticket in tickets:
        category = ticket.get("category", "Other")
        category_counts[category] = category_counts.get(category, 0) + 1
    
    return SuccessResponse(
        success=True,
        message="Category breakdown retrieved",
        data={"category_counts": category_counts}
    )


@router.get("/reports/daily", response_model=SuccessResponse)
async def get_daily_report(
    date: str = None,
    current_user: dict = Depends(require_user())
):
    if date:
        report_date = datetime.fromisoformat(date)
    else:
        report_date = utc_now()
    
    report = await daily_report_repo.get_by_date(report_date)
    
    if not report:
        return SuccessResponse(
            success=True,
            message="No daily report found for this date",
            data=None
        )
    
    return SuccessResponse(
        success=True,
        message="Daily report retrieved",
        data=report
    )


@router.get("/reports/weekly", response_model=SuccessResponse)
async def get_weekly_report(
    current_user: dict = Depends(require_user())
):
    today = utc_now()
    start_of_week = get_start_of_week(today)
    
    reports = await daily_report_repo.get_date_range(start_of_week, today)
    
    return SuccessResponse(
        success=True,
        message="Weekly report retrieved",
        data={"reports": reports}
    )


@router.get("/statistics/customer", response_model=SuccessResponse)
async def get_customer_statistics(
    current_user: dict = Depends(require_user())
):
    from app.repositories.customer_repository import CustomerRepository
    customer_repo = CustomerRepository()
    
    total_customers = await customer_repo.count()
    
    customers_by_tier = {}
    for tier in ["standard", "premium", "enterprise"]:
        customers = await customer_repo.get_by_tier(tier, limit=1000)
        customers_by_tier[tier] = len(customers)
    
    return SuccessResponse(
        success=True,
        message="Customer statistics retrieved",
        data={
            "total_customers": total_customers,
            "customers_by_tier": customers_by_tier
        }
    )


@router.get("/statistics/issue-heatmap", response_model=SuccessResponse)
async def get_issue_heatmap(
    current_user: dict = Depends(require_user())
):
    tickets = await ticket_repo.list_all(limit=1000)
    
    heatmap_data = {}
    for ticket in tickets:
        category = ticket.get("category", "Other")
        severity = ticket.get("severity", "Medium")
        key = f"{category}_{severity}"
        heatmap_data[key] = heatmap_data.get(key, 0) + 1
    
    return SuccessResponse(
        success=True,
        message="Issue heatmap retrieved",
        data={"heatmap": heatmap_data}
    )
