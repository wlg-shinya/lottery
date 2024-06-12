from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from api.schemas.common import IdBase, CreatedUpdatedAtBase, AccessTokenBase
from core.config import default_timezone

def default_expire_at():
    return datetime.now(default_timezone()) + timedelta(days=3)

class AccessTokensBase():
    token: str = Field(desciption="アクセストークン")
    user_id: int = Field(desciption="ユーザーID")
    expire_at: datetime = Field(default_expire_at(), desciption="有効期限")

class AccessTokens(BaseModel, IdBase, CreatedUpdatedAtBase, AccessTokensBase):
    pass

class AccessTokenCreate(BaseModel, AccessTokensBase):
    pass

class AccessTokenCreateResponse(BaseModel, IdBase):
    pass
