# frontend/src/components/Game/

React components for game UI and interaction.

## Purpose
Contains all React components related to the game interface including the main game board, guess input, and guess history display.

## Contents

### Files

- **GameBoard.tsx** - Main game container component
- **GuessInput.tsx** - Controlled input component for entering guesses
- **GuessHistory.tsx** - Display component for past guesses with feedback

### Functions in GameBoard.tsx

- **GameBoard()** - Main component that orchestrates game flow, handles loading/error states, displays game UI
- **handleNewGame()** - Event handler that resets and creates a new game

### Functions in GuessInput.tsx

- **GuessInput()** - Component rendering 4-digit input field with submit button
- **handleSubmit(e)** - Form submit handler that makes a guess via store
- **handleChange(e)** - Input change handler that updates current guess in store

### Functions in GuessHistory.tsx

- **GuessHistory({ guesses })** - Component that displays list of previous guesses with feedback badges

### Classes
None (all functional components)
