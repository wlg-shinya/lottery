import os
from functools import lru_cache
from pydantic import ConfigDict
from pydantic_settings import BaseSettings
from zoneinfo import ZoneInfo

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Environment(BaseSettings):
    app_title: str
    db_url: str
    db_test_url: str
    frontend_url: str
    notice_email: str
    openapi_url: str
    docs_url: str | None
    redoc_url: str | None
    smtp_password: str | None

    def get_sync_db_url(self, db_url: str):
        return f"postgresql+psycopg2://{db_url}"

    def get_async_db_url(self, db_url: str):
        return f"postgresql+asyncpg://{db_url}"

    model_config = ConfigDict(
        env_file = os.path.join(PROJECT_ROOT, '.env.local')
        )

@lru_cache
def env():
    return Environment()

def default_timezone():
    return ZoneInfo("Asia/Tokyo")