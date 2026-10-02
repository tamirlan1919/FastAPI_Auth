import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from app.api.routers import users, auth

app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)