from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from models.request_models import ChatRequest, FeedbackRequest, DailyCheckinRequest
from models.user_model import User
from services.auth_service import get_current_user
from services.chat_service import process_chat_stream
from db.chat_repository import save_feedback, save_daily_checkin

router = APIRouter()


@router.post("/chat")
def chat(request: ChatRequest, current_user: User = Depends(get_current_user)):
    return StreamingResponse(
        process_chat_stream(request.message, str(current_user.id)),
        media_type="text/event-stream",
    )


@router.post("/chat/feedback/{chat_id}")
def feedback(chat_id: int, request: FeedbackRequest, current_user: User = Depends(get_current_user)):
    updated = save_feedback(chat_id, str(current_user.id), request.score)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found.")
    return {"status": "success"}


@router.post("/chat/checkin")
def checkin(request: DailyCheckinRequest, current_user: User = Depends(get_current_user)):
    save_daily_checkin(str(current_user.id), request.stress_level, request.academic_focus)
    return {"status": "success"}
