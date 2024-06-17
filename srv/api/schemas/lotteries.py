from pydantic import BaseModel, Field
from api.schemas.common import IdBase, CreatedUpdatedAtBase, AccessTokenBase

class LotteriesBase():
    text: str = Field(default="", json_schema_extra={ "desciption": "くじ引きの抽選対象" })
    title: str = Field(default="", json_schema_extra={ "desciption": "くじ引き名" })
    description: str = Field(default="", json_schema_extra={ "desciption": "このくじ引きの説明" })

class UserIdBase():
    user_id: int = Field(json_schema_extra={ "desciption": "このくじ引きの所有者ID" })

class Lotteries(BaseModel, IdBase, CreatedUpdatedAtBase, UserIdBase, LotteriesBase):
    used_count: int | None = Field(default=0, json_schema_extra={ "desciption": "このくじ引きが抽選された回数" })

class LotteryCreate(BaseModel, AccessTokenBase, LotteriesBase):
    pass

class LotteryCreateResponse(BaseModel, IdBase, UserIdBase):
    pass
