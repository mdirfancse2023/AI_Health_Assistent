import os
import time
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
else:
    # Fallback to in-memory SQLite to prevent startup crashes when env vars are missing
    DATABASE_URL = "sqlite:///:memory:"

print("DB URL:", DATABASE_URL)  # optional debug

engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

def wait_for_database(max_attempts: int = 30, delay_seconds: int = 2) -> None:
    last_error = None

    for attempt in range(1, max_attempts + 1):
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            print("Database connection established.")
            return
        except OperationalError as exc:
            last_error = exc
            print(f"Database not ready (attempt {attempt}/{max_attempts}): {exc}")
            if attempt < max_attempts:
                time.sleep(delay_seconds)

    raise last_error
