from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class TokensBase(BaseModel):
    user_id: int = Field(desciption="ユーザーID")
    expire_at: datetime = Field(datetime.now() + datetime(day=3), desciption="有効期限")

class Tokens(TokensBase):
    id: int
    access_token: str = Field(desciption="アクセストークン")
    created_at: datetime = Field(desciption="作成日時")
    updated_at: datetime | None = Field(desciption="更新日時")

    model_config = ConfigDict(from_attributes=True)

class TokenCreate(TokensBase):
    # access_token にする前の文字列
    src: str

class TokenCreateResponse(TokensBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
