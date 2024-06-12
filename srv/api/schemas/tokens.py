from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from api.schemas.common import IdBase, CreatedUpdatedAtBase, AccessTokenBase

def default_timezone():
    return ZoneInfo("Asia/Tokyo")

def default_expire_at():
    return datetime.now(default_timezone()) + timedelta(days=3)

class TokensBase(AccessTokenBase):
    user_id: int = Field(desciption="ユーザーID")
    expire_at: datetime = Field(default_expire_at(), desciption="有効期限")

class Tokens(BaseModel, IdBase, CreatedUpdatedAtBase, TokensBase):
    pass

class TokenCreate(BaseModel, TokensBase):
    pass

class TokenCreateResponse(BaseModel, IdBase):
    pass
