from typing import Literal, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.ai import get_ai_player
from backend.core.game_engine import GuessRecord, MasterMindGame
from backend.db.models.game import Game
from backend.db.models.user import User
from backend.db.repositories.game_repository import GameRepository, PvPGameRepository, SingleGameRepository
from backend.db.repositories.user_repository import UserRepository


class GameService:
    def __init__(self, session: AsyncSession):
        self.single_repo = SingleGameRepository(session)
        self.game_repo = GameRepository(session)
        self.pvp_repo = PvPGameRepository(session)
        self.user_repo = UserRepository(session)

    async def create_game(
        self,
        user: User,
        game_mode: Literal["single", "ai", "pvp"],
        player_secret: Optional[str] = None,
        ai_difficulty: str | None = None,
    ) -> Game:
        if game_mode == "single":
            game = await self._create_single_game(user)
        elif game_mode == "pvp":
            game = await self._create_or_join_pvp_game(user, player_secret)
        elif game_mode == "ai":
            game = await self._create_ai_game(user, ai_difficulty, player_secret)
        else:
            raise ValueError("Invalid game mode")

        return game

    async def _create_single_game(self, user: User) -> Game:
        game_engine = MasterMindGame()
        return await self.single_repo.create(user, game_engine.secret)

    async def _create_or_join_pvp_game(self, user: User, player_secret: str | None) -> Game:
        game_engine = MasterMindGame(player_secret)
        available_game = await self.pvp_repo.get_waiting_games()
        if available_game:
            # Join existing game
            game = await self.pvp_repo.join_game(available_game[0], user, game_engine.secret)
            return game
        return await self.pvp_repo.create(user, game_engine.secret)

    async def _create_ai_game(self, user: User, ai_difficulty: str, player_secret: str | None) -> Game:
        player_game = MasterMindGame()
        ai_game = MasterMindGame(player_secret)
        ai_player = get_ai_player(ai_difficulty, ai_game)
        return await self.pvp_repo.create_ai_game(
            user,
            player_game.secret,
            ai_player.master_mind_game.secret,
            ai_name=ai_player.name,
            ai_difficulty=ai_difficulty,
        )

    async def get_game(self, game_id: int, user: User) -> Game:
        game = await self.game_repo.find_by_id(game_id)
        if not game:
            raise ValueError("Game not found")
        if game.game_mode == "single":
            if game.player.id != user.id:
                raise ValueError("Game not found")
        if game.game_mode in ("pvp", "ai"):
            if game.player1.id != user.id and game.player2.id != user.id:
                raise ValueError("Game not found")
        return game

    async def make_guess(self, game_id: int, guess_str: str, user: User) -> Game:
        game = await self.get_game(game_id, user)

        if game.completed_at is not None:
            raise ValueError("Game is already completed")

        if game.game_mode == "single":
            player = game.player
            repo = self.single_repo
        elif game.player1.id == user.id:
            player = game.player1
            repo = self.pvp_repo
        else:
            player = game.player2
            repo = self.pvp_repo

        history = [GuessRecord(**guess) for guess in player.guesses or []]
        mastermind = MasterMindGame(player_secret=player.secret, history=history)

        if not mastermind.validate_guess(guess_str):
            raise ValueError("Invalid guess format")

        exact, wrong_pos, is_winner = mastermind.make_guess(guess_str)
        game = await repo.make_guess(game, user, guess_str, exact, wrong_pos, is_winner)
        return game

    async def get_opponent_guess(self, game_id: int, user: User) -> Game:
        game = await self.get_game(game_id, user)
        if game.game_mode == "single":
            raise ValueError("No opponent in single player game")

        if game.game_mode != "ai":
            raise ValueError("PvP not implemented")

        history = [GuessRecord(**guess) for guess in game.player2.guesses or []]
        mastermind = MasterMindGame(player_secret=game.player2.secret, history=history)
        ai_player = get_ai_player(game.ai_difficulty, mastermind)

        ai_guess = ai_player.get_next_guess()
        exact, wrong_pos, is_winner = mastermind.make_guess(ai_guess)
        return await self.pvp_repo.make_guess(game, game.player2, ai_guess, exact, wrong_pos, is_winner)
