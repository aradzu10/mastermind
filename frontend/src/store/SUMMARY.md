# frontend/src/store/

Zustand state management store for global application state.

## Purpose
Centralized state management using Zustand. Manages game state, loading states, errors, and provides actions for creating games and making guesses.

## Contents

### Files

- **gameStore.ts** - Zustand store for game state and actions

### Interfaces in gameStore.ts

- **GameState** - Store state interface (game, loading, error, currentGuess, setCurrentGuess, createGame, makeGuess, resetGame)

### Functions in gameStore.ts

- **useGameStore** - Zustand hook that creates and exports the game store with state and actions

### Store Actions (within useGameStore)

- **setCurrentGuess(guess: string)** - Updates current input guess with validation (4 digits max, digits only)
- **createGame()** - Async action that creates a new game via API and updates store
- **makeGuess(guess: string)** - Async action that submits guess, receives feedback, and updates game state
- **resetGame()** - Clears game state to allow starting a new game

### Classes
None
