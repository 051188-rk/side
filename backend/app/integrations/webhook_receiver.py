from typing import Optional, Dict, Any
from fastapi import Request, HTTPException, status
from app.integrations.discord_integration import discord_integration
from app.integrations.telegram_integration import telegram_integration
from app.integrations.github_integration import github_integration
from app.core.logging import log
from app.core.exceptions import BadRequestException
from app.utils.validators import validate_webhook_signature
import hmac
import hashlib


class WebhookReceiver:
    async def receive_discord_webhook(self, request: Request) -> Dict[str, Any]:
        try:
            signature = request.headers.get("X-Signature-Ed25519")
            if not signature:
                raise BadRequestException("Missing Discord signature")
            
            body = await request.body()
            
            if not await discord_integration.verify_webhook(signature, body):
                raise BadRequestException("Invalid Discord signature")
            
            payload = await request.json()
            log.info(f"Received Discord webhook: {payload.get('type')}")
            
            return payload
            
        except Exception as e:
            log.error(f"Failed to receive Discord webhook: {e}")
            raise

    async def receive_telegram_webhook(self, request: Request) -> Dict[str, Any]:
        try:
            secret_token = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
            if not secret_token:
                raise BadRequestException("Missing Telegram secret token")
            
            if not await telegram_integration.verify_webhook(secret_token):
                raise BadRequestException("Invalid Telegram secret token")
            
            payload = await request.json()
            log.info(f"Received Telegram webhook: update_id={payload.get('update_id')}")
            
            return payload
            
        except Exception as e:
            log.error(f"Failed to receive Telegram webhook: {e}")
            raise

    async def receive_github_webhook(self, request: Request) -> Dict[str, Any]:
        try:
            signature = request.headers.get("X-Hub-Signature-256")
            if not signature:
                raise BadRequestException("Missing GitHub signature")
            
            body = await request.body()
            
            if not await github_integration.verify_webhook(body, signature):
                raise BadRequestException("Invalid GitHub signature")
            
            payload = await request.json()
            event_type = request.headers.get("X-GitHub-Event", "unknown")
            log.info(f"Received GitHub webhook: {event_type}")
            
            return {
                "event_type": event_type,
                "payload": payload,
            }
            
        except Exception as e:
            log.error(f"Failed to receive GitHub webhook: {e}")
            raise

    async def receive_generic_webhook(
        self,
        request: Request,
        secret: str,
        signature_header: str = "X-Signature"
    ) -> Dict[str, Any]:
        try:
            signature = request.headers.get(signature_header)
            if not signature:
                raise BadRequestException(f"Missing {signature_header}")
            
            body = await request.body()
            
            if not validate_webhook_signature(body, signature, secret):
                raise BadRequestException("Invalid webhook signature")
            
            payload = await request.json()
            log.info(f"Received generic webhook")
            
            return payload
            
        except Exception as e:
            log.error(f"Failed to receive generic webhook: {e}")
            raise

    async def receive_gmail_webhook(self, request: Request) -> Dict[str, Any]:
        try:
            payload = await request.json()
            message_id = payload.get("message", {}).get("data")
            
            if not message_id:
                raise BadRequestException("Missing Gmail message ID")
            
            log.info(f"Received Gmail webhook for message: {message_id}")
            
            return payload
            
        except Exception as e:
            log.error(f"Failed to receive Gmail webhook: {e}")
            raise


webhook_receiver = WebhookReceiver()
