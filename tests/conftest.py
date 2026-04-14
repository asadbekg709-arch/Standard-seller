import os

os.environ.setdefault("OPENAI_API_KEY", "test-key")
os.environ.setdefault("OPENAI_MODEL", "gpt-4o-mini")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379")
os.environ.setdefault("USER_SERVICE_URL", "http://localhost:8001")
os.environ.setdefault("ORDER_SERVICE_URL", "http://localhost:8002")
os.environ.setdefault("CRM_SERVICE_URL", "http://localhost:8003")
