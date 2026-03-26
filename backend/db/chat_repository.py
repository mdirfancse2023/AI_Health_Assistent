from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from db.database import Base, SessionLocal

class Chat(Base):
    __tablename__ = "chat_logs"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(Text)
    emotion = Column(String(50))
    response = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


def save_chat(message: str, emotion: str, response: str):
    db = SessionLocal()
    chat = Chat(
        message=message,
        emotion=emotion,
        response=response
    )
    db.add(chat)
    db.commit()
    db.close()


def get_all_chats():
    db = SessionLocal()
    chats = db.query(Chat).all()
    db.close()
    return chats