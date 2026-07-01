import pytest
from unittest.mock import Mock, AsyncMock, patch
from app.integrations.llm_provider import LLMProvider


@pytest.mark.asyncio
async def test_llm_provider_generate():
    with patch('app.integrations.groq_integration.groq_integration') as mock_groq:
        mock_groq._ensure_initialized = AsyncMock()
        mock_groq._client = Mock()
        mock_groq._client.invoke = Mock(return_value=Mock(content="Test response"))
        
        provider = LLMProvider()
        result = await provider.generate("Test prompt")
        
        assert result == "Test response"


@pytest.mark.asyncio
async def test_llm_provider_fallback():
    with patch('app.integrations.groq_integration.groq_integration') as mock_groq:
        with patch('app.integrations.gemini_integration.gemini_integration') as mock_gemini:
            mock_groq._ensure_initialized = AsyncMock()
            mock_groq._client.invoke = Mock(side_effect=Exception("Groq failed"))
            
            mock_gemini._ensure_initialized = AsyncMock()
            mock_gemini._client = Mock()
            mock_gemini._client.invoke = Mock(return_value=Mock(content="Gemini response"))
            
            provider = LLMProvider()
            result = await provider.generate("Test prompt")
            
            assert result == "Gemini response"


@pytest.mark.asyncio
async def test_llm_provider_both_fail():
    with patch('app.integrations.groq_integration.groq_integration') as mock_groq:
        with patch('app.integrations.gemini_integration.gemini_integration') as mock_gemini:
            mock_groq._ensure_initialized = AsyncMock()
            mock_groq._client.invoke = Mock(side_effect=Exception("Groq failed"))
            
            mock_gemini._ensure_initialized = AsyncMock()
            mock_gemini._client.invoke = Mock(side_effect=Exception("Gemini failed"))
            
            provider = LLMProvider()
            
            with pytest.raises(Exception):
                await provider.generate("Test prompt")


@pytest.mark.asyncio
async def test_llm_provider_structured_generation():
    with patch('app.integrations.groq_integration.groq_integration') as mock_groq:
        mock_groq._ensure_initialized = AsyncMock()
        mock_groq._client = Mock()
        mock_groq._client.with_structured_output = Mock(return_value=Mock(
            invoke=Mock(return_value={"category": "Bug", "confidence": 0.9})
        ))
        
        provider = LLMProvider()
        schema = {"type": "object", "properties": {"category": {"type": "string"}}}
        result = await provider.generate_structured("Test prompt", schema)
        
        assert result["category"] == "Bug"
