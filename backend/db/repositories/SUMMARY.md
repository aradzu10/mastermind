# backend/db/repositories/

Repository pattern implementations for data access abstraction.

## Purpose
Abstracts database operations using Repository pattern. Provides clean interface for CRUD operations and custom queries without exposing SQLAlchemy details to services.

## Contents

### Files

- **base.py** - Generic base repository with common CRUD operations
- **game_repository.py** - Game-specific repository with custom queries
- **user_repository.py** - User-specific repository with lookup methods
- **__init__.py** - Package initializer

### Classes in base.py

- **BaseRepository[ModelType]** - Generic repository with CRUD operations for any SQLAlchemy model

### Methods in BaseRepository

- **__init__(model, session)** - Initializes with model class and async session
- **create(**kwargs)** - Creates new instance, flushes, refreshes, returns model
- **get(id)** - Retrieves model by ID, returns model or None
- **get_all(limit, offset)** - Retrieves all models with pagination, returns list
- **update(id, **kwargs)** - Updates model by ID, returns updated model or None
- **delete(id)** - Deletes model by ID, returns bool success

### Classes in game_repository.py

- **GameRepository** - Extends BaseRepository with game-specific queries

### Methods in GameRepository

- **__init__(session)** - Initializes with Game model
- **get_by_user_id(user_id, limit)** - Gets games for user, ordered by created_at desc
- **get_active_games(user_id)** - Gets incomplete games for user
- **complete_game(game_id, won)** - Marks game as complete with timestamp

### Classes in user_repository.py

- **UserRepository** - Extends BaseRepository with user-specific queries

### Methods in UserRepository

- **__init__(session)** - Initializes with User model
- **get_by_email(email)** - Finds user by email, returns User or None
- **get_by_google_id(google_id)** - Finds user by Google OAuth ID, returns User or None

### Functions
None (all logic in class methods)
