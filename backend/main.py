import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

from routes.chat_routes import router as chat_router
from routes.auth_routes import router as auth_router
from db.database import Base, engine, wait_for_database

from routes.analytics_routes import router as analytics_router

APP_BASE_PATH = os.getenv("APP_BASE_PATH", "/aimentalhealth").rstrip("/") or ""


@asynccontextmanager
async def lifespan(app: FastAPI):
    wait_for_database()
    Base.metadata.create_all(bind=engine)
    yield


def create_app() -> FastAPI:
    api = FastAPI(title="AI Mental Health Assistant", lifespan=lifespan)

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

    @api.get("/{path:path}")
    def catch_all(path: str):
        if path.startswith("api/"):
            return {"error": "Not found"}

        if not path:
            return FileResponse("static/index.html")

        static_file_path = os.path.join("static", path)
        if os.path.isfile(static_file_path):
            media_type = None
            if path.endswith(".js"):
                media_type = "application/javascript"
            elif path.endswith(".css"):
                media_type = "text/css"
            elif path.endswith(".ico"):
                media_type = "image/x-icon"
            return FileResponse(static_file_path, media_type=media_type)

        return FileResponse("static/index.html")

    return api


app = FastAPI()
app.mount(APP_BASE_PATH, create_app())
