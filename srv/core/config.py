import os
from functools import lru_cache
from pydantic_settings import BaseSettings
from zoneinfo import ZoneInfo

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Environment(BaseSettings):
    db_url: str
    frontend_url: str

    def get_sync_db_url(self):
        return f"postgresql+psycopg2://{self.db_url}"

    def get_async_db_url(self):
        return f"postgresql+asyncpg://{self.db_url}"

    class Config:
        env_file = os.path.join(PROJECT_ROOT, '.env')

@lru_cache
def env():
    return Environment()

def default_timezone():
    return ZoneInfo("Asia/Tokyo")