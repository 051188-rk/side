from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, AnyHttpUrl
import os


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # Application
    app_name: str = "SIDE"
    app_version: str = "1.0.0"
    app_env: str = "development"
    debug: bool = True
    secret_key: str = Field(default="your-secret-key-change-this-in-production")
    api_v1_prefix: str = "/api/v1"

    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 4

    # Firebase
    firebase_project_id: str = Field(default="")
    firebase_private_key_id: str = Field(default="")
    firebase_private_key: str = Field(default="")
    firebase_client_email: str = Field(default="")
    firebase_client_id: str = Field(default="")
    firebase_auth_uri: str = "https://accounts.google.com/o/oauth2/auth"
    firebase_token_uri: str = "https://oauth2.googleapis.com/token"
    firebase_auth_provider_x509_cert_url: str = "https://www.googleapis.com/oauth2/v1/certs"
    firebase_client_x509_cert_url: str = Field(default="")
    firebase_database_url: str = Field(default="")
    firebase_storage_bucket: str = Field(default="")

    # Firebase Authentication
    firebase_api_key: str = Field(default="")
    firebase_auth_domain: str = Field(default="")
    firebase_messaging_sender_id: str = Field(default="")
    firebase_app_id: str = Field(default="")

    # JWT
    jwt_secret_key: str = Field(default="your-jwt-secret-key")
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7

    # Groq API
    groq_api_key: str = Field(default="")
    groq_model: str = "llama-3.3-70b-versatile"
    groq_backup_model: str = "llama-3.1-70b-versatile"

    # Google Gemini API
    gemini_api_key: str = Field(default="")
    gemini_model: str = "gemini-2.0-flash-exp"
    gemini_backup_model: str = "gemini-1.5-pro"

    # Cognee
    cognee_api_key: str = Field(default="")
    cognee_endpoint: str = "https://api.cognee.ai"
    cognee_vector_db: str = "weaviate"
    cognee_knowledge_graph: str = "neo4j"

    # TinyFish
    tinyfish_api_key: str = Field(default="")
    tinyfish_search_endpoint: str = "https://api.tinyfish.com/search"
    tinyfish_fetch_endpoint: str = "https://api.tinyfish.com/fetch"

    # Discord Bot
    discord_bot_token: str = Field(default="")
    discord_client_id: str = Field(default="")
    discord_client_secret: str = Field(default="")
    discord_guild_id: str = Field(default="")

    # Telegram Bot
    telegram_bot_token: str = Field(default="")
    telegram_webhook_secret: str = Field(default="")

    # GitHub
    github_access_token: str = Field(default="")
    github_webhook_secret: str = Field(default="")
    github_client_id: str = Field(default="")
    github_client_secret: str = Field(default="")

    # Gmail
    gmail_credentials_file: str = Field(default="")
    gmail_token_file: str = Field(default="")
    gmail_scopes: str = "https://www.googleapis.com/auth/gmail.readonly,https://www.googleapis.com/auth/gmail.send"

    # SMTP Email
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_username: str = Field(default="")
    smtp_password: str = Field(default="")
    smtp_from_email: str = "noreply@side.ai"
    smtp_from_name: str = "SIDE Platform"
    smtp_use_tls: bool = True

    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: str = Field(default="")

    # Rate Limiting
    rate_limit_enabled: bool = True
    rate_limit_per_minute: int = 60
    rate_limit_per_hour: int = 1000

    # CORS
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["*"]
    cors_allow_headers: List[str] = ["*"]

    # Logging
    log_level: str = "INFO"
    log_format: str = "json"
    log_file: str = "logs/app.log"

    # Background Tasks
    task_queue_size: int = 1000
    task_worker_count: int = 4

    # Agent Configuration
    agent_max_retries: int = 3
    agent_timeout: int = 300
    agent_fallback_enabled: bool = True

    # Memory Configuration
    memory_retention_days: int = 365
    memory_max_context_tokens: int = 8000

    # Webhook Configuration
    webhook_timeout: int = 30
    webhook_max_retries: int = 3
    webhook_verify_signatures: bool = True

    # Analytics
    analytics_enabled: bool = True
    analytics_retention_days: int = 90

    # Dashboard
    dashboard_refresh_interval: int = 300

    @property
    def firebase_credentials_dict(self) -> dict:
        return {
            "type": "service_account",
            "project_id": self.firebase_project_id,
            "private_key_id": self.firebase_private_key_id,
            "private_key": self.firebase_private_key.replace("\\n", "\n"),
            "client_email": self.firebase_client_email,
            "client_id": self.firebase_client_id,
            "auth_uri": self.firebase_auth_uri,
            "token_uri": self.firebase_token_uri,
            "auth_provider_x509_cert_url": self.firebase_auth_provider_x509_cert_url,
            "client_x509_cert_url": self.firebase_client_x509_cert_url,
        }

    @property
    def gmail_scopes_list(self) -> List[str]:
        return self.gmail_scopes.split(",")


settings = Settings()
