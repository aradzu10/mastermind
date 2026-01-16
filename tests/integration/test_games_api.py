import pytest
from httpx import AsyncClient, ASGITransport
from backend.main import app


@pytest.mark.asyncio
async def test_health_check():
    """Test the health check endpoint"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_root():
    """Test the root endpoint"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["version"] == "2.0.0"


@pytest.mark.asyncio
async def test_create_game():
    """Test creating a new game"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/games/single", json={"game_mode": "single"})
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["game_mode"] == "single"
    assert data["attempts"] == 0
    assert data["won"] is False


@pytest.mark.asyncio
async def test_make_guess():
    """Test making a guess"""
    # Create a game first
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        create_response = await ac.post("/api/games/single", json={"game_mode": "single"})

    game_id = create_response.json()["id"]

    # Make a guess in a new client context
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        guess_response = await ac.post(
            f"/api/games/{game_id}/guess",
            json={"guess": "1234"}
        )

    assert guess_response.status_code == 200
    data = guess_response.json()
    assert "exact" in data
    assert "wrong_pos" in data
    assert data["attempts"] == 1
