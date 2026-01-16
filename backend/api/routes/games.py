from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db.database import get_db
from backend.schemas.game import GameCreate, GameResponse, GameGuess, GameGuessResponse
from backend.services.game_service import GameService
from typing import List

router = APIRouter(prefix="/api/games", tags=["games"])


@router.post("/single", response_model=GameResponse, status_code=201)
async def create_single_player_game(
    game_data: GameCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new single-player game"""
    service = GameService(db)
    game = await service.create_game(user_id=None, game_mode=game_data.game_mode)

    return GameResponse(
        id=game.id,
        user_id=game.user_id,
        attempts=game.attempts,
        won=game.won,
        game_mode=game.game_mode,
        guesses=[],
        completed_at=game.completed_at,
        created_at=game.created_at
    )


@router.get("/{game_id}", response_model=GameResponse)
async def get_game(
    game_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get game state"""
    service = GameService(db)
    game = await service.get_game(game_id)

    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    guesses = game.guesses or []
    return GameResponse(
        id=game.id,
        user_id=game.user_id,
        attempts=game.attempts,
        won=game.won,
        game_mode=game.game_mode,
        guesses=guesses,
        completed_at=game.completed_at,
        created_at=game.created_at
    )


@router.post("/{game_id}/guess", response_model=GameGuessResponse)
async def make_guess(
    game_id: int,
    guess_data: GameGuess,
    db: AsyncSession = Depends(get_db)
):
    """Make a guess in the game"""
    service = GameService(db)

    try:
        result = await service.make_guess(game_id, guess_data.guess)
        return GameGuessResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
