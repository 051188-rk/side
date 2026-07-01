import pytest
from unittest.mock import Mock, AsyncMock, patch
from app.repositories.user_repository import UserRepository
from app.repositories.feedback_repository import FeedbackRepository
from app.repositories.ticket_repository import TicketRepository


@pytest.mark.asyncio
async def test_user_repository_create():
    with patch('app.repositories.firebase_client.firebase_client') as mock_client:
        mock_db = Mock()
        mock_client.db = mock_db
        
        mock_doc_ref = Mock()
        mock_doc_ref.id = "test_user_id"
        mock_doc_ref.set = AsyncMock()
        mock_db.collection.return_value.document.return_value = mock_doc_ref
        
        repo = UserRepository()
        user_id = await repo.create_user(
            email="test@example.com",
            display_name="Test User"
        )
        
        assert user_id == "test_user_id"
        mock_doc_ref.set.assert_called_once()


@pytest.mark.asyncio
async def test_feedback_repository_create():
    with patch('app.repositories.firebase_client.firebase_client') as mock_client:
        mock_db = Mock()
        mock_client.db = mock_db
        
        mock_doc_ref = Mock()
        mock_doc_ref.id = "test_feedback_id"
        mock_doc_ref.set = AsyncMock()
        mock_db.collection.return_value.document.return_value = mock_doc_ref
        
        repo = FeedbackRepository()
        feedback_id = await repo.create_feedback(
            source="test",
            content="Test feedback"
        )
        
        assert feedback_id == "test_feedback_id"
        mock_doc_ref.set.assert_called_once()


@pytest.mark.asyncio
async def test_ticket_repository_create():
    with patch('app.repositories.firebase_client.firebase_client') as mock_client:
        mock_db = Mock()
        mock_client.db = mock_db
        
        mock_doc_ref = Mock()
        mock_doc_ref.id = "test_ticket_id"
        mock_doc_ref.set = AsyncMock()
        mock_db.collection.return_value.document.return_value = mock_doc_ref
        
        repo = TicketRepository()
        ticket_id = await repo.create_ticket(
            title="Test Ticket",
            description="Test description",
            category="Bug",
            severity="High",
            priority_score=0.8
        )
        
        assert ticket_id == "test_ticket_id"
        mock_doc_ref.set.assert_called_once()


@pytest.mark.asyncio
async def test_user_repository_get_by_email():
    with patch('app.repositories.firebase_client.firebase_client') as mock_client:
        mock_db = Mock()
        mock_client.db = mock_db
        
        mock_query = Mock()
        mock_query.where = Mock(return_value=mock_query)
        mock_query.limit = Mock(return_value=mock_query)
        
        mock_doc = Mock()
        mock_doc.exists = True
        mock_doc.to_dict = Mock(return_value={
            "id": "test_id",
            "email": "test@example.com",
            "display_name": "Test User"
        })
        
        mock_query.get = AsyncMock(return_value=[mock_doc])
        mock_db.collection.return_value.where.return_value = mock_query
        
        repo = UserRepository()
        user = await repo.get_by_email("test@example.com")
        
        assert user is not None
        assert user["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_ticket_repository_update_status():
    with patch('app.repositories.firebase_client.firebase_client') as mock_client:
        mock_db = Mock()
        mock_client.db = mock_db
        
        mock_doc_ref = Mock()
        mock_doc_ref.update = AsyncMock()
        mock_db.collection.return_value.document.return_value = mock_doc_ref
        
        repo = TicketRepository()
        result = await repo.update_status("test_id", "resolved")
        
        assert result == True
        mock_doc_ref.update.assert_called_once()
