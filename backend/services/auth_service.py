import base64
import hashlib
import hmac
import json
import os
import secrets
import time

from fastapi import Header, HTTPException, status

from db.user_repository import (
    create_user,
    get_user_by_email,
    get_user_by_id,
    get_user_by_identifier,
    get_user_by_username,
)
from models.user_model import User

AUTH_SECRET_KEY = os.getenv("AUTH_SECRET_KEY", "mental-health-dev-secret")
TOKEN_TTL_SECONDS = int(os.getenv("AUTH_TOKEN_TTL_SECONDS", "604800"))
PASSWORD_ITERATIONS = 390000


def _base64url_encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode("ascii")


def _base64url_decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(value + padding)


def _bad_auth_error(detail: str = "Invalid authentication credentials") -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def serialize_user(user: User) -> dict[str, str | int]:
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
    }


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PASSWORD_ITERATIONS)
    return (
        f"pbkdf2_sha256${PASSWORD_ITERATIONS}$"
        f"{_base64url_encode(salt)}${_base64url_encode(digest)}"
    )


def verify_password(password: str, password_hash: str) -> bool:
    try:
        algorithm, iterations, salt_value, digest_value = password_hash.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False
        salt = _base64url_decode(salt_value)
        expected_digest = _base64url_decode(digest_value)
        actual_digest = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            int(iterations),
        )
        return hmac.compare_digest(actual_digest, expected_digest)
    except (ValueError, TypeError):
        return False


def create_access_token(user: User) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "sub": str(user.id),
        "username": user.username,
        "email": user.email,
        "exp": int(time.time()) + TOKEN_TTL_SECONDS,
    }

    encoded_header = _base64url_encode(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    encoded_payload = _base64url_encode(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    unsigned_token = f"{encoded_header}.{encoded_payload}"
    signature = hmac.new(
        AUTH_SECRET_KEY.encode("utf-8"),
        unsigned_token.encode("utf-8"),
        hashlib.sha256,
    ).digest()
    return f"{unsigned_token}.{_base64url_encode(signature)}"


def decode_access_token(token: str) -> dict[str, str | int]:
    try:
        encoded_header, encoded_payload, encoded_signature = token.split(".", 2)
    except ValueError as exc:
        raise _bad_auth_error() from exc

    unsigned_token = f"{encoded_header}.{encoded_payload}"
    expected_signature = hmac.new(
        AUTH_SECRET_KEY.encode("utf-8"),
        unsigned_token.encode("utf-8"),
        hashlib.sha256,
    ).digest()

    if not hmac.compare_digest(_base64url_encode(expected_signature), encoded_signature):
        raise _bad_auth_error()

    try:
        payload = json.loads(_base64url_decode(encoded_payload).decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise _bad_auth_error() from exc

    if int(payload.get("exp", 0)) <= int(time.time()):
        raise _bad_auth_error("Token has expired")

    return payload


def _token_response(user: User) -> dict[str, str | dict[str, str | int]]:
    return {
        "access_token": create_access_token(user),
        "token_type": "bearer",
        "user": serialize_user(user),
    }


def register_user(username: str, email: str, password: str) -> dict[str, str | dict[str, str | int]]:
    normalized_username = username.strip()
    normalized_email = email.strip().lower()

    if len(normalized_username) < 3:
        raise ValueError("Username must be at least 3 characters long.")
    if "@" not in normalized_email or "." not in normalized_email:
        raise ValueError("Please provide a valid email address.")
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long.")
    if get_user_by_username(normalized_username):
        raise ValueError("That username is already in use.")
    if get_user_by_email(normalized_email):
        raise ValueError("That email is already in use.")

    user = create_user(normalized_username, normalized_email, hash_password(password))
    return _token_response(user)


def login_user(identifier: str, password: str) -> dict[str, str | dict[str, str | int]]:
    normalized_identifier = identifier.strip().lower()
    user = get_user_by_identifier(normalized_identifier)

    if not user:
        user = get_user_by_identifier(identifier.strip())

    if not user or not verify_password(password, user.password_hash):
        raise _bad_auth_error("Invalid username/email or password.")

    return _token_response(user)


def get_current_user(authorization: str | None = Header(default=None)) -> User:
    if not authorization or not authorization.startswith("Bearer "):
        raise _bad_auth_error("Authentication required.")

    token = authorization.split(" ", 1)[1].strip()
    payload = decode_access_token(token)

    try:
        user_id = int(payload["sub"])
    except (KeyError, TypeError, ValueError) as exc:
        raise _bad_auth_error() from exc

    user = get_user_by_id(user_id)
    if not user:
        raise _bad_auth_error("User no longer exists.")

    return user
