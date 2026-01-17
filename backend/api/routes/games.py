from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.database import get_db
from backend.schemas.game import GameCreate, GameGuess, GameGuessResponse, GameResponse
from backend.services.game_service import GameService

router = APIRouter(prefix="/api/games", tags=["games"])


@router.post("/single", response_model=GameResponse, status_code=201)
async def create_single_player_game(
    game_data: GameCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new game (single-player or AI opponent)"""
    service = GameService(db)
    game = await service.create_game(
        user_id=None, 
        game_mode=game_data.game_mode,
        player_secret=game_data.player_secret
    )

    return GameResponse(
        id=game.id,
        user_id=game.user_id,
        attempts=game.attempts,
        won=game.won,
        game_mode=game.game_mode,
        guesses=[],
        completed_at=game.completed_at,
        created_at=game.created_at,
        opponent_type=game.opponent_type,
        ai_guesses=game.ai_guesses or [] if game.game_mode == "ai" else None,
        player_secret=None,  # Never expose until game is over
        ai_won=None
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
    ai_guesses = game.ai_guesses or []
    
    # Determine if AI won
    ai_won = None
    if game.game_mode == "ai" and ai_guesses:
        last_ai_guess = ai_guesses[-1]
        if last_ai_guess.get("exact") == 4:
            ai_won = True
        elif game.completed_at:
            ai_won = False  # Game ended but AI didn't win
    
    # Only expose secrets if game is over
    player_secret_exposed = None
    if game.completed_at and game.player_secret:
        player_secret_exposed = game.player_secret
    
    return GameResponse(
        id=game.id,
        user_id=game.user_id,
        attempts=game.attempts,
        won=game.won,
        game_mode=game.game_mode,
        guesses=guesses,
        completed_at=game.completed_at,
        created_at=game.created_at,
        opponent_type=game.opponent_type,
        ai_guesses=ai_guesses if game.game_mode == "ai" else None,
        player_secret=player_secret_exposed,
        ai_won=ai_won
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
