from sqlmodel import SQLModel, create_engine, Session
from typing import Generator
import os

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./task_management.db")

# Create database engine
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL query logging
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)


def create_db_and_tables():
    """Create database tables"""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Dependency to get database session"""
    with Session(engine) as session:
        yield session 