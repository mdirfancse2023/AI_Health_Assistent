from fastapi import APIRouter, Depends, HTTPException, status

from models.request_models import LoginRequest, SignupRequest
from models.user_model import User
from services.auth_service import get_current_user, login_user, register_user, serialize_user

router = APIRouter()


@router.post("/auth/signup")
def signup(request: SignupRequest):
    try:
        return register_user(request.username, request.email, request.password)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/auth/login")
def login(request: LoginRequest):
    return login_user(request.identifier, request.password)


@router.get("/auth/me")
def current_user(current_user: User = Depends(get_current_user)):
    return serialize_user(current_user)
