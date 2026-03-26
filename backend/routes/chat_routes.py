from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from models.request_models import ChatRequest, FeedbackRequest, DailyCheckinRequest
from services.chat_service import process_chat_stream
from db.chat_repository import save_feedback, save_daily_checkin

router = APIRouter()


@router.post("/chat")
def chat(request: ChatRequest):
    return StreamingResponse(process_chat_stream(request.message, request.user_id), media_type="text/event-stream")

@router.post("/chat/feedback/{chat_id}")
def feedback(chat_id: int, request: FeedbackRequest):
    save_feedback(chat_id, request.score)
    return {"status": "success"}

@router.post("/chat/checkin")
def checkin(request: DailyCheckinRequest):
    save_daily_checkin(request.user_id, request.stress_level, request.academic_focus)
    return {"status": "success"}