from pydantic import Field
from datetime import datetime

class IdBase():
    id: int

class CreatedUpdatedAtBase():
    created_at: datetime = Field(json_schema_extra={ "desciption": "作成日時" })
    updated_at: datetime | None = Field(json_schema_extra={ "desciption": "更新日時" })

class AccessTokenBase():
    access_token: str = Field(json_schema_extra={ "desciption": "アクセストークン" })
