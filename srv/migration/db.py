from sqlalchemy import create_engine
from core.config import get_env

Engine = create_engine(
    get_env().db_url,
    echo=True
)