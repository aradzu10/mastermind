# backend/db/models/

SQLAlchemy ORM models for database tables.

## Purpose
Defines database schema using SQLAlchemy declarative models. Maps Python classes to PostgreSQL tables with relationships and constraints.

## Contents

### Files

- **game.py** - Game model for games table
- **user.py** - User model for users table
- **__init__.py** - Package initializer

### Classes in game.py

- **Game** - SQLAlchemy model for games table with columns and user relationship

### Columns in Game

- **id** - Integer primary key
- **user_id** - Foreign key to users (nullable)
- **secret** - String(4) secret code
- **attempts** - Integer guess count
- **won** - Boolean win status
- **game_mode** - String (single, ai_easy, ai_medium, ai_hard)
- **guesses** - JSON array of guess records
- **completed_at** - DateTime completion timestamp (nullable)
- **created_at** - DateTime creation timestamp

### Classes in user.py

- **User** - SQLAlchemy model for users table with columns and games relationship

### Columns in User

- **id** - Integer primary key
- **email** - String unique email (nullable)
- **google_id** - String unique Google OAuth ID (nullable)
- **display_name** - String user display name
- **is_guest** - Boolean guest status
- **elo_rating** - Float ELO rating (default 1200.0)
- **created_at** - DateTime creation timestamp

### Functions
None (SQLAlchemy uses declarative class syntax)
