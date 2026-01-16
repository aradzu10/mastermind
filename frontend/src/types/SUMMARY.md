# frontend/src/types/

TypeScript type definitions for frontend data structures.

## Purpose
Contains TypeScript interfaces that define the shape of data used throughout the frontend application. Ensures type safety and provides IDE autocompletion.

## Contents

### Files

- **game.ts** - Type definitions for game-related data structures

### Interfaces in game.ts

- **GuessRecord** - Represents a single guess with feedback (guess: string, exact: number, wrong_pos: number)
- **Game** - Complete game state (id, attempts, won, game_mode, guesses, completed_at, created_at)
- **GameGuessResponse** - Server response after making a guess (game_id, guess, exact, wrong_pos, is_winner, attempts, game_over)

### Functions
None

### Classes
None
