import dataclasses
from datetime import datetime
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectin_polymorphic

from backend.db.models.game import Game, PlayerState, PvPGame, SingleGame
from backend.db.models.user import User
from backend.db.repositories.base import BaseRepository


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

    async def create(self, player: PlayerState) -> SingleGame:  # type: ignore
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
        player: PlayerState,
        opponent: PlayerState,
        winner_id: int | None = None,
    ) -> SingleGame:
        game.player = player
        if winner_id is not None:
            game.winner_id = winner_id  # type: ignore
            game.status = "completed"  # type: ignore
            game.completed_at = datetime.utcnow()  # type: ignore
        await self.session.flush()
        await self.session.refresh(game)
        return game


class PvPGameRepository(BaseRepository[PvPGame]):
    def __init__(self, session: AsyncSession):
        super().__init__(PvPGame, session)

    async def create(self, player1: PlayerState, player2: PlayerState) -> PvPGame:  # type: ignore
        return await super().create(
            player1=player1,
            player2=player2,
            status="waiting",
            game_mode="pvp",
        )

    async def join_game(self, game: PvPGame, player1: PlayerState, player2: PlayerState, current_turn: int) -> PvPGame:
        game.player1 = player1
        game.player2 = player2
        game.status = "in_progress"  # type: ignore
        game.started_at = datetime.utcnow()  # type: ignore
        game.current_turn = current_turn  # type: ignore

        await self.session.flush()
        await self.session.refresh(game)
        return game

    async def create_ai_game(
        self, player1: PlayerState, player2: PlayerState, ai_difficulty: str, current_turn: int
    ) -> PvPGame:  # type: ignore
        return await super().create(
            player1=player1,
            player2=player2,
            status="in_progress",
            game_mode="ai",
            ai_difficulty=ai_difficulty,
            started_at=datetime.utcnow(),
            current_turn=current_turn,  # type: ignore
        )

    async def get_waiting_games(self) -> list[PvPGame]:
        # TODO: Change to get a random waiting game, and set to joining.
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
        player1: PlayerState,
        player2: PlayerState,
        winner_id: int | None = None,
    ) -> PvPGame:
        if winner_id is not None:
            await self._finish_game(game, winner_id=winner_id, status="completed")
            await self._update_elo(player1, player2, winner_id)
        else:
            game.current_turn = player2.id if game.current_turn == player1.id else player1.id

        game.player1 = player1
        game.player2 = player2

        await self.session.flush()
        await self.session.refresh(game)
        return game

    async def abandon_game(self, game: PvPGame, abandoner: User) -> PvPGame:
        winner_id = game.player2.id if game.player1.id == abandoner.id else game.player1.id
        await self._finish_game(game, winner_id=winner_id, status="abandoned")
        player1 = PlayerState(**dataclasses.asdict(game.player1))
        player2 = PlayerState(**dataclasses.asdict(game.player2))
        await self._update_elo(player1, player2, winner_id)

        game.player1 = player1
        game.player2 = player2

        await self.session.flush()
        await self.session.refresh(game)
        return game

    async def _finish_game(self, game: PvPGame, winner_id: int, status: str) -> None:
        """Shared logic for completing a game."""
        game.winner_id = winner_id
        game.status = status
        game.completed_at = datetime.utcnow()

    async def _update_elo(self, player1: PlayerState, player2: PlayerState, winner_id: int) -> None:
        p1_user = await self.session.get(User, player1.id)
        p2_user = await self.session.get(User, player2.id)

        if not p1_user or not p2_user:
            return

        winner, loser = (p1_user, p2_user) if winner_id == p1_user.id else (p2_user, p1_user)

        K = 32
        expected_winner = 1 / (1 + 10 ** ((loser.elo_rating - winner.elo_rating) / 400))
        points = int(K * (1 - expected_winner))

        winner.elo_rating += points
        loser.elo_rating -= points
        if winner_id == player1.id:
            player1.elo += points
            player2.elo -= points
        else:
            player2.elo += points
            player1.elo -= points
