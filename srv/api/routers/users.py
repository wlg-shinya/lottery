from fastapi import APIRouter

router = APIRouter()

@router.get("/api/read_users")
async def read_users():
    pass
