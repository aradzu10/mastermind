from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.db.models.game import Game
from backend.db.repositories.base import BaseRepository


class GameRepository(BaseRepository[Game]):
    def __init__(self, session: AsyncSession):
        super().__init__(Game, session)

    async def get_by_user_id(self, user_id: int, limit: int = 10) -> List[Game]:
        result = await self.session.execute(
            select(Game)
            .where(Game.user_id == user_id)
            .order_by(Game.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_active_games(self, user_id: int) -> List[Game]:
        result = await self.session.execute(
            select(Game)
            .where(Game.user_id == user_id, Game.completed_at == None)
            .order_by(Game.created_at.desc())
        )
        return list(result.scalars().all())

    async def complete_game(self, game_id: int, won: bool) -> Optional[Game]:
        from datetime import datetime
        game = await self.get(game_id)
        if game:
            game.won = won
            game.completed_at = datetime.utcnow()
            await self.session.flush()
            await self.session.refresh(game)
        return game
