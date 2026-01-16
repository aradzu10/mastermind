# alembic/

Alembic database migration management.

## Purpose
Database migration framework using Alembic. Manages schema versioning, tracks changes, and provides upgrade/downgrade capabilities for PostgreSQL database.

## Contents

### Subdirectories

- **versions/** - Migration version files with upgrade/downgrade functions

### Files

- **env.py** - Alembic environment configuration with model imports and migration functions
- **script.py.mako** - Template for generating new migration files
- **README** - Brief Alembic documentation

### Functions in env.py

- **run_migrations_offline()** - Runs migrations in offline mode (no database connection, SQL output only)
- **run_migrations_online()** - Runs migrations in online mode (with database connection)

### Constants in env.py

- **config** - Alembic Config object from alembic.ini
- **database_url** - Database URL from environment, converted from asyncpg to psycopg2 for Alembic compatibility
- **target_metadata** - Base.metadata from SQLAlchemy models for autogenerate support

### Classes
None (uses Alembic configuration and functions)
