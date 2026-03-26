from db.database import SessionLocal
from models.chat_model import ChatLog
from collections import Counter
from datetime import datetime


def get_emotion_distribution(user_id="student_1"):
    db = SessionLocal()

    chats = db.query(ChatLog)\
        .filter(ChatLog.user_id == user_id)\
        .all()

    emotions = [chat.emotion for chat in chats]
    result = dict(Counter(emotions))

    db.close()
    return result


def get_chat_trend(user_id="student_1"):
    db = SessionLocal()

    chats = db.query(ChatLog)\
        .filter(ChatLog.user_id == user_id)\
        .all()

    trend = {}

    for chat in chats:
        date = chat.created_at.strftime("%Y-%m-%d")
        trend[date] = trend.get(date, 0) + 1

    db.close()
    return trend