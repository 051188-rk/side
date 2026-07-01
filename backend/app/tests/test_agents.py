import pytest
from unittest.mock import Mock, AsyncMock, patch
from app.agents.feedback_cleaner_agent import FeedbackCleanerAgent
from app.agents.classification_agent import ClassificationAgent
from app.agents.severity_agent import SeverityAgent


@pytest.mark.asyncio
async def test_feedback_cleaner_agent():
    with patch('app.repositories.agent_run_repository.AgentRunRepository') as mock_repo:
        mock_repo.return_value.create_agent_run = AsyncMock(return_value="run_id")
        mock_repo.return_value.complete_run = AsyncMock()
        
        agent = FeedbackCleanerAgent()
        result = await agent.execute({
            "content": "<script>alert('xss')</script>Hello World"
        })
        
        assert result["success"] == True
        assert result["result"]["cleaned_content"] is not None
        assert "<script>" not in result["result"]["cleaned_content"]


@pytest.mark.asyncio
async def test_feedback_cleaner_agent_spam_detection():
    with patch('app.repositories.agent_run_repository.AgentRunRepository') as mock_repo:
        mock_repo.return_value.create_agent_run = AsyncMock(return_value="run_id")
        mock_repo.return_value.complete_run = AsyncMock()
        
        agent = FeedbackCleanerAgent()
        result = await agent.execute({
            "content": "buy now free money winner"
        })
        
        assert result["success"] == True
        assert result["result"]["is_spam"] == True


@pytest.mark.asyncio
async def test_classification_agent():
    with patch('app.repositories.agent_run_repository.AgentRunRepository') as mock_repo:
        with patch('app.integrations.llm_provider.llm_provider') as mock_llm:
            mock_repo.return_value.create_agent_run = AsyncMock(return_value="run_id")
            mock_repo.return_value.complete_run = AsyncMock()
            
            mock_llm.generate_structured = AsyncMock(return_value={
                "category": "Bug",
                "confidence": 0.9,
                "reasoning": "Clear bug report"
            })
            
            agent = ClassificationAgent()
            result = await agent.execute({
                "content": "The app crashes when I click submit"
            })
            
            assert result["success"] == True
            assert result["result"]["category"] == "Bug"


@pytest.mark.asyncio
async def test_severity_agent():
    with patch('app.repositories.agent_run_repository.AgentRunRepository') as mock_repo:
        with patch('app.integrations.llm_provider.llm_provider') as mock_llm:
            mock_repo.return_value.create_agent_run = AsyncMock(return_value="run_id")
            mock_repo.return_value.complete_run = AsyncMock()
            
            mock_llm.generate_structured = AsyncMock(return_value={
                "severity": "High",
                "confidence": 0.85,
                "reasoning": "Critical functionality affected",
                "impact_factors": ["user impact", "business impact"]
            })
            
            agent = SeverityAgent()
            result = await agent.execute({
                "content": "Payment processing is broken",
                "category": "Bug"
            })
            
            assert result["success"] == True
            assert result["result"]["severity"] == "High"


@pytest.mark.asyncio
async def test_agent_error_handling():
    with patch('app.repositories.agent_run_repository.AgentRunRepository') as mock_repo:
        mock_repo.return_value.create_agent_run = AsyncMock(return_value="run_id")
        mock_repo.return_value.fail_run = AsyncMock()
        
        agent = FeedbackCleanerAgent()
        result = await agent.execute({
            "content": None  # This should cause an error
        })
        
        assert result["success"] == False
        assert result["error"] is not None
