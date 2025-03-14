from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # GitHub OAuth
    github_client_id: str = os.getenv("GITHUB_CLIENT_ID", "")
    github_client_secret: str = os.getenv("GITHUB_CLIENT_SECRET", "")
    github_redirect_uri: str = os.getenv("GITHUB_REDIRECT_URI", "http://localhost:8000/api/auth/callback")
    
    # Database
    database_url: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/gitmax")
    
    # JWT
    secret_key: str = os.getenv("SECRET_KEY", "")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # API
    api_prefix: str = "/api"
    
    # Frontend
    frontend_url: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    
    # CORS
    cors_origins: list = [
        "http://localhost:3000",  # React frontend
        "http://localhost:8000",  # FastAPI backend
    ]

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Get the application settings.
    
    Returns:
        Settings: The application settings.
    """
    return Settings()
