# backend/schemas/

Pydantic models for request/response validation and serialization.

## Purpose
Defines data validation schemas using Pydantic. Validates incoming requests, serializes outgoing responses, and provides automatic API documentation.

## Contents

### Files

- **game.py** - Pydantic schemas for game-related API operations
- **__init__.py** - Package initializer

### Classes in game.py

- **GuessRecord** - Single guess with feedback (guess, exact, wrong_pos with validation)
- **GameCreate** - Request schema for creating a game (game_mode with pattern validation)
- **GameGuess** - Request schema for making a guess (4-digit string with pattern validation)
- **GameResponse** - Response schema for game state (all game fields with from_attributes config)
- **GameGuessResponse** - Response schema after making a guess (game_id, guess, feedback, winner status)

### Functions
None (Pydantic models use class-based definitions)
