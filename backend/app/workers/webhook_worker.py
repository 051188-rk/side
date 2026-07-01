import asyncio
from typing import Dict, Any, Optional
from collections import deque
from app.core.logging import log
from app.core.exceptions import ExternalServiceException


class WebhookWorker:
    def __init__(self, queue_size: int = 1000, max_retries: int = 3):
        self.queue = deque(maxlen=queue_size)
        self.running = False
        self.max_retries = max_retries

    async def start(self):
        self.running = True
        log.info("Webhook worker started")
        
        while self.running:
            try:
                await self._process_queue()
            except Exception as e:
                log.error(f"Error in webhook worker: {e}")
            
            await asyncio.sleep(1)

    async def stop(self):
        self.running = False
        log.info("Webhook worker stopped")

    async def enqueue(self, webhook_data: Dict[str, Any]):
        if len(self.queue) >= self.queue.maxlen:
            log.warning("Webhook queue is full, dropping oldest item")
            self.queue.popleft()
        
        webhook_data["retries"] = webhook_data.get("retries", 0)
        self.queue.append(webhook_data)
        log.info(f"Enqueued webhook: {webhook_data.get('type')}")

    async def _process_queue(self):
        if not self.queue:
            return
        
        webhook_data = self.queue.popleft()
        
        try:
            await self._process_webhook(webhook_data)
            log.info(f"Successfully processed webhook: {webhook_data.get('type')}")
        except Exception as e:
            log.error(f"Error processing webhook: {e}")
            
            retries = webhook_data.get("retries", 0)
            if retries < self.max_retries:
                webhook_data["retries"] = retries + 1
                self.queue.appendleft(webhook_data)
                log.info(f"Retrying webhook (attempt {retries + 1}/{self.max_retries})")

    async def _process_webhook(self, webhook_data: Dict[str, Any]):
        webhook_type = webhook_data.get("type")
        payload = webhook_data.get("payload", {})
        
        if webhook_type == "discord":
            await self._process_discord_webhook(payload)
        elif webhook_type == "telegram":
            await self._process_telegram_webhook(payload)
        elif webhook_type == "github":
            await self._process_github_webhook(payload)
        elif webhook_type == "gmail":
            await self._process_gmail_webhook(payload)
        else:
            log.warning(f"Unknown webhook type: {webhook_type}")

    async def _process_discord_webhook(self, payload: Dict[str, Any]):
        from app.agents import FeedbackCollectorAgent
        collector = FeedbackCollectorAgent()
        
        content = payload.get("d", {}).get("content", "")
        author = payload.get("d", {}).get("author", {})
        channel_id = payload.get("d", {}).get("channel_id")
        
        if content:
            await collector.execute({
                "source": "discord",
                "content": content,
                "customer_info": {
                    "external_id": author.get("id"),
                    "name": author.get("username"),
                },
                "metadata": {
                    "channel_id": channel_id,
                    "author": author,
                }
            })

    async def _process_telegram_webhook(self, payload: Dict[str, Any]):
        from app.agents import FeedbackCollectorAgent
        collector = FeedbackCollectorAgent()
        
        message = payload.get("message", {})
        text = message.get("text", "")
        from_user = message.get("from", {})
        chat = message.get("chat", {})
        
        if text:
            await collector.execute({
                "source": "telegram",
                "content": text,
                "customer_info": {
                    "external_id": str(from_user.get("id")),
                    "name": from_user.get("username"),
                },
                "metadata": {
                    "chat_id": str(chat.get("id")),
                    "chat_type": chat.get("type"),
                }
            })

    async def _process_github_webhook(self, payload: Dict[str, Any]):
        from app.agents import FeedbackCollectorAgent
        collector = FeedbackCollectorAgent()
        
        action = payload.get("action")
        issue = payload.get("issue", {})
        
        if action in ["opened", "created", "edited"]:
            await collector.execute({
                "source": "github",
                "content": issue.get("body", ""),
                "customer_info": {
                    "external_id": issue.get("user", {}).get("login"),
                    "name": issue.get("user", {}).get("login"),
                },
                "metadata": {
                    "issue_number": issue.get("number"),
                    "title": issue.get("title"),
                    "url": issue.get("html_url"),
                    "action": action,
                }
            })

    async def _process_gmail_webhook(self, payload: Dict[str, Any]):
        from app.workers.email_worker import email_worker
        from app.integrations.gmail_integration import gmail_integration
        
        message_id = payload.get("message", {}).get("data")
        
        if message_id:
            await email_worker.process_single_email(message_id)


webhook_worker = WebhookWorker()
