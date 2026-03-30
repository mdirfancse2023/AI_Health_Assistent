from db.database import SessionLocal
from models.chat_model import ChatLog
from collections import Counter


def get_emotion_distribution(user_id: str):
    db = SessionLocal()
    try:
        chats = db.query(ChatLog)\
            .filter(ChatLog.user_id == user_id)\
            .all()

        emotions = [chat.emotion for chat in chats]
        result = dict(Counter(emotions))
        return result
    finally:
        db.close()


def get_chat_trend(user_id: str):
    db = SessionLocal()
    try:
        chats = db.query(ChatLog)\
            .filter(ChatLog.user_id == user_id)\
            .all()

        trend = {}

        for chat in chats:
            date = chat.created_at.strftime("%Y-%m-%d")
            trend[date] = trend.get(date, 0) + 1

        return trend
    finally:
        db.close()

from models.chat_model import DailyCheckin


def get_effectiveness_score(user_id: str):
    db = SessionLocal()
    try:
        chats = db.query(ChatLog).filter(ChatLog.user_id == user_id, ChatLog.feedback_score != 0).all()
        
        if not chats:
            return 0.0
            
        total_score = sum(chat.feedback_score for chat in chats)
        avg_score = total_score / len(chats)
        return round(avg_score, 2)
    finally:
        db.close()


def get_stress_and_academic_trend(user_id: str):
    db = SessionLocal()
    try:
        checkins = db.query(DailyCheckin).filter(DailyCheckin.user_id == user_id).order_by(DailyCheckin.created_at.asc()).all()
        
        trend = []
        for checkin in checkins:
            trend.append({
                "date": checkin.created_at.strftime("%Y-%m-%d"),
                "stress_level": checkin.stress_level,
                "academic_focus": checkin.academic_focus
            })
            
        return trend
    finally:
        db.close()
