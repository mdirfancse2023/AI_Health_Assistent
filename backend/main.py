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
    wait_for_database()
    Base.metadata.create_all(bind=engine)
    yield


def get_index_html(base_href: str) -> str:
    """Read index.html and replace base href with the correct one"""
    index_path = os.path.join("static", "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()
            # Replace the base href
            import re
            return re.sub(
                r'<base\s+href="[^"]*"\s*>',
                f'<base href="{base_href}">',
                content
            )
    return ""


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
            "https://healthai.virtualgyans.tech",
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
    def catch_all(request: Request, path: str):
        if path.startswith("api/"):
            return {"error": "Not found"}

        # Determine base href from request URL path
        url_path = request.url.path
        base_href = "/aimentalhealth/" if url_path.startswith("/aimentalhealth") else "/"

        if not path or not os.path.isfile(os.path.join("static", path)):
            return HTMLResponse(content=get_index_html(base_href), media_type="text/html")

        static_file_path = os.path.join("static", path)
        media_type = None
        if path.endswith(".js"):
            media_type = "application/javascript"
        elif path.endswith(".css"):
            media_type = "text/css"
        elif path.endswith(".ico"):
            media_type = "image/x-icon"
        return FileResponse(static_file_path, media_type=media_type)

    return api


app = FastAPI()
# Serve at both root and /aimentalhealth for compatibility
app.mount("", create_app())
app.mount("/aimentalhealth", create_app())
