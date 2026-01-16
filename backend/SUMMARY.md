# backend/

FastAPI backend with three-layer architecture (API → Service → Repository).

## Purpose
Complete backend API server implementing Repository pattern with async SQLAlchemy. Provides REST endpoints for game creation, gameplay, and future multiplayer features.

## Contents

### Subdirectories

- **api/** - FastAPI routes and WebSocket handlers
- **core/** - Pure game logic (MasterMindGame class, NEVER MODIFY)
- **db/** - Database layer (models, repositories, async SQLAlchemy)
- **schemas/** - Pydantic request/response validation models
- **services/** - Business logic orchestration layer

### Files

- **main.py** - FastAPI application initialization with CORS, routes, and health endpoints
- **CLAUDE.md** - Backend development guidelines
- **__init__.py** - Package initializer

### Functions in main.py

- **health_check()** - GET /api/health - Returns {"status": "ok"} health check
- **root()** - GET / - Returns API info with version and docs link

### Constants in main.py

- **app** - FastAPI application instance with title, description, version
- **origins** - CORS allowed origins from environment (default: localhost:3000,5173)

### Classes
None (uses FastAPI app instance and route decorators)
