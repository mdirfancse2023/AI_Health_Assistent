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
    feedback_score = Column(Integer, default=0) # 1 to 5 scale, 0 means unrated
    created_at = Column(DateTime, default=datetime.utcnow)

class DailyCheckin(Base):
    __tablename__ = "daily_checkins"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, default="default_user")
    stress_level = Column(Integer)  # 1 to 10
    academic_focus = Column(Integer) # 1 to 10
    created_at = Column(DateTime, default=datetime.utcnow)