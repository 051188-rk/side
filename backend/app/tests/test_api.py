import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, AsyncMock, patch
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_auth():
    with patch('app.core.security.verify_firebase_token') as mock:
        mock.return_value = {"uid": "test_uid", "email": "test@example.com"}
        yield mock


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data


def test_readiness_check(client):
    response = client.get("/health/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"


def test_liveness_check(client):
    response = client.get("/health/live")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "alive"


@pytest.mark.asyncio
async def test_login_endpoint(client, mock_auth):
    with patch('app.repositories.user_repository.UserRepository') as mock_repo:
        with patch('app.core.security.create_access_token') as mock_token:
            with patch('app.core.security.create_refresh_token') as mock_refresh:
                mock_repo.return_value.get_by_firebase_uid = AsyncMock(return_value={
                    "id": "user_id",
                    "email": "test@example.com",
                    "role": "user"
                })
                mock_token.return_value = "access_token"
                mock_refresh.return_value = "refresh_token"
                
                response = client.post("/api/v1/auth/login", json={
                    "firebase_token": "test_token"
                })
                
                assert response.status_code == 200
                data = response.json()
                assert data["success"] == True
                assert "access_token" in data["data"]


@pytest.mark.asyncio
async def test_signup_endpoint(client):
    with patch('app.integrations.firebase_integration.firebase_integration') as mock_firebase:
        with patch('app.repositories.user_repository.UserRepository') as mock_user_repo:
            with patch('app.repositories.organization_repository.OrganizationRepository') as mock_org_repo:
                with patch('app.core.security.create_access_token') as mock_token:
                    with patch('app.core.security.create_refresh_token') as mock_refresh:
                        mock_firebase.create_user = AsyncMock(return_value={
                            "uid": "firebase_uid",
                            "email": "test@example.com"
                        })
                        mock_org_repo.return_value.create_organization = AsyncMock(return_value="org_id")
                        mock_user_repo.return_value.create_user = AsyncMock(return_value="user_id")
                        mock_user_repo.return_value.get_by_id = AsyncMock(return_value={
                            "id": "user_id",
                            "email": "test@example.com",
                            "role": "user"
                        })
                        mock_token.return_value = "access_token"
                        mock_refresh.return_value = "refresh_token"
                        
                        response = client.post("/api/v1/auth/signup", json={
                            "email": "test@example.com",
                            "password": "password123",
                            "display_name": "Test User"
                        })
                        
                        assert response.status_code == 200
                        data = response.json()
                        assert data["success"] == True


def test_cors_headers(client):
    response = client.options("/", headers={
        "Origin": "http://localhost:3000",
        "Access-Control-Request-Method": "POST"
    })
    assert response.status_code == 200
