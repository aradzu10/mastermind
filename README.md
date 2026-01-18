# Mastermind

A web-based implementation of the classic code-breaking game.

## What You Can Do

**Three game modes:**
- **Single Player** - Break the computer's secret code at your own pace
- **AI Opponent** - Race against a bot to see who cracks the code first
- **Player vs Player** - Real-time matchmaking against other players

**AI opponents** come in two flavors:
- **Brad** (ELO 200) - Makes random guesses
- **AradzBot** (ELO 2000) - Uses constraint-solving to systematically eliminate possibilities

**No signup required.** Play as a guest with just a display name. Your ELO rating updates after each competitive game (AI or PvP). Win against harder opponents to climb faster.

## Screenshots

**Game Selection**

<img src="images/game_start.gif" alt="AI Game Selection" height="300"/>


**Active Game**

<img src="images/pvp.gif" alt="Active Game" height="300"/>


## How It Works

Frontend uses React with TypeScript, styled with Tailwind CSS. State management through Zustand, with Framer Motion for animations.

Backend is FastAPI with a Service-Repository-Model pattern. Services handle game logic and AI opponents, repositories manage database access, and SQLAlchemy models define the schema. PostgreSQL stores users, games, and ELO ratings.

The app runs in Docker containers: PostgreSQL, FastAPI backend, and Nginx serving the React frontend.

## Running It

**Production:**
```bash
docker-compose up -d
```
Access at `http://localhost`

**Development:**
```bash
./dev.sh
```
The dev script handles everything: starts PostgreSQL in Docker, runs migrations, seeds AI users, launches the FastAPI backend (port 8000) and Vite dev server (port 5173).

Access at `http://localhost:5173`

# Final Project

For the final project, the game was expanded in several ways:
1. ✓ Create a Web version for playing the game.
2. ✓ Play against AI - multiple hardness levels.
3. ✓ Allow multiplayer game - 1 vs 1.
4. ✓ Add Users and Ranking.
5. ✓ Dockerize everything.

## Final Project: Enhanced Game Features

This project transitions the game from a local prototype to a full-featured web application.

### ✓ 1. Web Deployment

Porting the game engine to a web-compatible framework for browser accessibility.

### ✓ 2. Adaptive AI

Development of an AI engine with three difficulty tiers:

* **Easy:** Random moves.
* **Hard:** Constraint-solving for deep strategy.

### ✓ 3. Real-Time Multiplayer

Enable 1v1 remote play. This includes server-side state validation to prevent cheating and a lobby system for matchmaking.

### ✓ 4. User System & Ranking

A backend infrastructure to manage the competitive ecosystem:

* **Logging as guest** Without keeping score.
* **Database:** Persistent storage for profiles and match history.
* **Ranking:** A global Leaderboard based on an ELO ranking system.

### ✓ 5. Dockerize everything

Make everything in container.