from fastapi import FastAPI

from app.config import settings
from app.database import init_db
from app.routers import router

app = FastAPI(title=settings.project_name)
app.include_router(router)


@app.on_event("startup")
async def start_db():
    await init_db()
