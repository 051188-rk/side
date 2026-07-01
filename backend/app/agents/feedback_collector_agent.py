from typing import Dict, Any, Optional
from app.agents.base_agent import BaseAgent
from app.integrations.discord_integration import discord_integration
from app.integrations.telegram_integration import telegram_integration
from app.integrations.gmail_integration import gmail_integration
from app.integrations.github_integration import github_integration
from app.repositories.feedback_repository import FeedbackRepository
from app.repositories.customer_repository import CustomerRepository
from app.core.logging import log


class FeedbackCollectorAgent(BaseAgent):
    def __init__(self):
        super().__init__("feedback_collector")
        self.feedback_repo = FeedbackRepository()
        self.customer_repo = CustomerRepository()

    async def _execute(
        self,
        input_data: Dict[str, Any],
        feedback_id: Optional[str] = None,
        ticket_id: Optional[str] = None
    ) -> Dict[str, Any]:
        source = input_data.get("source")
        content = input_data.get("content")
        customer_info = input_data.get("customer_info", {})
        
        if not source or not content:
            raise ValueError("Source and content are required")
        
        customer_id = await self._get_or_create_customer(source, customer_info)
        
        feedback_id = await self.feedback_repo.create_feedback(
            source=source,
            content=content,
            customer_id=customer_id,
            metadata=input_data.get("metadata", {})
        )
        
        log.info(f"Collected feedback from {source}: {feedback_id}")
        
        return {
            "feedback_id": feedback_id,
            "customer_id": customer_id,
            "source": source,
            "status": "collected",
        }

    async def _get_or_create_customer(self, source: str, customer_info: Dict[str, Any]) -> str:
        email = customer_info.get("email")
        external_id = customer_info.get("external_id")
        
        if email:
            customer = await self.customer_repo.get_by_email(email)
            if customer:
                return customer["id"]
        
        customer_id = await self.customer_repo.create_customer(
            email=email or f"{source}_user_{external_id}",
            name=customer_info.get("name"),
            source=source,
            external_id=external_id,
            metadata=customer_info
        )
        
        return customer_id

    async def collect_from_discord(self, channel_id: str, limit: int = 100) -> Dict[str, Any]:
        messages = await discord_integration.get_channel_messages(channel_id, limit)
        collected = []
        
        for msg in messages:
            result = await self.execute({
                "source": "discord",
                "content": msg["content"],
                "customer_info": {
                    "external_id": msg["author"],
                    "name": msg["author"],
                },
                "metadata": {
                    "message_id": msg["id"],
                    "channel_id": channel_id,
                    "timestamp": msg["timestamp"],
                }
            })
            collected.append(result)
        
        return {"collected_count": len(collected), "results": collected}

    async def collect_from_telegram(self, chat_id: str, limit: int = 100) -> Dict[str, Any]:
        messages = await telegram_integration.get_chat_history(chat_id, limit)
        collected = []
        
        for msg in messages:
            result = await self.execute({
                "source": "telegram",
                "content": msg.get("text", ""),
                "customer_info": {
                    "external_id": str(msg.get("from_user", {}).get("id", "")),
                    "name": msg.get("from_user", {}).get("username", ""),
                },
                "metadata": {
                    "message_id": msg["message_id"],
                    "chat_id": chat_id,
                    "date": msg["date"],
                }
            })
            collected.append(result)
        
        return {"collected_count": len(collected), "results": collected}

    async def collect_from_gmail(self, query: str, limit: int = 100) -> Dict[str, Any]:
        emails = await gmail_integration.search_emails(query, limit)
        collected = []
        
        for email in emails:
            result = await self.execute({
                "source": "gmail",
                "content": email["body"],
                "customer_info": {
                    "email": email["from"],
                    "name": email["from"].split("<")[0].strip() if "<" in email["from"] else email["from"],
                },
                "metadata": {
                    "subject": email["subject"],
                    "message_id": email["id"],
                    "date": email["date"],
                }
            })
            collected.append(result)
        
        return {"collected_count": len(collected), "results": collected}

    async def collect_from_github(self, repo_name: str, state: str = "open") -> Dict[str, Any]:
        issues = await github_integration.get_issues(repo_name, state)
        collected = []
        
        for issue in issues:
            result = await self.execute({
                "source": "github",
                "content": issue["body"],
                "customer_info": {
                    "external_id": issue["user"],
                    "name": issue["user"],
                },
                "metadata": {
                    "issue_number": issue["number"],
                    "title": issue["title"],
                    "url": issue["url"],
                    "labels": issue["labels"],
                }
            })
            collected.append(result)
        
        return {"collected_count": len(collected), "results": collected}
