from fastapi import APIRouter
from models.request_models import ChatRequest
from services.chat_service import process_chat

router = APIRouter()

@router.post("/chat")
async def chat(req: ChatRequest):
    result = process_chat(req.message)
    return result