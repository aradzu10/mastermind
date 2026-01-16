from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from backend.core.game_engine import MasterMindGame, GuessRecord
from backend.db.repositories.game_repository import GameRepository
from backend.db.models.game import Game


class GameService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = GameRepository(session)

    async def create_game(self, user_id: Optional[int] = None, game_mode: str = "single") -> Game:
        game_engine = MasterMindGame()

        game = await self.repo.create(
            user_id=user_id,
            secret=game_engine.secret,
            game_mode=game_mode,
            attempts=0,
            won=False,
            guesses=[]
        )
        return game

    async def get_game(self, game_id: int) -> Optional[Game]:
        return await self.repo.get(game_id)

    async def make_guess(self, game_id: int, guess_str: str) -> dict:
        game = await self.repo.get(game_id)
        if not game:
            raise ValueError("Game not found")

        if game.completed_at:
            raise ValueError("Game already completed")

        # Create game engine with the stored secret
        game_engine = MasterMindGame()
        game_engine.secret = game.secret
        game_engine.attempts = game.attempts

        # Validate and evaluate guess
        if not game_engine.validate_guess(guess_str):
            raise ValueError("Invalid guess format")

        exact, wrong_pos, is_winner = game_engine.make_guess(guess_str)

        # Update game state
        guesses_list = game.guesses or []
        guesses_list.append({
            "guess": guess_str,
            "exact": exact,
            "wrong_pos": wrong_pos
        })

        game.guesses = guesses_list
        game.attempts = game_engine.attempts

        # Complete game if won
        if is_winner:
            await self.repo.complete_game(game_id, won=True)

        await self.session.flush()
        await self.session.refresh(game)

        return {
            "game_id": game.id,
            "guess": guess_str,
            "exact": exact,
            "wrong_pos": wrong_pos,
            "is_winner": is_winner,
            "attempts": game.attempts,
            "game_over": is_winner or (game.completed_at is not None)
        }
