# alembic/versions/

Database migration version files.

## Purpose
Contains Alembic migration scripts that define database schema changes over time. Each file represents a versioned schema modification with upgrade and downgrade functions.

## Contents

### Files

- **7c2580e573cf_initial_migration_users_and_games_tables.py** - Initial migration creating users and games tables

### Functions in 7c2580e573cf_initial_migration_users_and_games_tables.py

- **upgrade()** - Creates users and games tables with columns, indexes, and foreign keys
- **downgrade()** - Drops games and users tables and their indexes

### Constants

- **revision** - Migration version ID '7c2580e573cf'
- **down_revision** - Previous migration (None for initial)
- **branch_labels** - Branch labels (None)
- **depends_on** - Dependencies (None)

### Classes
None (uses Alembic migration function format)
