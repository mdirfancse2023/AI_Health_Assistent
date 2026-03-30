from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    user_id: str = "default_user"


class FeedbackRequest(BaseModel):
    score: int  # e.g., 1 to 5, or -1, 1


class DailyCheckinRequest(BaseModel):
    user_id: str = "default_user"
    stress_level: int
    academic_focus: int


class SignupRequest(BaseModel):
    username: str
    email: str
    password: str


class LoginRequest(BaseModel):
    identifier: str
    password: str
