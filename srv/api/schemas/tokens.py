from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

def default_timezone():
    return ZoneInfo("Asia/Tokyo")

def default_expire_at():
    return datetime.now(default_timezone()) + timedelta(days=3)

class TokensBase(BaseModel):
    access_token: str = Field(desciption="アクセストークン")
    user_id: int = Field(desciption="ユーザーID")
    expire_at: datetime = Field(default_expire_at(), desciption="有効期限")

class Tokens(TokensBase):
    id: int
    created_at: datetime = Field(desciption="作成日時")
    updated_at: datetime | None = Field(desciption="更新日時")

    model_config = ConfigDict(from_attributes=True)

class TokenCreate(TokensBase):
    pass

class TokenCreateResponse(TokensBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
