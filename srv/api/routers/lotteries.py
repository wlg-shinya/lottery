from fastapi import APIRouter

router = APIRouter()

@router.get("/api/read_lotteries")
async def read_lotteries():
    pass
