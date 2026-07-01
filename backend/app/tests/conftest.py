import pytest
import asyncio
from typing import Generator


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def mock_firebase_client(monkeypatch):
    from unittest.mock import Mock, AsyncMock
    
    mock_client = Mock()
    mock_db = Mock()
    
    mock_doc_ref = Mock()
    mock_doc_ref.id = "test_id"
    mock_doc_ref.set = AsyncMock()
    mock_doc_ref.get = AsyncMock()
    mock_doc_ref.update = AsyncMock()
    mock_doc_ref.delete = AsyncMock()
    
    mock_query = Mock()
    mock_query.where = Mock(return_value=mock_query)
    mock_query.order_by = Mock(return_value=mock_query)
    mock_query.limit = Mock(return_value=mock_query)
    mock_query.offset = Mock(return_value=mock_query)
    
    mock_doc = Mock()
    mock_doc.exists = True
    mock_doc.to_dict = Mock(return_value={"id": "test_id"})
    
    mock_query.get = AsyncMock(return_value=[mock_doc])
    
    mock_db.collection.return_value.document.return_value = mock_doc_ref
    mock_db.collection.return_value.where.return_value = mock_query
    
    mock_client.db = mock_db
    
    monkeypatch.setattr("app.repositories.firebase_client.firebase_client", mock_client)
    yield mock_client
