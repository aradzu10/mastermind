# backend/api/routes/

FastAPI route handlers for REST endpoints.

## Purpose
Thin route handlers that validate requests, call service layer, and return responses. Implements REST API endpoints with automatic OpenAPI documentation.

## Contents

### Files

- **games.py** - Game-related API endpoints
- **__init__.py** - Package initializer

### Constants in games.py

- **router** - FastAPI APIRouter with /api/games prefix and "games" tag

### Functions in games.py

- **create_single_player_game(game_data, db)** - POST /api/games/single - Creates new game, returns GameResponse (201)
- **get_game(game_id, db)** - GET /api/games/{game_id} - Retrieves game state, returns GameResponse or 404
- **make_guess(game_id, guess_data, db)** - POST /api/games/{game_id}/guess - Submits guess, returns GameGuessResponse or 400

### Classes
None (uses FastAPI route decorators)
