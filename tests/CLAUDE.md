# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Testing Architecture

Three-level testing strategy:
- **Unit tests**: Test individual functions and classes in isolation
- **Integration tests**: Test API endpoints with test database
- **E2E tests**: Test full user workflows (planned for future)

## Commands

```bash
# From project root with venv activated
source .venv/bin/activate

# Run all tests
pytest

# Run specific test directory
pytest tests/unit/
pytest tests/integration/

# Run specific test file
pytest tests/unit/test_mastermind_logic.py

# Run specific test
pytest tests/unit/test_mastermind_logic.py::test_evaluate_guess

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=backend --cov-report=html
```

## Directory Structure

- `unit/` - Fast, isolated tests
  - `test_mastermind_logic.py` - Core game logic tests (from legacy)
- `integration/` - API endpoint tests with database
  - `test_games_api.py` - Game API integration tests
- `e2e/` - End-to-end browser tests (future: Playwright)
- `conftest.py` - Shared pytest fixtures

## Test Configuration

### pytest.ini (in pyproject.toml)
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]
asyncio_mode = "auto"
addopts = "-v --tb=short"
```

- `asyncio_mode = "auto"` - Automatically detects and runs async tests
- `pythonpath = ["."]` - Allows importing `backend.*` from project root
- `testpaths = ["tests"]` - Only search `tests/` directory

## Unit Tests

Test pure logic in isolation (no database, no API calls).

### test_mastermind_logic.py
Tests the core `MasterMindGame` class:
- `test_evaluate_guess()` - Feedback calculation (exact, wrong_pos)
- `test_duplicates()` - Handling duplicate digits
- `test_validation()` - Input validation

Example:
```python
def test_evaluate_guess():
    game = MasterMindGame(secret="1234")
    exact, wrong_pos = game.evaluate_guess("1243")
    assert exact == 2  # 1 and 2 in correct positions
    assert wrong_pos == 2  # 3 and 4 in wrong positions
```

## Integration Tests

Test API endpoints with real HTTP requests and test database.

### test_games_api.py
Tests FastAPI endpoints:
- `test_health_check()` - GET /api/health
- `test_root()` - GET /
- `test_create_game()` - POST /api/games/single (future)
- `test_make_guess()` - POST /api/games/{id}/guess (future)

Uses `TestClient` from FastAPI:
```python
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
```

## Fixtures (conftest.py)

### cleanup_db
Auto-runs after each test to dispose database connections:
```python
@pytest.fixture(scope="function", autouse=True)
async def cleanup_db():
    yield
    await engine.dispose()
```

Prevents event loop conflicts in async tests.

## Testing Best Practices

### Unit Tests
- Test one thing per test function
- Use descriptive test names (`test_evaluate_guess_with_duplicates`)
- No database or API calls
- Fast execution (<1ms per test)
- Mock external dependencies

### Integration Tests
- Test full request/response cycle
- Use test database (not production)
- Clean up test data after each test
- Test error cases (400, 404, 500)
- Verify JSON response structure

### Test Organization
```python
# Arrange - Set up test data
game = MasterMindGame(secret="1234")

# Act - Perform the operation
result = game.evaluate_guess("1243")

# Assert - Verify the result
assert result == (2, 2)
```

## Running Tests in Docker

```bash
# Start test database
docker-compose up -d postgres

# Run tests in Docker
docker-compose exec backend pytest

# Run with coverage
docker-compose exec backend pytest --cov=backend
```

## Async Testing

pytest-asyncio handles async tests automatically:

```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await some_async_function()
    assert result == expected_value
```

With `asyncio_mode = "auto"`, the `@pytest.mark.asyncio` decorator is optional.

## Test Database Setup

Integration tests use the same database as development (for now). Future improvement: separate test database.

To reset database for clean tests:
```bash
docker-compose down -v  # Remove volumes
docker-compose up -d postgres
alembic upgrade head
```

## Adding New Tests

### New Unit Test
1. Create test file in `tests/unit/test_<module>.py`
2. Import module to test
3. Write test functions starting with `test_`
4. Run `pytest tests/unit/test_<module>.py`

### New Integration Test
1. Create test file in `tests/integration/test_<feature>_api.py`
2. Import `TestClient` and `app`
3. Write tests using `client.get()`, `client.post()`, etc.
4. Clean up test data in teardown
5. Run `pytest tests/integration/`

## Coverage

Generate coverage report:
```bash
pytest --cov=backend --cov-report=html
open htmlcov/index.html
```

Target: >80% coverage for backend code.

## Important Notes

- All tests must be idempotent (can run multiple times safely)
- Tests should not depend on each other (execution order independent)
- Use fixtures for common setup/teardown
- Mock external services (future: OAuth, WebSockets)
- Integration tests require Docker postgres running
- Unit tests can run without database
