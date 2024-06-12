from pydantic import BaseModel, Field
from api.schemas.common import IdBase, CreatedUpdatedAtBase, AccessTokenBase

class LotteriesBase():
    text: str = Field("", desciption="くじ引きの抽選対象")
    title: str = Field("", desciption="くじ引き名")
    description: str = Field("", desciption="このくじ引きの説明")

class UserIdBase():
    user_id: int = Field(desciption="このくじ引きの所有者ID")

class Lotteries(BaseModel, IdBase, CreatedUpdatedAtBase, UserIdBase, LotteriesBase):
    used_count: int | None = Field(0, desciption="このくじ引きが抽選された回数")

class LotteryCreate(BaseModel, AccessTokenBase, LotteriesBase):
    pass

class LotteryCreateResponse(BaseModel, IdBase, UserIdBase):
    pass

class LotteryDelete(BaseModel, AccessTokenBase):
    pass
