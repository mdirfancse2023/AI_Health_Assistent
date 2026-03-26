from db.database import SessionLocal
from models.chat_model import ChatLog

def save_chat(user_id, message, emotion, response):
    db = SessionLocal()
    chat = ChatLog(
        user_id=user_id,
        message=message,
        emotion=emotion,
        response=response
    )
    db.add(chat)
    db.commit()
    db.close()


def get_recent_chats(user_id, limit=5):
    db = SessionLocal()
    chats = db.query(ChatLog)\
        .filter(ChatLog.user_id == user_id)\
        .order_by(ChatLog.created_at.desc())\
        .limit(limit)\
        .all()
    db.close()
    return chats


def get_emotion_summary(user_id):
    db = SessionLocal()
    chats = db.query(ChatLog)\
        .filter(ChatLog.user_id == user_id)\
        .all()

    emotion_count = {}

    for chat in chats:
        emotion = chat.emotion
        emotion_count[emotion] = emotion_count.get(emotion, 0) + 1

    db.close()
    return emotion_count