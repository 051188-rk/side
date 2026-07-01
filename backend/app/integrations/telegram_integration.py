from typing import Optional, Dict, Any, List
from telegram import Bot, Update
from telegram.ext import Application
from app.config import settings
from app.core.logging import log
from app.core.exceptions import ExternalServiceException


class TelegramIntegration:
    def __init__(self):
        self._bot: Optional[Bot] = None
        self._application: Optional[Application] = None
        self._initialized = False

    async def _ensure_initialized(self):
        if not self._initialized:
            try:
                self._bot = Bot(token=settings.telegram_bot_token)
                self._application = Application.builder().token(settings.telegram_bot_token).build()
                self._initialized = True
                log.info("Telegram integration initialized")
            except Exception as e:
                log.error(f"Failed to initialize Telegram: {e}")
                raise ExternalServiceException("Telegram", str(e))

    async def send_message(self, chat_id: str, text: str, parse_mode: Optional[str] = None) -> bool:
        await self._ensure_initialized()
        try:
            await self._bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode=parse_mode,
            )
            log.info(f"Sent Telegram message to chat {chat_id}")
            return True
        except Exception as e:
            log.error(f"Failed to send Telegram message: {e}")
            raise ExternalServiceException("Telegram", f"Failed to send message: {str(e)}")

    async def send_photo(self, chat_id: str, photo: str, caption: Optional[str] = None) -> bool:
        await self._ensure_initialized()
        try:
            await self._bot.send_photo(
                chat_id=chat_id,
                photo=photo,
                caption=caption,
            )
            log.info(f"Sent Telegram photo to chat {chat_id}")
            return True
        except Exception as e:
            log.error(f"Failed to send Telegram photo: {e}")
            raise ExternalServiceException("Telegram", f"Failed to send photo: {str(e)}")

    async def get_chat_history(self, chat_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        await self._ensure_initialized()
        try:
            async with self._application:
                messages = []
                async for message in self._bot.get_chat_history(chat_id=chat_id, limit=limit):
                    messages.append({
                        "message_id": message.message_id,
                        "text": message.text,
                        "from_user": message.from_user.to_dict() if message.from_user else None,
                        "date": message.date.isoformat() if message.date else None,
                    })
                
                log.info(f"Retrieved {len(messages)} messages from Telegram chat {chat_id}")
                return messages
        except Exception as e:
            log.error(f"Failed to get Telegram chat history: {e}")
            raise ExternalServiceException("Telegram", f"Failed to get chat history: {str(e)}")

    async def get_chat_info(self, chat_id: str) -> Dict[str, Any]:
        await self._ensure_initialized()
        try:
            chat = await self._bot.get_chat(chat_id=chat_id)
            return {
                "id": str(chat.id),
                "type": chat.type,
                "title": chat.title,
                "username": chat.username,
                "description": chat.description,
            }
        except Exception as e:
            log.error(f"Failed to get Telegram chat info: {e}")
            raise ExternalServiceException("Telegram", f"Failed to get chat info: {str(e)}")

    async def set_webhook(self, webhook_url: str, secret_token: Optional[str] = None) -> bool:
        await self._ensure_initialized()
        try:
            await self._bot.set_webhook(
                url=webhook_url,
                secret_token=secret_token or settings.telegram_webhook_secret,
            )
            log.info(f"Set Telegram webhook to {webhook_url}")
            return True
        except Exception as e:
            log.error(f"Failed to set Telegram webhook: {e}")
            raise ExternalServiceException("Telegram", f"Failed to set webhook: {str(e)}")

    async def delete_webhook(self) -> bool:
        await self._ensure_initialized()
        try:
            await self._bot.delete_webhook()
            log.info("Deleted Telegram webhook")
            return True
        except Exception as e:
            log.error(f"Failed to delete Telegram webhook: {e}")
            raise ExternalServiceException("Telegram", f"Failed to delete webhook: {str(e)}")

    async def verify_webhook(self, secret_token: str) -> bool:
        return secret_token == settings.telegram_webhook_secret

    async def close(self):
        if self._application and self._initialized:
            await self._application.shutdown()
            self._initialized = False
            log.info("Telegram integration closed")


telegram_integration = TelegramIntegration()
