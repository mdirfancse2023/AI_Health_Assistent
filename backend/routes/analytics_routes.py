from fastapi import APIRouter
from services.analytics_service import get_emotion_distribution, get_chat_trend

router = APIRouter()

@router.get("/analytics/emotions")
def emotion_data():
    return get_emotion_distribution()

@router.get("/analytics/trend")
def trend_data():
    return get_chat_trend()