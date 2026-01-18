# Master Mind Game

A simple implementation of the Master Mind board game in Python.

## How to Play

The computer thinks of a 4-digit number (duplicates allowed).
You try to guess it and receive feedback:

- `+` = correct digit in correct position
- `~` = correct digit in wrong position
- `-` means no correct digits

Try to guess the number in as few attempts as possible!

## Example

```
Computer thinks: 5567 (hidden)

Your guess: 1234
Feedback: -        (Nothing match)

Your guess: 4589
Feedback: +        (5 is correct position)

Your guess: 5678
Feedback: +~~      (5 correct position, 6 and 7 wrong positions)
```

## Winning

```bash
Attempt #8
Enter your guess (4 digits): 6521
------------------------------
0123    +~
4567    +~
6701    ++
2244    ~
3344    -
2015    ~~~
2156    ~~~~
6521    ++++
------------------------------
Enter your name: aradz

🎉 You won! The number was 6521
You guessed it in 8 attempts!
🏆 NEW HIGH SCORE! 🏆
```

## Running the Game

```bash
python mastermind.py
```

# Final Project

For the final project, I will expand it in several ways.
1. Create a Web version for playing the game.
2. Play against AI - multiple hardnest levels.
3. Allow multiplayer game - 1 vs 1.
4. Add Users and Ranking.

## Final Project: Enhanced Game Features

This project transitions the game from a local prototype to a full-featured web application.


### 1. Web Deployment

Porting the game engine to a web-compatible framework for browser accessibility.

### 2. Adaptive AI

Development of an AI engine with three difficulty tiers:

* **Easy:** Random moves.
* **Medium:** Heuristic-based tactics.
* **Hard:** Minimax algorithm for deep strategic play.

### 3. Real-Time Multiplayer

Integration of **WebSockets** to enable 1v1 remote play. This includes server-side state validation to prevent cheating and a lobby system for matchmaking.

The design should be, that once the player got connected, the server don't need to know them until the finish with the game.
Then it will check for cheating, and if someone cheat, it automatically looses.

### 4. User System & Ranking

A backend infrastructure to manage the competitive ecosystem:

* **Logging as guest** Without keeping score.
* **Database:** Persistent storage for profiles and match history.
* **Ranking:** A global Leaderboard based on an ELO ranking system.

### 5. Dockerize everything

Make everything dockerize, that I could just run my docker and get a real website. Including the databases.
Still allow for local testing.