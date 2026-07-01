"""
Insight generation tasks

This module defines async tasks for insight generation.
"""

from app.tasks.async_tasks import AsyncTask
from app.graphs.insight_graph import insight_graph
from app.core.logging import log


async def generate_daily_insight_task() -> dict:
    """Task to generate daily insights."""
    log.info("Generating daily insights")
    result = await insight_graph.generate_insights(
        insight_type="daily_summary",
        time_range="day"
    )
    return result


async def generate_weekly_insight_task() -> dict:
    """Task to generate weekly insights."""
    log.info("Generating weekly insights")
    result = await insight_graph.generate_insights(
        insight_type="weekly_summary",
        time_range="week"
    )
    return result


async def generate_trending_issues_task() -> dict:
    """Task to generate trending issues report."""
    log.info("Generating trending issues")
    result = await insight_graph.generate_insights(
        insight_type="trending_issues",
        time_range="week"
    )
    return result


async def generate_feature_insights_task() -> dict:
    """Task to generate feature request insights."""
    log.info("Generating feature insights")
    result = await insight_graph.generate_insights(
        insight_type="feature_requests",
        time_range="month"
    )
    return result


# Create task objects
daily_insight_async_task = AsyncTask(
    name="daily_insight",
    func=generate_daily_insight_task,
    max_retries=3
)

weekly_insight_async_task = AsyncTask(
    name="weekly_insight",
    func=generate_weekly_insight_task,
    max_retries=3
)

trending_issues_async_task = AsyncTask(
    name="trending_issues",
    func=generate_trending_issues_task,
    max_retries=3
)

feature_insights_async_task = AsyncTask(
    name="feature_insights",
    func=generate_feature_insights_task,
    max_retries=3
)
