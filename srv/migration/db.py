from sqlalchemy import create_engine
from core.config import env

Engine = create_engine(
    env().get_sync_db_url(),
    echo=True
)