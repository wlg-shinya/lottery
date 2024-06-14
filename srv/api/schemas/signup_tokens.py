from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from api.schemas.common import IdBase, CreatedUpdatedAtBase
from api.schemas.users import UserCreateBase
from core.config import default_timezone

def default_expire_at():
    return datetime.now(default_timezone()) + timedelta(minutes=10)

class SignupTokensBase(UserCreateBase):
    token: str = Field(json_schema_extra={ "desciption": "サインアップトークン" })
    expire_at: datetime = Field(default=default_expire_at(), json_schema_extra={ "desciption": "有効期限" })

class SignupTokens(BaseModel, IdBase, CreatedUpdatedAtBase, SignupTokensBase):
    pass

class SignupTokenCreate(BaseModel, SignupTokensBase):
    pass

class SignupTokenCreateResponse(BaseModel, IdBase):
    pass
