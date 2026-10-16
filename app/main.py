from asyncio import ensure_future

import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from app.api.routers import users, auth, todos
from app.db.database import Base, engine
from app.db import models  # noqa: F401 — регистрирует модели в Base.metadata для create_all



app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(todos.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)









if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)