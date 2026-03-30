import os
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

from routes.chat_routes import router as chat_router
from db.database import Base, engine

from routes.analytics_routes import router as analytics_router

app = FastAPI(title="AI Mental Health Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:80",
        "http://localhost:4200",
        "http://app.34.30.233.97.sslip.io",
        "https://app.34.30.233.97.sslip.io",
        "*"  # Fallback for any other origins
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(chat_router)

app.include_router(analytics_router)

@app.get("/")
def home():
    return {"message": "AI Mental Health Assistant is running 🚀"}