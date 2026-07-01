import asyncio
from typing import Optional
from app.integrations.gmail_integration import gmail_integration
from app.agents import FeedbackCollectorAgent
from app.core.logging import log
from app.core.exceptions import ExternalServiceException
from datetime import datetime, timedelta


class EmailWorker:
    def __init__(self, poll_interval: int = 300):
        self.poll_interval = poll_interval
        self.running = False
        self.collector_agent = FeedbackCollectorAgent()

    async def start(self):
        self.running = True
        log.info("Email worker started")
        
        while self.running:
            try:
                await self._poll_emails()
            except Exception as e:
                log.error(f"Error in email worker: {e}")
            
            await asyncio.sleep(self.poll_interval)

    async def stop(self):
        self.running = False
        log.info("Email worker stopped")

    async def _poll_emails(self):
        try:
            query = "is:unread"
            emails = await gmail_integration.search_emails(query, limit=50)
            
            log.info(f"Found {len(emails)} unread emails")
            
            for email in emails:
                try:
                    await self._process_email(email)
                    await gmail_integration.mark_as_read(email["id"])
                    await gmail_integration.add_label(email["id"], "SIDE_PROCESSED")
                except Exception as e:
                    log.error(f"Error processing email {email['id']}: {e}")
                    
        except Exception as e:
            log.error(f"Error polling emails: {e}")
            raise

    async def _process_email(self, email: dict):
        content = email.get("body", "")
        from_email = email.get("from", "")
        subject = email.get("subject", "")
        
        if not content:
            return
        
        result = await self.collector_agent.execute({
            "source": "gmail",
            "content": content,
            "customer_info": {
                "email": from_email,
                "name": from_email.split("<")[0].strip() if "<" in from_email else from_email,
            },
            "metadata": {
                "subject": subject,
                "message_id": email["id"],
                "date": email["date"],
            }
        })
        
        log.info(f"Processed email from {from_email}: {result.get('success')}")

    async def process_single_email(self, message_id: str):
        try:
            email = await gmail_integration.get_message(message_id)
            await self._process_email(email)
            await gmail_integration.mark_as_read(message_id)
            return True
        except Exception as e:
            log.error(f"Error processing single email {message_id}: {e}")
            return False


email_worker = EmailWorker()
