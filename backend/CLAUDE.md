# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Backend Architecture

FastAPI backend using Repository Pattern with async SQLAlchemy.

```
FastAPI Routes (api/routes/)
  ↓
Service Layer (services/) - Business logic orchestration
  ↓
Repository Layer (db/repositories/) - Data access abstraction
  ↓
SQLAlchemy Models (db/models/)
  ↓
PostgreSQL
```

## Commands

```bash
# From project root, activate venv
source .venv/bin/activate

# Start backend (requires Docker postgres)
docker-compose up -d postgres
uvicorn backend.main:app --reload

# Access API docs
open http://localhost:8000/docs

# Run database migrations
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "add_field_to_model"

# Run tests
pytest tests/unit/
pytest tests/integration/
```

## Directory Structure

- `core/` - Pure game logic (no I/O, no database)
  - `game_engine.py` - Original MasterMindGame class (NEVER MODIFY)
- `db/` - Database layer
  - `database.py` - Async SQLAlchemy setup
  - `models/` - SQLAlchemy ORM models
  - `repositories/` - Repository pattern implementations
- `services/` - Business logic
  - `game_service.py` - Orchestrates game creation, guesses, state management
- `api/routes/` - FastAPI endpoints
  - `games.py` - Game-related routes
- `schemas/` - Pydantic models for request/response validation
  - `game.py` - GameCreate, GameGuess, GameResponse, etc.
- `main.py` - FastAPI app initialization

## Key Design Patterns

### Repository Pattern
Abstracts data access. All database operations go through repositories.

```python
# DON'T: Direct model access
game = await session.query(Game).filter_by(id=game_id).first()

# DO: Use repository
game = await game_repository.get_by_id(game_id)
```

### Service Layer
Business logic lives in services, not routes or repositories.

```python
# Routes are thin - they call services
@router.post("/api/games/single")
async def create_game(db: AsyncSession = Depends(get_db)):
    return await game_service.create_single_player_game(db)

# Services orchestrate logic
async def create_single_player_game(db: AsyncSession):
    secret = MasterMindGame.generate_secret()
    game = await game_repository.create(db, secret=secret, ...)
    return game
```

### Core Logic Isolation
`backend/core/game_engine.py` contains the original `MasterMindGame` class. This file is NEVER modified - it's the preserved CLI game logic. All new features wrap around it.

## Database Models

### User
- id (UUID, primary key)
- email, google_id (nullable, for OAuth)
- display_name
- is_guest (boolean)
- elo_rating (integer, default 1200)
- created_at

### Game
- id (UUID, primary key)
- user_id (FK to User, nullable for now)
- secret (string, 4 digits)
- attempts (integer)
- won (boolean)
- game_mode (string: "single", "ai_easy", "ai_medium", "ai_hard")
- guesses (JSONB array: [{guess, exact, wrong_pos}])
- created_at, completed_at

## API Request Flow

Example: Making a guess

1. `POST /api/games/{id}/guess` with body `{"guess": "1234"}`
2. Route handler in `api/routes/games.py` validates request
3. Calls `game_service.make_guess(db, game_id, guess)`
4. Service:
   - Fetches game via `game_repository.get_by_id()`
   - Uses `MasterMindGame.evaluate_guess()` to calculate feedback
   - Updates game state via `game_repository.update()`
5. Returns Pydantic response schema
6. FastAPI serializes to JSON

## Testing

- Unit tests: Test services and core logic in isolation
- Integration tests: Test API endpoints with test database
- Use pytest fixtures for database sessions
- Mock external dependencies

## Adding New Features

### New API Endpoint
1. Create Pydantic schemas in `schemas/`
2. Add business logic in `services/`
3. Add route in `api/routes/`
4. Add integration test in `tests/integration/`

### New Database Model
1. Create model in `db/models/`
2. Create repository in `db/repositories/`
3. Create Alembic migration
4. Add service layer methods
5. Update schemas and routes
6. Add tests

## Environment Variables

Required (set in docker-compose.yml or .env):
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - For JWT signing (future auth)
- `ENVIRONMENT` - "development" or "production"

## CORS Configuration

Configured in `main.py`:
- Defaults: `http://localhost:3000,http://localhost:5173`
- Override with `CORS_ORIGINS` environment variable

## Important Notes

- All database operations are async (use `await`)
- Use dependency injection for database sessions (`Depends(get_db)`)
- Pydantic validates all input/output automatically
- FastAPI generates OpenAPI docs automatically at `/docs`
- Never modify `core/game_engine.py` - it's the preserved original logic
