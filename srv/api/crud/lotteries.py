from sqlalchemy.ext.asyncio import AsyncSession

from api.models import Lotteries as Model
import api.schemas.lotteries as schema

async def create_lottery(
    db: AsyncSession, schema: schema.LotteryCreate
) -> Model:
    model = Model(**schema.model_dump())
    db.add(model)
    await db.commit()
    await db.refresh(model)
    return model
