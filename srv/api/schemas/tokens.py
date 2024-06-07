from pydantic import BaseModel, ConfigDict, Field
import datetime

def default_expire_at():
    return datetime.datetime.now() + datetime.timedelta(days=3)

class TokensBase(BaseModel):
    access_token: str = Field(desciption="アクセストークン")
    user_id: int = Field(desciption="ユーザーID")
    expire_at: datetime.datetime = Field(default_expire_at(), desciption="有効期限")

class Tokens(TokensBase):
    id: int
    created_at: datetime.datetime = Field(desciption="作成日時")
    updated_at: datetime.datetime | None = Field(desciption="更新日時")

    model_config = ConfigDict(from_attributes=True)

class TokenCreate(TokensBase):
    pass

class TokenCreateResponse(TokensBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
