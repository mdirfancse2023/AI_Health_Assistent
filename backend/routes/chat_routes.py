from fastapi import APIRouter
from models.request_models import ChatRequest, FeedbackRequest, DailyCheckinRequest
from services.chat_service import process_chat
from db.chat_repository import save_feedback, save_daily_checkin

router = APIRouter()


@router.post("/chat")
def chat(request: ChatRequest):
    return process_chat(request.message, request.user_id)

@router.post("/chat/feedback/{chat_id}")
def feedback(chat_id: int, request: FeedbackRequest):
    save_feedback(chat_id, request.score)
    return {"status": "success"}

@router.post("/chat/checkin")
def checkin(request: DailyCheckinRequest):
    save_daily_checkin(request.user_id, request.stress_level, request.academic_focus)
    return {"status": "success"}