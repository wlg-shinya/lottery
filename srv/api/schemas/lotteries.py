from pydantic import BaseModel, ConfigDict, Field

class LotteriesBase(BaseModel):
    user_id: int = Field(-1, desciption="このくじ引きの所有者ID")
    text: str = Field("", desciption="くじ引きの抽選対象")
    title: str = Field("", desciption="くじ引き名")

class Lotteries(LotteriesBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class LotteryCreate(LotteriesBase):
    pass

class LotteryCreateResponse(LotteryCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
