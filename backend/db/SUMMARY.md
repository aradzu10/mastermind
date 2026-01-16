# backend/db/

Database layer with async SQLAlchemy setup, models, and repositories.

## Purpose
Complete database layer implementing Repository pattern with async SQLAlchemy. Manages database connections, ORM models, and data access abstractions.

## Contents

### Subdirectories

- **models/** - SQLAlchemy ORM models (Game, User)
- **repositories/** - Repository pattern implementations for data access

### Files

- **database.py** - Async SQLAlchemy engine, session factory, and dependency injection
- **__init__.py** - Package initializer

### Constants in database.py

- **DATABASE_URL** - PostgreSQL connection string from environment (with asyncpg driver)
- **engine** - Async SQLAlchemy engine with echo=True for query logging
- **AsyncSessionLocal** - Async session factory for creating database sessions
- **Base** - Declarative base class for ORM models

### Functions in database.py

- **get_db()** - Async generator dependency that yields AsyncSession with transaction management (commit on success, rollback on error)

### Classes
None (uses factory functions and declarative base)
