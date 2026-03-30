from fastapi import APIRouter, Depends
from models.user_model import User
from services.analytics_service import get_emotion_distribution, get_chat_trend, get_effectiveness_score, get_stress_and_academic_trend
from services.auth_service import get_current_user

router = APIRouter()


@router.get("/analytics/emotions")
def emotion_data(current_user: User = Depends(get_current_user)):
    return get_emotion_distribution(str(current_user.id))


@router.get("/analytics/trend")
def trend_data(current_user: User = Depends(get_current_user)):
    return get_chat_trend(str(current_user.id))


@router.get("/analytics/effectiveness")
def effectiveness_data(current_user: User = Depends(get_current_user)):
    return {"score": get_effectiveness_score(str(current_user.id))}


@router.get("/analytics/stress_academic")
def stress_academic_data(current_user: User = Depends(get_current_user)):
    return get_stress_and_academic_trend(str(current_user.id))
