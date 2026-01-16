# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Full-stack Mastermind game web application with:
- **Backend**: FastAPI + PostgreSQL + SQLAlchemy (async)
- **Frontend**: React + TypeScript + Vite + Tailwind CSS
- **Legacy**: Original CLI game preserved in `legacy/`

## Commands

### Backend Development
```bash
# Start backend only (requires Docker)
docker-compose up -d postgres
source .venv/bin/activate
uvicorn backend.main:app --reload

# Start full Docker stack
docker-compose up -d

# Run database migrations
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "description"

# Run backend tests
pytest tests/

# Run specific test
pytest tests/unit/test_mastermind_logic.py::test_evaluate_guess
```

### Frontend Development
```bash
cd frontend
npm install
npm run dev          # Dev server at http://localhost:5173
npm run build        # Production build
npm run lint         # ESLint
npm run preview      # Preview production build
```

### Legacy CLI
```bash
cd legacy
python mastermind_ui.py
```

## Architecture

### Three-Layer Backend
```
API Layer (FastAPI)
  ↓
Service Layer (Business Logic)
  ↓
Repository Layer (Data Access)
  ↓
Database (PostgreSQL)
```

**Key Principle**: Core game logic (`MasterMindGame` class) preserved from CLI version, never modified.

### Backend Structure
- `backend/core/` - Pure logic, no I/O (game_engine.py contains original MasterMindGame)
- `backend/db/models/` - SQLAlchemy models (User, Game)
- `backend/db/repositories/` - Repository pattern for data access
- `backend/services/` - Business logic orchestration
- `backend/api/routes/` - FastAPI REST endpoints
- `backend/schemas/` - Pydantic request/response models

### Frontend Structure
- `frontend/src/components/Game/` - Game UI components (GameBoard, GuessInput, GuessHistory)
- `frontend/src/store/` - Zustand state management
- `frontend/src/services/` - API client (axios)
- `frontend/src/types/` - TypeScript type definitions

### Legacy CLI (still functional)
- `legacy/mastermind_logic.py` - Core game engine
- `legacy/mastermind_ui.py` - CLI interface
- `legacy/database.py` - JSON file persistence

Data flows: UI → Logic → Database. Logic is pure and testable independently.

## API Endpoints

```
GET  /                     - API information
GET  /api/health           - Health check
POST /api/games/single     - Create single-player game
GET  /api/games/{id}       - Get game state
POST /api/games/{id}/guess - Submit guess and get feedback
GET  /docs                 - Swagger UI (auto-generated)
```

## Database

PostgreSQL with async SQLAlchemy:
- `users` table: id, email, google_id, display_name, is_guest, elo_rating
- `games` table: id, user_id, secret, attempts, won, game_mode, guesses (JSONB)

## Development Workflow

1. **Database changes**: Create Alembic migration → Run `alembic upgrade head`
2. **Backend changes**: Edit code → Tests pass → FastAPI auto-reloads
3. **Frontend changes**: Edit code → Vite hot-reloads → Verify in browser
4. **API proxy**: Vite proxies `/api/*` to `http://localhost:8000` (configured in vite.config.ts)

## Project Phases

See PROGRESS.md for detailed status. Current phases:
- ✅ Phase 0: Setup & Migration
- ✅ Phase 1: Web Backend Foundation
- ✅ Phase 2: Frontend Basic Game
- ⏳ Phase 3: AI Engine (RandomAI, HeuristicAI, MinimaxAI)
- ⬜ Phase 4: Authentication (Google OAuth + guest mode)
- ⬜ Phase 5: Real-Time Multiplayer (WebSockets + cheat detection)
- ⬜ Phase 6: Ranking & Leaderboard (ELO system)
- ⬜ Phase 7: Docker & Deployment

## Interaction

- Be short. Especially when running bash commands or testing.
- No fluff. No politeness. No "I understand."
- Technical accuracy first. Check work twice.
- No apologies. Fix mistakes directly.
- State uncertainty explicitly.
- Provide code and terminal output. Minimize prose.

## Coding Style

- Simple, clear, readable code.
- Documentation only when complexity demands it.
- Guard clauses and flat logic over deep nesting.
- Highly descriptive names for self-documenting code.
- Standard library first, external dependencies last.
- Small functions, single responsibility.
- Consistent naming conventions.
- Fix root causes, not symptoms.
