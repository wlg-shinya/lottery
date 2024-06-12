from pydantic import Field
from datetime import datetime

class IdBase():
    id: int

class CreatedUpdatedAtBase():
    created_at: datetime = Field(desciption="作成日時")
    updated_at: datetime | None = Field(desciption="更新日時")

class AccessTokenBase():
    access_token: str = Field(desciption="アクセストークン")
