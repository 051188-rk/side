from typing import Optional, Dict, Any, List
from app.integrations.groq_integration import groq_integration
from app.integrations.gemini_integration import gemini_integration
from app.core.logging import log
from app.core.exceptions import LLMException


class LLMProvider:
    def __init__(self):
        self._primary_provider = "groq"
        self._fallback_provider = "gemini"

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        try:
            log.info(f"Generating with primary provider: {self._primary_provider}")
            return await self._generate_with_provider(
                self._primary_provider,
                prompt,
                system_prompt,
                temperature,
                max_tokens
            )
        except Exception as e:
            log.warning(f"Primary provider {self._primary_provider} failed, trying fallback: {e}")
            try:
                return await self._generate_with_provider(
                    self._fallback_provider,
                    prompt,
                    system_prompt,
                    temperature,
                    max_tokens
                )
            except Exception as fallback_error:
                log.error(f"Fallback provider {self._fallback_provider} also failed: {fallback_error}")
                raise LLMException("LLMProvider", f"All providers failed: {str(e)}, {str(fallback_error)}")

    async def _generate_with_provider(
        self,
        provider: str,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        if provider == "groq":
            return await groq_integration.generate(prompt, system_prompt, temperature, max_tokens)
        elif provider == "gemini":
            return await gemini_integration.generate(prompt, system_prompt, temperature, max_tokens)
        else:
            raise ValueError(f"Unknown provider: {provider}")

    async def generate_with_history(
        self,
        prompt: str,
        conversation_history: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        try:
            log.info(f"Generating with history using primary provider: {self._primary_provider}")
            return await self._generate_with_history_provider(
                self._primary_provider,
                prompt,
                conversation_history,
                system_prompt,
                temperature,
                max_tokens
            )
        except Exception as e:
            log.warning(f"Primary provider {self._primary_provider} failed, trying fallback: {e}")
            try:
                return await self._generate_with_history_provider(
                    self._fallback_provider,
                    prompt,
                    conversation_history,
                    system_prompt,
                    temperature,
                    max_tokens
                )
            except Exception as fallback_error:
                log.error(f"Fallback provider {self._fallback_provider} also failed: {fallback_error}")
                raise LLMException("LLMProvider", f"All providers failed: {str(e)}, {str(fallback_error)}")

    async def _generate_with_history_provider(
        self,
        provider: str,
        prompt: str,
        conversation_history: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        if provider == "groq":
            return await groq_integration.generate_with_history(
                prompt, conversation_history, system_prompt, temperature, max_tokens
            )
        elif provider == "gemini":
            return await gemini_integration.generate_with_history(
                prompt, conversation_history, system_prompt, temperature, max_tokens
            )
        else:
            raise ValueError(f"Unknown provider: {provider}")

    async def generate_structured(
        self,
        prompt: str,
        schema: Dict[str, Any],
        system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        try:
            log.info(f"Generating structured output with primary provider: {self._primary_provider}")
            return await self._generate_structured_provider(
                self._primary_provider,
                prompt,
                schema,
                system_prompt
            )
        except Exception as e:
            log.warning(f"Primary provider {self._primary_provider} failed, trying fallback: {e}")
            try:
                return await self._generate_structured_provider(
                    self._fallback_provider,
                    prompt,
                    schema,
                    system_prompt
                )
            except Exception as fallback_error:
                log.error(f"Fallback provider {self._fallback_provider} also failed: {fallback_error}")
                raise LLMException("LLMProvider", f"All providers failed: {str(e)}, {str(fallback_error)}")

    async def _generate_structured_provider(
        self,
        provider: str,
        prompt: str,
        schema: Dict[str, Any],
        system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        if provider == "groq":
            return await groq_integration.generate_structured(prompt, schema, system_prompt)
        elif provider == "gemini":
            return await gemini_integration.generate_structured(prompt, schema, system_prompt)
        else:
            raise ValueError(f"Unknown provider: {provider}")


llm_provider = LLMProvider()
