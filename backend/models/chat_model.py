from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from db.database import Base

class ChatLog(Base):
    __tablename__ = "chat_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, default="default_user")   # 🔥 NEW
    message = Column(String)
    emotion = Column(String)
    response = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)