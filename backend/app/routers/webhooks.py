from fastapi import APIRouter, Request, HTTPException, status, BackgroundTasks
from app.schemas.common import SuccessResponse
from app.integrations.webhook_receiver import webhook_receiver
from app.agents import FeedbackCollectorAgent
from app.core.logging import log

router = APIRouter()
collector_agent = FeedbackCollectorAgent()


@router.post("/discord", response_model=SuccessResponse)
async def discord_webhook(
    request: Request,
    background_tasks: BackgroundTasks
):
    try:
        payload = await webhook_receiver.receive_discord_webhook(request)
        
        background_tasks.add_task(process_discord_webhook, payload)
        
        return SuccessResponse(success=True, message="Discord webhook received")
    except Exception as e:
        log.error(f"Discord webhook error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


async def process_discord_webhook(payload: dict):
    try:
        if payload.get("type") == 1:
            return
        
        content = payload.get("d", {}).get("content", "")
        author = payload.get("d", {}).get("author", {})
        channel_id = payload.get("d", {}).get("channel_id")
        
        if content:
            await collector_agent.execute({
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
    except Exception as e:
        log.error(f"Error processing Discord webhook: {e}")


@router.post("/telegram", response_model=SuccessResponse)
async def telegram_webhook(
    request: Request,
    background_tasks: BackgroundTasks
):
    try:
        payload = await webhook_receiver.receive_telegram_webhook(request)
        
        background_tasks.add_task(process_telegram_webhook, payload)
        
        return SuccessResponse(success=True, message="Telegram webhook received")
    except Exception as e:
        log.error(f"Telegram webhook error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


async def process_telegram_webhook(payload: dict):
    try:
        message = payload.get("message", {})
        text = message.get("text", "")
        from_user = message.get("from", {})
        chat = message.get("chat", {})
        
        if text:
            await collector_agent.execute({
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
    except Exception as e:
        log.error(f"Error processing Telegram webhook: {e}")


@router.post("/github", response_model=SuccessResponse)
async def github_webhook(
    request: Request,
    background_tasks: BackgroundTasks
):
    try:
        webhook_data = await webhook_receiver.receive_github_webhook(request)
        
        background_tasks.add_task(process_github_webhook, webhook_data)
        
        return SuccessResponse(success=True, message="GitHub webhook received")
    except Exception as e:
        log.error(f"GitHub webhook error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


async def process_github_webhook(webhook_data: dict):
    try:
        event_type = webhook_data.get("event_type")
        payload = webhook_data.get("payload", {})
        
        if event_type == "issues":
            action = payload.get("action")
            issue = payload.get("issue", {})
            
            if action in ["opened", "created", "edited"]:
                await collector_agent.execute({
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
    except Exception as e:
        log.error(f"Error processing GitHub webhook: {e}")


@router.post("/gmail", response_model=SuccessResponse)
async def gmail_webhook(
    request: Request,
    background_tasks: BackgroundTasks
):
    try:
        payload = await webhook_receiver.receive_gmail_webhook(request)
        
        background_tasks.add_task(process_gmail_webhook, payload)
        
        return SuccessResponse(success=True, message="Gmail webhook received")
    except Exception as e:
        log.error(f"Gmail webhook error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


async def process_gmail_webhook(payload: dict):
    try:
        message_id = payload.get("message", {}).get("data")
        
        if message_id:
            from app.integrations.gmail_integration import gmail_integration
            email_data = await gmail_integration.get_message(message_id)
            
            if email_data:
                await collector_agent.execute({
                    "source": "gmail",
                    "content": email_data.get("body", ""),
                    "customer_info": {
                        "email": email_data.get("from"),
                        "name": email_data.get("from").split("<")[0].strip() if "<" in email_data.get("from", "") else email_data.get("from"),
                    },
                    "metadata": {
                        "subject": email_data.get("subject"),
                        "message_id": message_id,
                        "date": email_data.get("date"),
                    }
                })
    except Exception as e:
        log.error(f"Error processing Gmail webhook: {e}")


@router.post("/generic/{secret}", response_model=SuccessResponse)
async def generic_webhook(
    secret: str,
    request: Request,
    background_tasks: BackgroundTasks
):
    try:
        from app.config import settings
        payload = await webhook_receiver.receive_generic_webhook(request, secret)
        
        background_tasks.add_task(process_generic_webhook, payload)
        
        return SuccessResponse(success=True, message="Generic webhook received")
    except Exception as e:
        log.error(f"Generic webhook error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


async def process_generic_webhook(payload: dict):
    try:
        source = payload.get("source", "generic")
        content = payload.get("content", "")
        
        if content:
            await collector_agent.execute({
                "source": source,
                "content": content,
                "customer_info": payload.get("customer_info", {}),
                "metadata": payload.get("metadata", {}),
            })
    except Exception as e:
        log.error(f"Error processing generic webhook: {e}")
