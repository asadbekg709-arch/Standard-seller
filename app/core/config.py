from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    redis_url: str = "redis://localhost:6379"
    user_service_url: str = "http://user-service:8000"
    order_service_url: str = "http://order-service:8001"
    crm_service_url: str = "http://crm-service:8002"
    timeout: int = 10

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()
