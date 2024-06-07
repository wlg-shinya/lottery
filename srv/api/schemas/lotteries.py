from pydantic import BaseModel, ConfigDict, Field
import datetime

class LotteriesBase(BaseModel):
    user_id: int = Field(desciption="このくじ引きの所有者ID")
    text: str = Field("", desciption="くじ引きの抽選対象")
    title: str = Field("", desciption="くじ引き名")

class Lotteries(LotteriesBase):
    id: int
    created_at: datetime.datetime = Field(desciption="作成日時")
    updated_at: datetime.datetime | None = Field(desciption="更新日時")

    model_config = ConfigDict(from_attributes=True)

class LotteryCreate(LotteriesBase):
    pass

class LotteryCreateResponse(LotteryCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
