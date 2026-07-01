from typing import Optional, Dict, Any, List
import discord
from discord.ext import commands
from app.config import settings
from app.core.logging import log
from app.core.exceptions import ExternalServiceException


class DiscordIntegration:
    def __init__(self):
        self._client: Optional[discord.Client] = None
        self._initialized = False

    async def _ensure_initialized(self):
        if not self._initialized:
            try:
                intents = discord.Intents.default()
                intents.message_content = True
                intents.guilds = True
                intents.members = True
                
                self._client = discord.Client(intents=intents)
                await self._client.login(settings.discord_bot_token)
                self._initialized = True
                log.info("Discord integration initialized")
            except Exception as e:
                log.error(f"Failed to initialize Discord: {e}")
                raise ExternalServiceException("Discord", str(e))

    async def send_message(self, channel_id: str, content: str, embed: Optional[Dict[str, Any]] = None) -> bool:
        await self._ensure_initialized()
        try:
            channel = self._client.get_channel(int(channel_id))
            if not channel:
                raise ValueError(f"Channel {channel_id} not found")
            
            if embed:
                discord_embed = discord.Embed.from_dict(embed)
                await channel.send(content=content, embed=discord_embed)
            else:
                await channel.send(content)
            
            log.info(f"Sent Discord message to channel {channel_id}")
            return True
        except Exception as e:
            log.error(f"Failed to send Discord message: {e}")
            raise ExternalServiceException("Discord", f"Failed to send message: {str(e)}")

    async def get_channel_messages(self, channel_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        await self._ensure_initialized()
        try:
            channel = self._client.get_channel(int(channel_id))
            if not channel:
                raise ValueError(f"Channel {channel_id} not found")
            
            messages = []
            async for message in channel.history(limit=limit):
                messages.append({
                    "id": str(message.id),
                    "author": str(message.author),
                    "content": message.content,
                    "timestamp": message.created_at.isoformat(),
                    "channel_id": str(message.channel.id),
                })
            
            log.info(f"Retrieved {len(messages)} messages from Discord channel {channel_id}")
            return messages
        except Exception as e:
            log.error(f"Failed to get Discord messages: {e}")
            raise ExternalServiceException("Discord", f"Failed to get messages: {str(e)}")

    async def create_guild_channel(self, guild_id: str, name: str, channel_type: str = "text") -> str:
        await self._ensure_initialized()
        try:
            guild = self._client.get_guild(int(guild_id))
            if not guild:
                raise ValueError(f"Guild {guild_id} not found")
            
            if channel_type == "text":
                channel = await guild.create_text_channel(name)
            elif channel_type == "voice":
                channel = await guild.create_voice_channel(name)
            else:
                raise ValueError(f"Unsupported channel type: {channel_type}")
            
            log.info(f"Created Discord channel {name} in guild {guild_id}")
            return str(channel.id)
        except Exception as e:
            log.error(f"Failed to create Discord channel: {e}")
            raise ExternalServiceException("Discord", f"Failed to create channel: {str(e)}")

    async def get_guild_info(self, guild_id: str) -> Dict[str, Any]:
        await self._ensure_initialized()
        try:
            guild = self._client.get_guild(int(guild_id))
            if not guild:
                raise ValueError(f"Guild {guild_id} not found")
            
            return {
                "id": str(guild.id),
                "name": guild.name,
                "member_count": guild.member_count,
                "owner_id": str(guild.owner_id),
            }
        except Exception as e:
            log.error(f"Failed to get Discord guild info: {e}")
            raise ExternalServiceException("Discord", f"Failed to get guild info: {str(e)}")

    async def verify_webhook(self, signature: str, body: bytes) -> bool:
        try:
            from nacl.signing import VerifyKey
            verify_key = VerifyKey(bytes.fromhex(settings.discord_client_id))
            verify_key.verify(body, bytes.fromhex(signature))
            return True
        except Exception as e:
            log.error(f"Failed to verify Discord webhook: {e}")
            return False

    async def close(self):
        if self._client and self._initialized:
            await self._client.close()
            self._initialized = False
            log.info("Discord integration closed")


discord_integration = DiscordIntegration()
