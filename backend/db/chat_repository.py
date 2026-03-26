from db.database import SessionLocal
from models.chat_model import ChatLog

def save_chat(user_id, message, emotion, response):
    db = SessionLocal()
    try:
        chat = ChatLog(
            user_id=user_id,
            message=message,
            emotion=emotion,
            response=response
        )
        db.add(chat)
        db.commit()
        db.refresh(chat) # Refresh to get the generated ID
        return chat.id
    finally:
        db.close()


def get_recent_chats(user_id, limit=5):
    db = SessionLocal()
    try:
        chats = db.query(ChatLog)\
            .filter(ChatLog.user_id == user_id)\
            .order_by(ChatLog.created_at.desc())\
            .limit(limit)\
            .all()
        return chats
    finally:
        db.close()


def get_emotion_summary(user_id):
    db = SessionLocal()
    try:
        chats = db.query(ChatLog)\
            .filter(ChatLog.user_id == user_id)\
            .all()

        emotion_count = {}

        for chat in chats:
            emotion = chat.emotion
            emotion_count[emotion] = emotion_count.get(emotion, 0) + 1

        return emotion_count
    finally:
        db.close()

def save_feedback(chat_id: int, score: int):
    db = SessionLocal()
    try:
        chat = db.query(ChatLog).filter(ChatLog.id == chat_id).first()
        if chat:
            chat.feedback_score = score
            db.commit()
    finally:
        db.close()

from models.chat_model import DailyCheckin

def save_daily_checkin(user_id: str, stress_level: int, academic_focus: int):
    db = SessionLocal()
    try:
        checkin = DailyCheckin(
            user_id=user_id,
            stress_level=stress_level,
            academic_focus=academic_focus
        )
        db.add(checkin)
        db.commit()
    finally:
        db.close()