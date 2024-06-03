from typing import Optional
from pydantic import BaseModel, Field

class Lotteries(BaseModel):
    id: int
    user_id: int = Field(desciption="このくじ引きの所有者ID")
    text: str = Field("", desciption="くじ引きの抽選対象")
    title: str = Field("", desciption="くじ引き名")