from fastapi import APIRouter
from services.analytics_service import get_emotion_distribution, get_chat_trend, get_effectiveness_score, get_stress_and_academic_trend

router = APIRouter()

@router.get("/analytics/emotions")
def emotion_data():
    return get_emotion_distribution()

@router.get("/analytics/trend")
def trend_data():
    return get_chat_trend()

@router.get("/analytics/effectiveness")
def effectiveness_data():
    return {"score": get_effectiveness_score()}

@router.get("/analytics/stress_academic")
def stress_academic_data():
    return get_stress_and_academic_trend()