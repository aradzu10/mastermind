# tests/integration/

Integration tests for API endpoints with full request/response cycle.

## Purpose
Tests FastAPI endpoints with real HTTP requests using AsyncClient. Validates API contracts, status codes, response formats, and database interactions.

## Contents

### Files

- **test_games_api.py** - Integration tests for game API endpoints

### Functions in test_games_api.py

- **test_health_check()** - Async test for GET /api/health endpoint (200 status, "ok" message)
- **test_root()** - Async test for GET / endpoint (200 status, version info)
- **test_create_game()** - Async test for POST /api/games/single endpoint (201 status, game creation)
- **test_make_guess()** - Async test for POST /api/games/{id}/guess endpoint (200 status, guess feedback)

### Classes
None
