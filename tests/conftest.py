"""Shared test fixtures for the cab-management-app test suite."""

import pytest
from sqlalchemy import create_engine

from database.db import init_db, get_session


@pytest.fixture()
def db_engine():
    """Create a fresh in-memory SQLite engine with all tables."""
    engine = create_engine("sqlite:///:memory:")
    init_db(db_engine=engine)
    return engine


@pytest.fixture()
def db_session(db_engine):
    """Yield a session backed by the in-memory engine; close after test."""
    session = get_session(db_engine=db_engine)
    yield session
    session.close()
