# frontend/src/services/

API client services for backend communication.

## Purpose
Contains axios-based HTTP client for making API requests to the backend. Centralizes all backend communication logic.

## Contents

### Files

- **api.ts** - Axios HTTP client and API methods

### Constants in api.ts

- **API_BASE_URL** - Base URL for API requests (from VITE_API_URL env or localhost:8000)
- **api** - Configured axios instance with baseURL and JSON headers

### Objects in api.ts

- **gameApi** - Object containing all game-related API methods

### Functions in api.ts (gameApi methods)

- **createGame(gameMode = 'single')** - POST request to create a new game, returns Game
- **getGame(gameId)** - GET request to fetch game state by ID, returns Game
- **makeGuess(gameId, guess)** - POST request to submit a guess, returns GameGuessResponse

### Classes
None
