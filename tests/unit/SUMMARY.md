# tests/unit/

Unit tests for core game logic in isolation.

## Purpose
Contains unit tests that test individual functions and classes without database or API dependencies. Tests are fast and focused on pure logic validation.

## Contents

### Files

- **test_mastermind_logic.py** - Unit tests for core MasterMindGame class logic

### Functions in test_mastermind_logic.py

- **test_evaluate_guess()** - Tests feedback calculation for various guess scenarios (all exact, partial matches, no matches, all wrong positions)
- **test_duplicates()** - Tests handling of duplicate digits in both secret and guess
- **test_validation()** - Tests input validation (correct length, digits only, empty string)

### Classes
None
