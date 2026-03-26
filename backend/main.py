import os
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# 🔥 ABSOLUTE PATH (NO FAIL)
env_path = "/Users/macbook/Documents/GitHub/AI_Powered_Mental_Health_Assistent/.env"
load_dotenv(env_path)


print("ENV LOADED:", os.getenv("DATABASE_URL"))

from routes.chat_routes import router as chat_router
from db.database import Base, engine

app = FastAPI(title="AI Mental Health Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow Angular
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(chat_router)

@app.get("/")
def home():
    return {"message": "AI Mental Health Assistant is running 🚀"}