from fastapi import APIRouter
from pydantic import BaseModel
from services.chat_service import process_chat

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    user_id: str = "default_user"   # 🔥 NEW


@router.post("/chat")
def chat(request: ChatRequest):
    return process_chat(request.message, request.user_id)