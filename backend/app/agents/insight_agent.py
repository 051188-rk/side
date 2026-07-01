from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from app.agents.base_agent import BaseAgent
from app.integrations.llm_provider import llm_provider
from app.repositories.feedback_repository import FeedbackRepository
from app.repositories.ticket_repository import TicketRepository
from app.repositories.analytics_repository import AnalyticsRepository
from app.core.logging import log
from app.utils.date_utils import get_start_of_week, get_start_of_month, utc_now


class InsightAgent(BaseAgent):
    def __init__(self):
        super().__init__("insight_agent")
        self.feedback_repo = FeedbackRepository()
        self.ticket_repo = TicketRepository()
        self.analytics_repo = AnalyticsRepository()

    async def _execute(
        self,
        input_data: Dict[str, Any],
        feedback_id: Optional[str] = None,
        ticket_id: Optional[str] = None
    ) -> Dict[str, Any]:
        insight_type = input_data.get("insight_type", "daily_summary")
        time_range = input_data.get("time_range", "week")
        
        if insight_type == "daily_summary":
            return await self._generate_daily_summary()
        elif insight_type == "weekly_summary":
            return await self._generate_weekly_summary()
        elif insight_type == "trending_issues":
            return await self._generate_trending_issues()
        elif insight_type == "top_bugs":
            return await self._generate_top_bugs()
        elif insight_type == "feature_requests":
            return await self._generate_feature_requests()
        else:
            return await self._generate_executive_summary()

    async def _generate_daily_summary(self) -> Dict[str, Any]:
        today = utc_now()
        start = get_start_of_day(today)
        
        feedback_count = len(await self.feedback_repo.get_by_date_range(start, today, limit=1000))
        tickets_created = len(await self.ticket_repo.list_all(limit=1000))
        
        system_prompt = "Generate a daily summary of feedback activity. Be concise and highlight key trends."
        prompt = f"Generate a daily summary for today with {feedback_count} feedback items and {tickets_created} tickets created."
        
        summary = await llm_provider.generate(prompt, system_prompt)
        
        return {
            "summary_type": "daily",
            "date": today.isoformat(),
            "feedback_count": feedback_count,
            "tickets_created": tickets_created,
            "summary": summary,
        }

    async def _generate_weekly_summary(self) -> Dict[str, Any]:
        today = utc_now()
        start = get_start_of_week(today)
        
        feedback = await self.feedback_repo.get_by_date_range(start, today, limit=1000)
        tickets = await self.ticket_repo.list_all(limit=1000)
        
        categories = {}
        for item in feedback:
            category = item.get("metadata", {}).get("category", "Other")
            categories[category] = categories.get(category, 0) + 1
        
        system_prompt = "Generate a weekly summary of feedback activity. Highlight trends, top issues, and patterns."
        prompt = f"Generate a weekly summary with {len(feedback)} feedback items and {len(tickets)} tickets. Categories: {categories}"
        
        summary = await llm_provider.generate(prompt, system_prompt)
        
        return {
            "summary_type": "weekly",
            "date_range": f"{start.isoformat()} to {today.isoformat()}",
            "feedback_count": len(feedback),
            "tickets_created": len(tickets),
            "categories": categories,
            "summary": summary,
        }

    async def _generate_trending_issues(self) -> Dict[str, Any]:
        today = utc_now()
        start = today - timedelta(days=7)
        
        feedback = await self.feedback_repo.get_by_date_range(start, today, limit=1000)
        
        system_prompt = """Identify trending issues from the feedback data. Look for:
- Recurring themes
- Common complaints
- Emerging patterns
- High-severity issues

Respond with a JSON object containing:
- trending_issues: a list of trending issues with descriptions
- trend_score: a score indicating how strong the trend is
- affected_users: estimated number of affected users"""
        
        feedback_text = "\n".join([f.get("content", "") for f in feedback[:50]])
        prompt = f"Identify trending issues from this feedback:\n\n{feedback_text}"
        
        schema = {
            "type": "object",
            "properties": {
                "trending_issues": {"type": "array", "items": {"type": "string"}},
                "trend_score": {"type": "number"},
                "affected_users": {"type": "number"}
            },
            "required": ["trending_issues", "trend_score", "affected_users"]
        }
        
        result = await llm_provider.generate_structured(prompt, schema, system_prompt)
        
        return {
            "insight_type": "trending_issues",
            "date_range": f"{start.isoformat()} to {today.isoformat()}",
            "trending_issues": result["trending_issues"],
            "trend_score": result["trend_score"],
            "affected_users": result["affected_users"],
        }

    async def _generate_top_bugs(self) -> Dict[str, Any]:
        tickets = await self.ticket_repo.get_by_category("Bug", limit=100)
        
        system_prompt = """Analyze the bug tickets and identify the top bugs by:
- Severity
- Priority score
- Number of duplicates
- Impact

Respond with a JSON object containing:
- top_bugs: a list of top bugs with titles and descriptions
- severity_breakdown: breakdown by severity level
- recommendation: recommended action items"""
        
        tickets_text = "\n".join([f"{t.get('title')}: {t.get('description')}" for t in tickets[:20]])
        prompt = f"Analyze these bug tickets:\n\n{tickets_text}"
        
        schema = {
            "type": "object",
            "properties": {
                "top_bugs": {"type": "array", "items": {"type": "object"}},
                "severity_breakdown": {"type": "object"},
                "recommendation": {"type": "string"}
            },
            "required": ["top_bugs", "severity_breakdown", "recommendation"]
        }
        
        result = await llm_provider.generate_structured(prompt, schema, system_prompt)
        
        return {
            "insight_type": "top_bugs",
            "total_bugs": len(tickets),
            "top_bugs": result["top_bugs"],
            "severity_breakdown": result["severity_breakdown"],
            "recommendation": result["recommendation"],
        }

    async def _generate_feature_requests(self) -> Dict[str, Any]:
        tickets = await self.ticket_repo.get_by_category("Feature Request", limit=100)
        
        system_prompt = """Analyze the feature request tickets and identify:
- Most requested features
- Feature themes
- Implementation complexity estimates

Respond with a JSON object containing:
- top_features: a list of most requested features
- feature_themes: themes that emerge from the requests
- implementation_priority: suggested implementation order"""
        
        tickets_text = "\n".join([f"{t.get('title')}: {t.get('description')}" for t in tickets[:20]])
        prompt = f"Analyze these feature requests:\n\n{tickets_text}"
        
        schema = {
            "type": "object",
            "properties": {
                "top_features": {"type": "array", "items": {"type": "string"}},
                "feature_themes": {"type": "array", "items": {"type": "string"}},
                "implementation_priority": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["top_features", "feature_themes", "implementation_priority"]
        }
        
        result = await llm_provider.generate_structured(prompt, schema, system_prompt)
        
        return {
            "insight_type": "feature_requests",
            "total_requests": len(tickets),
            "top_features": result["top_features"],
            "feature_themes": result["feature_themes"],
            "implementation_priority": result["implementation_priority"],
        }

    async def _generate_executive_summary(self) -> Dict[str, Any]:
        today = utc_now()
        start = get_start_of_month(today)
        
        feedback = await self.feedback_repo.get_by_date_range(start, today, limit=1000)
        tickets = await self.ticket_repo.list_all(limit=1000)
        
        system_prompt = """Generate an executive summary for leadership. Include:
- Key metrics
- Major issues
- Positive highlights
- Recommendations

Be professional, concise, and actionable."""
        
        prompt = f"""Generate an executive summary for the period {start.isoformat()} to {today.isoformat()}:
- Feedback items: {len(feedback)}
- Tickets created: {len(tickets)}"""
        
        summary = await llm_provider.generate(prompt, system_prompt)
        
        return {
            "insight_type": "executive_summary",
            "period": f"{start.isoformat()} to {today.isoformat()}",
            "feedback_count": len(feedback),
            "tickets_created": len(tickets),
            "summary": summary,
        }
