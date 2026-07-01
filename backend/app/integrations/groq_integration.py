from typing import Optional, Dict, Any, List
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from app.config import settings
from app.core.logging import log
from app.core.exceptions import LLMException


class GroqIntegration:
    def __init__(self):
        self._client: Optional[ChatGroq] = None
        self._backup_client: Optional[ChatGroq] = None
        self._initialized = False

    async def _ensure_initialized(self):
        if not self._initialized:
            try:
                self._client = ChatGroq(
                    api_key=settings.groq_api_key,
                    model=settings.groq_model,
                    temperature=0.7,
                    max_tokens=4096,
                )
                
                self._backup_client = ChatGroq(
                    api_key=settings.groq_api_key,
                    model=settings.groq_backup_model,
                    temperature=0.7,
                    max_tokens=4096,
                )
                
                self._initialized = True
                log.info("Groq integration initialized")
            except Exception as e:
                log.error(f"Failed to initialize Groq: {e}")
                raise LLMException("Groq", str(e))

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        use_backup: bool = False
    ) -> str:
        await self._ensure_initialized()
        
        client = self._backup_client if use_backup else self._client
        
        try:
            messages = []
            if system_prompt:
                messages.append(SystemMessage(content=system_prompt))
            messages.append(HumanMessage(content=prompt))
            
            response = client.invoke(
                messages,
                temperature=temperature or 0.7,
                max_tokens=max_tokens or 4096,
            )
            
            result = response.content
            log.info(f"Groq generation completed, tokens used: {response.usage_metadata.get('total_tokens', 0)}")
            return result
            
        except Exception as e:
            log.error(f"Groq generation failed: {e}")
            if not use_backup and settings.agent_fallback_enabled:
                log.info("Falling back to backup Groq model")
                return await self.generate(
                    prompt, system_prompt, temperature, max_tokens, use_backup=True
                )
            raise LLMException("Groq", f"Generation failed: {str(e)}")

    async def generate_with_history(
        self,
        prompt: str,
        conversation_history: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        await self._ensure_initialized()
        
        try:
            messages = []
            if system_prompt:
                messages.append(SystemMessage(content=system_prompt))
            
            for msg in conversation_history:
                if msg["role"] == "user":
                    messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    messages.append(AIMessage(content=msg["content"]))
            
            messages.append(HumanMessage(content=prompt))
            
            response = self._client.invoke(
                messages,
                temperature=temperature or 0.7,
                max_tokens=max_tokens or 4096,
            )
            
            result = response.content
            log.info(f"Groq generation with history completed")
            return result
            
        except Exception as e:
            log.error(f"Groq generation with history failed: {e}")
            raise LLMException("Groq", f"Generation with history failed: {str(e)}")

    async def generate_structured(
        self,
        prompt: str,
        schema: Dict[str, Any],
        system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        await self._ensure_initialized()
        
        try:
            messages = []
            if system_prompt:
                messages.append(SystemMessage(content=system_prompt))
            messages.append(HumanMessage(content=prompt))
            
            response = self._client.with_structured_output(schema).invoke(messages)
            
            log.info(f"Groq structured generation completed")
            return response
            
        except Exception as e:
            log.error(f"Groq structured generation failed: {e}")
            raise LLMException("Groq", f"Structured generation failed: {str(e)}")

    async def generate_stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None
    ):
        await self._ensure_initialized()
        
        try:
            messages = []
            if system_prompt:
                messages.append(SystemMessage(content=system_prompt))
            messages.append(HumanMessage(content=prompt))
            
            async for chunk in self._client.astream(messages):
                yield chunk.content
                
        except Exception as e:
            log.error(f"Groq stream generation failed: {e}")
            raise LLMException("Groq", f"Stream generation failed: {str(e)}")


groq_integration = GroqIntegration()
