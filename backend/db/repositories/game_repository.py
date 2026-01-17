from datetime import datetime
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectin_polymorphic

from backend.db.models.game import Game, PlayerState, PvPGame, SingleGame
from backend.db.models.user import User
from backend.db.repositories.base import BaseRepository
from backend.schemas import game


class GameRepository(BaseRepository[Game]):
    def __init__(self, session: AsyncSession):
        super().__init__(Game, session)

    async def find_by_id(self, game_id: int) -> Game:
        result = await self.session.execute(
            select(Game)
            .where(Game.id == game_id)  #
            .options(selectin_polymorphic(Game, [SingleGame, PvPGame]))
        )
        return result.scalar_one_or_none()


class SingleGameRepository(BaseRepository[SingleGame]):
    def __init__(self, session: AsyncSession):
        super().__init__(SingleGame, session)

    async def create(self, user: User, secret: str) -> SingleGame:  # type: ignore
        player = PlayerState(
            id=user.id,  # type: ignore
            name=user.display_name,  # type: ignore
            secret=secret,
            guesses=[],
            elo=user.elo_rating,  # type: ignore
        )
        return await super().create(
            player=player,
            game_mode="single",
            status="in_progress",
            started_at=datetime.utcnow(),
        )

    async def get_by_user_id(self, user_id: int, limit: int = 10) -> List[SingleGame]:
        result = await self.session.execute(
            select(SingleGame)
            .where(SingleGame.player.id == user_id)
            .order_by(SingleGame.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_active_games(self, user_id: int) -> List[SingleGame]:
        result = await self.session.execute(
            select(SingleGame)
            .where(SingleGame.player.id == user_id, SingleGame.completed_at == None)
            .order_by(SingleGame.created_at.desc())
        )
        return list(result.scalars().all())

    async def make_guess(
        self,
        game: SingleGame,
        user: User,
        guess: str,
        exact: int,
        wrong_pos: int,
        is_winner: bool,
    ) -> SingleGame:
        curr_guess = [{"guess": guess, "exact": exact, "wrong_pos": wrong_pos}]
        player = PlayerState(
            id=game.player.id,
            name=game.player.name,
            secret=game.player.secret,
            guesses=game.player.guesses + curr_guess,
            elo=game.player.elo,
        )
        game.player = player
        if is_winner:
            game.winner_id = game.player.id  # type: ignore
            game.status = "completed"  # type: ignore
            game.completed_at = datetime.utcnow()  # type: ignore
        await self.session.flush()
        await self.session.refresh(game)
        return game


class PvPGameRepository(BaseRepository[PvPGame]):
    def __init__(self, session: AsyncSession):
        super().__init__(PvPGame, session)

    async def create(self, user: User, secret: str) -> PvPGame:  # type: ignore
        player1 = PlayerState(
            id=user.id,  # type: ignore
            name=user.display_name,  # type: ignore
            secret="",
            guesses=[],
            elo=user.elo_rating,  # type: ignore
        )
        player2 = PlayerState(
            id=None,  # type: ignore
            name=None,  # type: ignore
            secret=secret,
            guesses=[],
            elo=None,  # type: ignore
        )
        return await super().create(
            player1=player1,
            player2=player2,
            status="waiting",
            game_mode="pvp",
        )

    async def join_game(self, game: PvPGame, user: User, secret: str) -> PvPGame:
        player1 = PlayerState(
            id=game.player1.id,
            name=game.player1.name,
            secret=secret,
            guesses=game.player1.guesses,
            elo=game.player1.elo,
        )
        player2 = PlayerState(
            id=user.id,  # type: ignore
            name=user.display_name,  # type: ignore
            secret=game.player2.secret,
            guesses=[],
            elo=user.elo_rating,  # type: ignore
        )
        game.player1 = player1
        game.player2 = player2
        game.status = "in_progress"  # type: ignore
        game.started_at = datetime.utcnow()  # type: ignore
        await self.session.flush()
        await self.session.refresh(game)
        return game

    async def create_ai_game(
        self,
        user: User,
        user_secret: str,
        ai_secret: str,
        ai_name: str,
        ai_elo: int,
        ai_difficulty: str,
    ) -> PvPGame:  # type: ignore
        player1 = PlayerState(
            id=user.id,  # type: ignore
            name=user.display_name,  # type: ignore
            secret=user_secret,
            guesses=[],
            elo=user.elo_rating,  # type: ignore
        )
        player2 = PlayerState(
            id=None,  # type: ignore
            name=ai_name,
            secret=ai_secret,
            guesses=[],
            elo=ai_elo,
        )
        return await super().create(
            player1=player1,
            player2=player2,
            status="in_progress",
            game_mode="ai",
            ai_difficulty=ai_difficulty,
            started_at=datetime.utcnow(),
        )

    async def get_waiting_games(self) -> list[PvPGame]:
        result = await self.session.execute(select(PvPGame).where(PvPGame.status == "waiting"))
        return list(result.scalars().all())

    async def get_by_player_id(self, player_id: int) -> list[PvPGame]:
        result = await self.session.execute(
            select(PvPGame).where((PvPGame.player1.id == player_id) | (PvPGame.player2.id == player_id))
        )
        return list(result.scalars().all())

    async def make_guess(
        self,
        game: PvPGame,
        user: User,
        guess: str,
        exact: int,
        wrong_pos: int,
        is_winner: bool,
    ) -> PvPGame:
        curr_guess = [{"guess": guess, "exact": exact, "wrong_pos": wrong_pos}]
        if game.player1.id == user.id:
            player = PlayerState(
                id=game.player1.id,
                name=game.player1.name,
                secret=game.player1.secret,
                guesses=game.player1.guesses + curr_guess,
                elo=game.player1.elo,
            )
            game.player1 = player
        else:
            player = PlayerState(
                id=game.player2.id,
                name=game.player2.name,
                secret=game.player2.secret,
                guesses=game.player2.guesses + curr_guess,
                elo=game.player2.elo,
            )
            game.player2 = player
        if is_winner:
            game.winner_id = player.id  # type: ignore
            game.status = "completed"  # type: ignore
            game.completed_at = datetime.utcnow()  # type: ignore
        await self.session.flush()
        await self.session.refresh(game)
        return game
