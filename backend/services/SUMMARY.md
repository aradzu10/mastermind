# backend/services/

Business logic services that orchestrate operations between API and data layers.

## Purpose
Service layer that implements business logic, coordinates between repositories and core game logic, and manages transactions. Keeps route handlers thin and logic reusable.

## Contents

### Files

- **game_service.py** - Service for game creation and gameplay logic
- **__init__.py** - Package initializer

### Classes in game_service.py

- **GameService** - Orchestrates game operations (create, get, make_guess) using repositories and game engine

### Methods in GameService

- **__init__(session)** - Initializes service with AsyncSession and GameRepository
- **create_game(user_id, game_mode)** - Creates new game with generated secret, returns Game model
- **get_game(game_id)** - Retrieves game by ID, returns Game model or None
- **make_guess(game_id, guess_str)** - Validates guess, evaluates using game engine, updates database, returns dict with feedback

### Functions
None (all logic in class methods)
