from fastapi import FastAPI

from app.api.routers import items

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(items.router)