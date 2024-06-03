from fastapi import APIRouter
from api.database import Database

router = APIRouter()

@router.get("/api/read_users")
async def read_users():
    try:
        message = Database().execute("SELECT version();")
        return { "message": message }
    
    except Exception as e:
        return e
