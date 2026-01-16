# legacy/

Original CLI-based Mastermind game (preserved and functional).

## Purpose
Contains the original command-line version of Mastermind game. Preserved as-is for reference and backward compatibility. Still fully functional and can be played independently.

## Contents

### Files

- **mastermind_logic.py** - Core game logic (identical to backend/core/game_engine.py)
- **mastermind_ui.py** - CLI user interface with terminal-based gameplay
- **database.py** - JSON file-based database for storing scores
- **test_database.py** - Tests for database functionality

### Classes in mastermind_logic.py

- **GuessRecord** - Dataclass for guess records (guess, exact, wrong_pos)
- **MasterMindGame** - Core game logic class (same as backend version)

### Classes in database.py

- **ScoreRecord** - Dataclass for score records (player_name, guesses, secret, timestamp)
- **ScoreRepository** - JSON file-based repository for reading/writing scores
- **GameRecordManager** - High-level manager for recording and retrieving high scores

### Functions in mastermind_ui.py

- **print_welcome_message(score_manager)** - Displays welcome banner and high score
- **create_feedback(exact, wrong_pos)** - Creates feedback string with symbols (+, ~, -)
- **print_history(history)** - Displays guess history table
- **print_win_message(secret, attempts, is_new_high_score)** - Displays win message with optional high score celebration
- **play_game()** - Main game loop handling input, validation, and gameplay
- **main()** - Entry point with play again loop

### Methods in ScoreRepository

- **_load_data()** - Loads JSON data from file
- **_save_data(data)** - Saves data to JSON file
- **get_scores()** - Returns list of ScoreRecord objects
- **save_score(record)** - Adds new score and returns updated list

### Methods in GameRecordManager

- **__init__(file_path)** - Initializes with ScoreRepository
- **record_score(player_name, guesses, secret)** - Records score and returns if it's a new high score
- **get_high_score()** - Returns ScoreRecord with minimum guesses or None
