from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    This class uses Pydantic to validate and load configuration.
    Values are read from .env file or environment variables.
    """
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/network_monitor"
    
    # JWT Authentication
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # WebSocket
    WS_MESSAGE_QUEUE_SIZE: int = 100
    
    # Monitoring
    ALERT_CHECK_INTERVAL: int = 60  # seconds
    
    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:3000"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Using lru_cache ensures we only create one Settings instance
    and reuse it throughout the application.
    """
    return Settings()
