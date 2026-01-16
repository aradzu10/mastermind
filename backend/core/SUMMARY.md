# backend/core/

Pure game logic with no I/O dependencies.

## Purpose
Contains the core game engine logic preserved from the original CLI version. This code is NEVER modified - it's the canonical Mastermind game implementation that all other layers wrap around.

## Contents

### Files

- **game_engine.py** - Core MasterMindGame class (preserved from CLI version, NEVER MODIFY)
- **__init__.py** - Package initializer

### Classes in game_engine.py

- **GuessRecord** - Dataclass representing a single guess (guess, exact, wrong_pos)
- **MasterMindGame** - Core game logic class for Mastermind gameplay

### Methods in MasterMindGame

- **__init__()** - Initializes game with attempts=0, num_digits=4, generates secret, empty history
- **_generate_secret_number()** - Generates random 4-digit secret code
- **validate_guess(guess)** - Validates guess is 4 digits, returns bool
- **evaluate_guess(guess)** - Calculates exact matches and wrong position matches, returns (exact, wrong_pos) tuple
- **make_guess(guess)** - Increments attempts, evaluates guess, updates history, returns (exact, wrong_pos, is_winner) tuple

### Functions
None (all logic in classes)
