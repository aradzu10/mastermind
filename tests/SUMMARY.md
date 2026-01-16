# tests/

Test suite for the Mastermind backend using pytest.

## Purpose
Contains all test files organized by testing level (unit, integration, e2e). Uses pytest with async support and shared fixtures for database cleanup.

## Contents

### Subdirectories

- **unit/** - Unit tests for pure logic (no I/O, no database)
- **integration/** - API endpoint tests with real HTTP requests
- **e2e/** - End-to-end browser tests (planned, currently empty)

### Files

- **conftest.py** - Shared pytest fixtures and configuration
- **CLAUDE.md** - Testing guidelines and documentation

### Functions in conftest.py

- **cleanup_db()** - Async pytest fixture that auto-runs after each test to dispose database connections and prevent event loop conflicts

### Classes
None
