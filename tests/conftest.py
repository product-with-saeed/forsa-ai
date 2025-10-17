"""Pytest configuration and fixtures for Forsa AI tests.

This module provides reusable fixtures for testing database models,
services, and API endpoints. All tests use an isolated test database
that is created fresh for each test session and cleaned up after.

Fixtures:
    engine: SQLAlchemy async engine for test database
    session: Database session for each test (auto-rollback)
    client: FastAPI test client
"""

from typing import AsyncGenerator, Generator
from uuid import uuid4

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from fastapi.testclient import TestClient

from app.models.base import Base
from app.main import app


# Test database URL (separate from development database)
TEST_DATABASE_URL = "postgresql+asyncpg://forsa_user:forsa_password@localhost:5433/forsa_test_db"


@pytest_asyncio.fixture(scope="session")
async def engine():
    """Create test database engine.

    Creates a fresh test database engine with NullPool to avoid
    connection issues in tests. Engine is shared across test session.

    Yields:
        SQLAlchemy async engine connected to test database
    """
    test_engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,  # Set True to see SQL queries
        poolclass=NullPool,  # Disable connection pooling for tests
    )

    # Create all tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield test_engine

    # Drop all tables after tests
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await test_engine.dispose()


@pytest_asyncio.fixture
async def session(engine) -> AsyncGenerator[AsyncSession, None]:
    """Create database session for each test with automatic rollback.

    Each test gets a fresh session that is automatically rolled back
    after the test completes, ensuring test isolation.

    Args:
        engine: Test database engine fixture

    Yields:
        Database session for the test
    """
    async_session_maker = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session_maker() as session:
        yield session
        await session.rollback()


@pytest.fixture
def client() -> Generator:
    """Create FastAPI test client.

    Provides a test client for making HTTP requests to the API
    without running a real server.

    Yields:
        FastAPI TestClient instance
    """
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def sample_uuid() -> str:
    """Generate a sample UUID for testing.

    Returns:
        UUID string
    """
    return str(uuid4())


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers and settings."""
    config.addinivalue_line(
        "markers",
        "unit: Unit tests that don't require database"
    )
    config.addinivalue_line(
        "markers",
        "integration: Integration tests that require database"
    )
    config.addinivalue_line(
        "markers",
        "multilingual: Tests for multilingual functionality"
    )
