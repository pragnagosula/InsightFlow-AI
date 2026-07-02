from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.core.database import connect_db, close_db
from app.core.embeddings import load_embedding_model
from app.core.storage import ensure_dirs
from app.api.v1.router import api_router

# Create storage directories before app and static file mounts are initialised
ensure_dirs()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    load_embedding_model()
    yield
    await close_db()


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/storage/charts", StaticFiles(directory=str(settings.CHARTS_DIR)), name="charts")

app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
async def health():
    return {"status": "ok", "app": settings.APP_NAME}
