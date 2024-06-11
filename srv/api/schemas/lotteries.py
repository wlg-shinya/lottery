from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class LotteriesBase(BaseModel):
    text: str = Field("", desciption="くじ引きの抽選対象")
    title: str = Field("", desciption="くじ引き名")
    description: str = Field("", desciption="このくじ引きの説明")

class Lotteries(LotteriesBase):
    id: int
    created_at: datetime = Field(desciption="作成日時")
    updated_at: datetime | None = Field(desciption="更新日時")
    user_id: int = Field(desciption="このくじ引きの所有者ID")
    used_count: int | None = Field(0, desciption="このくじ引きが抽選された回数")

    model_config = ConfigDict(from_attributes=True)

class LotteryCreate(LotteriesBase):
    access_token: str = Field(desciption="アクセストークン")

class LotteryCreateResponse(LotteriesBase):
    id: int
    user_id: int = Field(desciption="このくじ引きの所有者ID")

    model_config = ConfigDict(from_attributes=True)

class LotteryDelete(BaseModel):
    access_token: str = Field(desciption="アクセストークン")
