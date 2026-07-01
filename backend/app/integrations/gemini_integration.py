from typing import Optional, Dict, Any, List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from app.config import settings
from app.core.logging import log
from app.core.exceptions import LLMException


class GeminiIntegration:
    def __init__(self):
        self._client: Optional[ChatGoogleGenerativeAI] = None
        self._backup_client: Optional[ChatGoogleGenerativeAI] = None
        self._initialized = False

    async def _ensure_initialized(self):
        if not self._initialized:
            try:
                self._client = ChatGoogleGenerativeAI(
                    api_key=settings.gemini_api_key,
                    model=settings.gemini_model,
                    temperature=0.7,
                    max_output_tokens=4096,
                )
                
                self._backup_client = ChatGoogleGenerativeAI(
                    api_key=settings.gemini_api_key,
                    model=settings.gemini_backup_model,
                    temperature=0.7,
                    max_output_tokens=4096,
                )
                
                self._initialized = True
                log.info("Gemini integration initialized")
            except Exception as e:
                log.error(f"Failed to initialize Gemini: {e}")
                raise LLMException("Gemini", str(e))

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
                max_output_tokens=max_tokens or 4096,
            )
            
            result = response.content
            log.info(f"Gemini generation completed")
            return result
            
        except Exception as e:
            log.error(f"Gemini generation failed: {e}")
            if not use_backup and settings.agent_fallback_enabled:
                log.info("Falling back to backup Gemini model")
                return await self.generate(
                    prompt, system_prompt, temperature, max_tokens, use_backup=True
                )
            raise LLMException("Gemini", f"Generation failed: {str(e)}")

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
                max_output_tokens=max_tokens or 4096,
            )
            
            result = response.content
            log.info(f"Gemini generation with history completed")
            return result
            
        except Exception as e:
            log.error(f"Gemini generation with history failed: {e}")
            raise LLMException("Gemini", f"Generation with history failed: {str(e)}")

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
            
            log.info(f"Gemini structured generation completed")
            return response
            
        except Exception as e:
            log.error(f"Gemini structured generation failed: {e}")
            raise LLMException("Gemini", f"Structured generation failed: {str(e)}")

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
            log.error(f"Gemini stream generation failed: {e}")
            raise LLMException("Gemini", f"Stream generation failed: {str(e)}")


gemini_integration = GeminiIntegration()
