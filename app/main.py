from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base

from app.modules.users.router import router as users_router
from app.modules.clicks.router import router as clicks_router
from app.modules.farm_template.router import router as farm_template_router
from app.modules.user_farm.router import router as user_farm_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all, checkfirst=True)
    print("Application started")
    
    yield
    
    await engine.dispose()
    print("Application shutdown")

app = FastAPI(
    title="Telegram Clicker API",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router, prefix="/api/v1")
app.include_router(clicks_router, prefix="/api/v1")
app.include_router(farm_template_router, prefix="/api/v1")
app.include_router(user_farm_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000
    )