from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from backend.core.game_engine import MasterMindGame, GuessRecord
from backend.db.repositories.game_repository import GameRepository
from backend.db.models.game import Game
from backend.core.ai import get_ai_player


class GameService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = GameRepository(session)

    async def create_game(
        self, 
        user_id: Optional[int] = None, 
        game_mode: str = "single",
        player_secret: Optional[str] = None
    ) -> Game:
        """
        Create a new game.
        
        Args:
            user_id: ID of the user creating the game
            game_mode: "single", "ai", or "pvp"
            player_secret: For AI mode, the secret code that the AI will try to guess
                          If None in AI mode, a random secret will be generated
        """
        game_engine = MasterMindGame()
        
        # Determine opponent type
        opponent_type = "none"
        if game_mode == "ai":
            opponent_type = "ai"
            # If player didn't provide a secret, generate one
            if not player_secret:
                player_secret = game_engine._generate_secret_number()
        elif game_mode == "pvp":
            opponent_type = "human"

        game = await self.repo.create(
            user_id=user_id,
            secret=game_engine.secret,  # The secret player is guessing
            player_secret=player_secret,  # The player's secret (for AI to guess)
            game_mode=game_mode,
            opponent_type=opponent_type,
            attempts=0,
            won=False,
            guesses=[],
            ai_guesses=[] if game_mode == "ai" else None
        )
        return game

    async def get_game(self, game_id: int) -> Optional[Game]:
        return await self.repo.get(game_id)

    async def make_guess(self, game_id: int, guess_str: str) -> dict:
        """Player makes a guess against the game's secret."""
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

        # Complete game if player won
        player_won = is_winner
        if player_won:
            await self.repo.complete_game(game_id, won=True)

        await self.session.flush()
        await self.session.refresh(game)

        # If AI mode and game not over, make AI move
        ai_result = None
        if game.game_mode == "ai" and not game.completed_at:
            ai_result = await self._make_ai_move(game)

        return {
            "game_id": game.id,
            "guess": guess_str,
            "exact": exact,
            "wrong_pos": wrong_pos,
            "is_winner": player_won,
            "attempts": game.attempts,
            "game_over": (game.completed_at is not None),
            "ai_move": ai_result
        }

    async def _make_ai_move(self, game: Game) -> dict:
        """Make an AI move against the player's secret."""
        if not game.player_secret:
            raise ValueError("No player secret set for AI game")

        # Get AI player
        ai_player = get_ai_player("random")
        
        # Restore AI state from previous guesses
        for guess_record in (game.ai_guesses or []):
            ai_player.record_guess(
                guess_record["guess"],
                guess_record["exact"],
                guess_record["wrong_pos"]
            )

        # Get AI's next guess
        ai_guess = ai_player.get_next_guess()

        # Evaluate AI's guess against player's secret
        game_engine = MasterMindGame()
        game_engine.secret = game.player_secret
        exact, wrong_pos = game_engine.evaluate_guess(ai_guess)
        ai_won = (exact == 4)

        # Update AI guesses
        ai_guesses_list = game.ai_guesses or []
        ai_guesses_list.append({
            "guess": ai_guess,
            "exact": exact,
            "wrong_pos": wrong_pos
        })
        game.ai_guesses = ai_guesses_list

        # If AI won, complete the game
        if ai_won:
            await self.repo.complete_game(game.id, won=False)  # Player lost

        await self.session.flush()
        await self.session.refresh(game)

        return {
            "ai_guess": ai_guess,
            "exact": exact,
            "wrong_pos": wrong_pos,
            "ai_won": ai_won
        }
