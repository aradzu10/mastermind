from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.models.pvp_game import PvPGame
from backend.db.repositories.base import BaseRepository


class PvPGameRepository(BaseRepository[PvPGame]):
    def __init__(self, session: AsyncSession):
        super().__init__(PvPGame, session)

    async def get_waiting_games(self) -> list[PvPGame]:
        """Get all games waiting for a second player."""
        result = await self.session.execute(
            select(PvPGame).where(PvPGame.status == "waiting")
        )
        return list(result.scalars().all())

    async def get_by_player_id(self, player_id: int) -> list[PvPGame]:
        """Get all games for a specific player."""
        result = await self.session.execute(
            select(PvPGame).where(
                (PvPGame.player1_id == player_id) | (PvPGame.player2_id == player_id)
            )
        )
        return list(result.scalars().all())

    async def complete_game(self, game_id: int, winner_id: int) -> Optional[PvPGame]:
        """Mark a PvP game as completed with a winner."""
        game = await self.get(game_id)
        if game:
            game.status = "completed"  # type: ignore
            game.winner_id = winner_id  # type: ignore
            game.completed_at = datetime.utcnow()  # type: ignore
            await self.session.flush()
            await self.session.refresh(game)
        return game
