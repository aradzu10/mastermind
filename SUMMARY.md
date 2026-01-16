# mastermind/

Full-stack Mastermind game web application.

## Purpose
Complete web-based Mastermind game with FastAPI backend, React frontend, PostgreSQL database, and original CLI version preserved. Supports single-player gameplay with plans for AI opponents and multiplayer.

## Contents

### Subdirectories

- **backend/** - FastAPI server with three-layer architecture (API → Service → Repository)
- **frontend/** - React + TypeScript + Vite + Tailwind CSS application
- **tests/** - pytest test suite (unit, integration, e2e)
- **alembic/** - Database migration management
- **legacy/** - Original CLI game (preserved and functional)
- **docker/** - Docker configuration files

### Files

- **README.md** - Project overview and getting started guide
- **CLAUDE.md** - Development guidelines and architecture documentation
- **PROGRESS.md** - Detailed project status and phase tracking
- **pyproject.toml** - Python project configuration (dependencies, pytest, black, ruff)
- **alembic.ini** - Alembic migration configuration
- **docker-compose.yml** - Multi-container Docker orchestration (postgres, backend, frontend)
- **.env.example** - Environment variables template
- **.gitignore** - Git ignore patterns

### Architecture

```
Frontend (React + Zustand)
  ↓ HTTP/REST
Backend (FastAPI)
  ├─ API Layer (routes/)
  ├─ Service Layer (services/)
  ├─ Repository Layer (repositories/)
  └─ Core Logic (game_engine.py - NEVER MODIFY)
  ↓
Database (PostgreSQL + Alembic)
```

### Key Technologies

- **Backend**: FastAPI, SQLAlchemy (async), Pydantic, PostgreSQL
- **Frontend**: React, TypeScript, Vite, Zustand, Tailwind CSS, Axios
- **Database**: PostgreSQL with async driver (asyncpg)
- **Testing**: pytest with async support
- **Deployment**: Docker + docker-compose

### Development Commands

Backend:
- `docker-compose up -d postgres` - Start PostgreSQL
- `source .venv/bin/activate` - Activate Python venv
- `uvicorn backend.main:app --reload` - Start backend dev server
- `alembic upgrade head` - Run database migrations
- `pytest` - Run tests

Frontend:
- `cd frontend && npm install` - Install dependencies
- `npm run dev` - Start dev server (http://localhost:5173)
- `npm run build` - Production build

Legacy:
- `cd legacy && python mastermind_ui.py` - Play CLI version

### Project Phases

- ✅ Phase 0: Setup & Migration
- ✅ Phase 1: Web Backend Foundation
- ✅ Phase 2: Frontend Basic Game
- ⏳ Phase 3: AI Engine (in progress)
- ⬜ Phase 4: Authentication
- ⬜ Phase 5: Real-Time Multiplayer
- ⬜ Phase 6: Ranking & Leaderboard
- ⬜ Phase 7: Docker & Deployment

### Functions
None (project root with configuration files)

### Classes
None
