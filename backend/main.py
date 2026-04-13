import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
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


app = FastAPI(title="AI Mental Health Assistant", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "http://localhost:8000",
        "http://health.34.30.233.97.sslip.io",
        "https://health.34.30.233.97.sslip.io",
        "https://capstone-mental-health.web.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# API routes (must come before static mount)
app.include_router(auth_router)
app.include_router(auth_router, prefix="/api")
app.include_router(chat_router)
app.include_router(chat_router, prefix="/api")
app.include_router(analytics_router)
app.include_router(analytics_router, prefix="/api")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
    return FileResponse("static/index.html")

# Catch-all route for Angular SPA routing
@app.get("/{path:path}")
def catch_all(path: str):
    # Don't catch API routes or static files
    if path.startswith("api/") or path.startswith("static/"):
        return {"error": "Not found"}
    return FileResponse("static/index.html")
