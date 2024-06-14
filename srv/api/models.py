from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import INTEGER, TIMESTAMP, VARCHAR, ARRAY
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql.functions import current_timestamp

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=current_timestamp(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=current_timestamp())

class Lotteries(BaseModel):
    __tablename__ = "lotteries"

    user_id = Column(INTEGER, nullable=False)
    text = Column(VARCHAR(256), nullable=False)
    title = Column(VARCHAR(32), nullable=False)
    description = Column(VARCHAR(256), nullable=False)
    used_count = Column(INTEGER)

class Users(BaseModel):
    __tablename__ = "users"

    email = Column(VARCHAR(80), nullable=False, unique=True)
    account_name = Column(VARCHAR(24), nullable=False)
    identification = Column(VARCHAR(64), nullable=False, unique=True)
    pull_lottery_ids = Column(ARRAY(INTEGER), nullable=False)

class AccessTokens(BaseModel):
    __tablename__ = "access_tokens"

    token = Column(VARCHAR(64), nullable=False, unique=True)
    user_id = Column(INTEGER, nullable=False)
    expire_at = Column(TIMESTAMP(timezone=True), nullable=False)

class SignupTokens(BaseModel):
    __tablename__ = "signup_tokens"

    token = Column(VARCHAR(64), nullable=False, unique=True)
    email = Column(VARCHAR(80), nullable=False)
    account_name = Column(VARCHAR(24), nullable=False)
    identification = Column(VARCHAR(64), nullable=False)
    expire_at = Column(TIMESTAMP(timezone=True), nullable=False)
