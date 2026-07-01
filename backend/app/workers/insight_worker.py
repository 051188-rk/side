import asyncio
from typing import Optional
from datetime import datetime, timedelta
from app.graphs.insight_graph import insight_graph
from app.repositories.daily_report_repository import DailyReportRepository
from app.core.logging import log
from app.utils.date_utils import utc_now


class InsightWorker:
    def __init__(self, daily_report_time: str = "00:00"):
        self.daily_report_time = daily_report_time
        self.running = False
        self.daily_report_repo = DailyReportRepository()

    async def start(self):
        self.running = True
        log.info("Insight worker started")
        
        while self.running:
            try:
                await self._check_and_generate_reports()
            except Exception as e:
                log.error(f"Error in insight worker: {e}")
            
            await asyncio.sleep(60)

    async def stop(self):
        self.running = False
        log.info("Insight worker stopped")

    async def _check_and_generate_reports(self):
        now = utc_now()
        current_time = now.strftime("%H:%M")
        
        if current_time == self.daily_report_time:
            await self._generate_daily_report()
            await self._generate_weekly_summary()

    async def _generate_daily_report(self):
        try:
            today = utc_now()
            existing_report = await self.daily_report_repo.get_by_date(today)
            
            if existing_report:
                log.info("Daily report already exists for today")
                return
            
            result = await insight_graph.generate_insights(
                insight_type="daily_summary",
                time_range="day"
            )
            
            await self.daily_report_repo.create_report(
                report_date=today,
                report_type="daily",
                data=result
            )
            
            log.info("Daily report generated successfully")
            
        except Exception as e:
            log.error(f"Error generating daily report: {e}")

    async def _generate_weekly_summary(self):
        try:
            today = utc_now()
            weekday = today.weekday()
            
            if weekday != 0:
                return
            
            result = await insight_graph.generate_insights(
                insight_type="weekly_summary",
                time_range="week"
            )
            
            await self.daily_report_repo.create_report(
                report_date=today,
                report_type="weekly",
                data=result
            )
            
            log.info("Weekly summary generated successfully")
            
        except Exception as e:
            log.error(f"Error generating weekly summary: {e}")

    async def generate_insights_on_demand(self, insight_type: str = "daily_summary"):
        try:
            result = await insight_graph.generate_insights(
                insight_type=insight_type,
                time_range="week"
            )
            
            log.info(f"On-demand insights generated: {insight_type}")
            return result
            
        except Exception as e:
            log.error(f"Error generating on-demand insights: {e}")
            raise


insight_worker = InsightWorker()
