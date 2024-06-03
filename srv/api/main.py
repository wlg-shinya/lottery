from fastapi import FastAPI
from api.database import Database

app = FastAPI()

@app.get("/api/read_users")
async def read_users():
    try:
        message = Database().execute("SELECT version();")
        return { "message": message }
    
    except Exception as e:
        return e
