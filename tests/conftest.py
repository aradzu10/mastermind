import pytest
from backend.db.database import engine


@pytest.fixture(scope="function", autouse=True)
async def cleanup_db():
    """Cleanup database connections after each test"""
    yield
    # Dispose of all connections to avoid event loop conflicts
    await engine.dispose()
