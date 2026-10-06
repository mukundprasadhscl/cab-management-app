"""Database engine, session factory, and initialisation."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import Base

DATABASE_URL = "sqlite:///cab_management.db"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)


def init_db(db_engine=None):
    """Create all tables if they do not exist yet."""
    target = db_engine or engine
    Base.metadata.create_all(target)


def get_session(db_engine=None):
    """Return a new session — caller is responsible for closing it."""
    if db_engine:
        return sessionmaker(bind=db_engine)()
    return SessionLocal()
