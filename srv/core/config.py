import os
from functools import lru_cache
from pydantic_settings import BaseSettings

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Environment(BaseSettings):
    db_url: str

    class Config:
        env_file = os.path.join(PROJECT_ROOT, '.env')

@lru_cache
def get_env():
    return Environment()