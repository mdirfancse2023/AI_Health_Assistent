from db.database import SessionLocal
from models.user_model import User


def get_user_by_id(user_id: int) -> User | None:
    db = SessionLocal()
    try:
        return db.query(User).filter(User.id == user_id).first()
    finally:
        db.close()


def get_user_by_username(username: str) -> User | None:
    db = SessionLocal()
    try:
        return db.query(User).filter(User.username == username).first()
    finally:
        db.close()


def get_user_by_email(email: str) -> User | None:
    db = SessionLocal()
    try:
        return db.query(User).filter(User.email == email).first()
    finally:
        db.close()


def get_user_by_identifier(identifier: str) -> User | None:
    db = SessionLocal()
    try:
        return db.query(User).filter((User.username == identifier) | (User.email == identifier)).first()
    finally:
        db.close()


def create_user(username: str, email: str, password_hash: str) -> User:
    db = SessionLocal()
    try:
        user = User(username=username, email=email, password_hash=password_hash)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    finally:
        db.close()
