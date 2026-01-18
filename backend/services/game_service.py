import dataclasses
import random
from typing import Literal, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.ai import get_ai_player
from backend.core.game_engine import GuessRecord, MasterMindGame
from backend.db.models.game import Game, PlayerState
from backend.db.models.user import User
from backend.db.repositories.game_repository import GameRepository, PvPGameRepository, SingleGameRepository
from backend.db.repositories.user_repository import UserRepository


class GameService:
    def __init__(self, session: AsyncSession):
        self.single_repo = SingleGameRepository(session)
        self.game_repo = GameRepository(session)
        self.pvp_repo = PvPGameRepository(session)
        self.user_repo = UserRepository(session)

    def _create_player(self, user: User | None, secret: str) -> PlayerState:
        if user is None:
            user = User(id=None, display_name=None, elo_rating=None)
        return PlayerState(
            id=user.id,  # type: ignore
            name=user.display_name,  # type: ignore
            secret=secret,
            guesses=[],
            elo=user.elo_rating,  # type: ignore
        )

    def _apply_free_guess(self, player: PlayerState) -> PlayerState:
        mastermind = MasterMindGame(player_secret=player.secret)
        mastermind.apply_free_guess()
        free_guess = mastermind.history[0]
        player.guesses += [{"guess": free_guess.guess, "exact": free_guess.exact, "wrong_pos": free_guess.wrong_pos}]
        return player

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
        player = self._create_player(user, game_engine.secret)
        return await self.single_repo.create(player)

    async def _create_or_join_pvp_game(self, user: User, player_secret: str | None) -> Game:
        game_engine = MasterMindGame(player_secret)
        available_game = await self.pvp_repo.get_waiting_game()
        if available_game:
            # Join existing game - player1 gets the joining user's secret, player2 is the new player
            player1 = PlayerState(**dataclasses.asdict(available_game.player1))
            player1.secret = game_engine.secret
            player2 = self._create_player(user, available_game.player2.secret)

            current_turn = random.choice([player1.id, player2.id])

            if current_turn == player1.id:
                player2 = self._apply_free_guess(player2)
            else:
                player1 = self._apply_free_guess(player1)
            return await self.pvp_repo.join_game(available_game, player1, player2, current_turn)

        # Create new waiting game
        player1 = self._create_player(user, secret="")
        player2 = self._create_player(None, secret=game_engine.secret)
        return await self.pvp_repo.create(player1, player2)

    async def _create_ai_game(self, user: User, ai_difficulty: str, player_secret: str | None) -> Game:
        player_game = MasterMindGame()
        ai_game = MasterMindGame(player_secret)
        ai_player = get_ai_player(ai_difficulty, ai_game)
        ai_user = ai_player.user()

        player1 = self._create_player(user, player_game.secret)
        player2 = self._create_player(ai_user, ai_game.secret)

        current_turn = random.choice([player1.id, player2.id])

        if current_turn == player1.id:
            player2 = self._apply_free_guess(player2)
        else:
            player1 = self._apply_free_guess(player1)

        return await self.pvp_repo.create_ai_game(player1, player2, ai_difficulty, current_turn)

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

        # For PvP games, validate it's the player's turn
        if game.game_mode == "pvp":
            if game.current_turn != user.id:
                raise ValueError("It's not your turn")

        if game.game_mode == "single":
            player = PlayerState(**dataclasses.asdict(game.player))
            opponent = self._create_player(None, secret=None)
            repo = self.single_repo
        elif game.player1.id == user.id:
            player = PlayerState(**dataclasses.asdict(game.player1))
            opponent = PlayerState(**dataclasses.asdict(game.player2))
            repo = self.pvp_repo
        else:
            player = PlayerState(**dataclasses.asdict(game.player2))
            opponent = PlayerState(**dataclasses.asdict(game.player1))
            repo = self.pvp_repo

        history = [GuessRecord(**guess) for guess in player.guesses or []]
        mastermind = MasterMindGame(player_secret=player.secret, history=history)

        if not mastermind.validate_guess(guess_str):
            raise ValueError("Invalid guess format")

        exact, wrong_pos, is_winner = mastermind.make_guess(guess_str)
        player.guesses.append({"guess": guess_str, "exact": exact, "wrong_pos": wrong_pos})
        winner_id = player.id if is_winner else None
        if game.game_mode != "single" and game.player2.id == user.id:
            player, opponent = opponent, player
        game = await repo.make_guess(game, player, opponent, winner_id)

        return game

    async def get_opponent_guess(self, game_id: int, user: User) -> Game:
        game = await self.get_game(game_id, user)
        if game.game_mode == "single":
            raise ValueError("No opponent in single player game")

        # For PvP, just return current state (opponent makes moves via /guess endpoint)
        if game.game_mode == "pvp":
            return game

        # For AI, generate AI's next guess
        if game.game_mode == "ai":
            history = [GuessRecord(**guess) for guess in game.player2.guesses or []]
            mastermind = MasterMindGame(player_secret=game.player2.secret, history=history)
            ai_player = get_ai_player(game.ai_difficulty, mastermind)

            ai_guess = ai_player.get_next_guess()
            exact, wrong_pos, is_winner = mastermind.make_guess(ai_guess)
            ai_player_state = PlayerState(**dataclasses.asdict(game.player2))
            ai_player_state.guesses.append({"guess": ai_guess, "exact": exact, "wrong_pos": wrong_pos})
            winner_id = ai_player_state.id if is_winner else None
            return await self.pvp_repo.make_guess(game, game.player1, ai_player_state, winner_id)

        raise ValueError(f"Unknown game mode: {game.game_mode}")

    async def abandon_game(self, game_id: int, user: User) -> Game:
        game = await self.get_game(game_id, user)

        if game.status != "in_progress":
            raise ValueError("Can only abandon games that are in progress")
        if game.game_mode == "single":
            raise ValueError("Cannot abandon single player games")

        game = await self.pvp_repo.abandon_game(game, user)
        return game

    async def abandon_all_active_games(self, user: User) -> None:
        active_games = await self.pvp_repo.get_active_pvp_games(user.id)
        for game in active_games:
            try:
                game = await self.pvp_repo.abandon_game(game, user)
            except Exception:
                # Continue abandoning other games even if one fails
                pass
