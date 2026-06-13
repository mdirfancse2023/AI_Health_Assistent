import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

from routes.chat_routes import router as chat_router
from routes.auth_routes import router as auth_router
from db.database import Base, engine, wait_for_database

from routes.analytics_routes import router as analytics_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Skip long DB connection loops on Vercel serverless environment
    if not os.getenv("VERCEL"):
        wait_for_database()
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Lifespan database creation failed: {e}")
    yield





def create_app() -> FastAPI:
    api = FastAPI(title="AI Mental Health Assistant", lifespan=lifespan)

    @api.get("/health")
    @api.get("/api/health")
    def health():
        from sqlalchemy import text
        db_status = "unknown"
        db_error = None
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            db_status = "connected"
        except Exception as e:
            db_status = "failed"
            db_error = str(e)
        
        return {
            "status": "healthy",
            "database": db_status,
            "database_error": db_error,
            "database_url_configured": bool(os.getenv("DATABASE_URL")),
            "vercel": bool(os.getenv("VERCEL")),
            "openrouter_configured": bool(os.getenv("OPENROUTER_API_KEY")),
        }

    api.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:4200",
            "http://localhost:8000",
            "http://health.34.30.233.97.sslip.io",
            "https://health.34.30.233.97.sslip.io",
            "https://capstone-mental-health.web.app",
            "https://ai-mental-health.blackocean-872335af.centralindia.azurecontainerapps.io",
            "https://virtualgyans.tech",
            "https://www.virtualgyans.tech",
            "https://healthai.virtualgyans.tech",
            "https://virtualgyans.me",
            "http://virtualgyans.me",
            "https://mdirfancse2023.github.io",
            "http://mdirfancse2023.github.io",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    api.include_router(auth_router)
    api.include_router(auth_router, prefix="/api")
    api.include_router(chat_router)
    api.include_router(chat_router, prefix="/api")
    api.include_router(analytics_router)
    api.include_router(analytics_router, prefix="/api")

    @api.get("/")
    def read_root():
        return {
            "message": "AI Powered Mental Health Assistant API is running",
            "docs": "/docs",
            "health": "/health"
        }

    return api


app = FastAPI()
# Serve at both root and /aimentalhealth for compatibility
app.mount("", create_app())
app.mount("/aimentalhealth", create_app())
