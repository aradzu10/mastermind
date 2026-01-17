from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.dependencies import get_current_user
from backend.db.database import get_db
from backend.db.models.game import Game, PlayerState
from backend.db.models.user import User
from backend.schemas.game import GameCreate, GameGuess, GameResponse
from backend.services.game_service import GameService

router = APIRouter(prefix="/api/games", tags=["games"])


def _game_response_from_game(game: Game, user: User) -> GameResponse:
    if game.game_mode == "single":
        self_player = game.player
        opponent_player = PlayerState(id=None, name=None, secret=None, guesses=None)
    elif game.game_mode == "ai":
        self_player = game.player1
        opponent_player = game.player2
    else:
        self_player = game.player1 if game.player1.id == user.id else game.player2
        opponent_player = game.player2 if game.player1.id == user.id else game.player1

    self_secret = self_player.secret if game.status == "completed" else None
    return GameResponse(
        id=game.id,
        game_mode=game.game_mode,
        self_id=self_player.id,
        self_name=self_player.name,
        self_secret=self_secret,  # type: ignore
        self_guesses=self_player.guesses,
        winner_id=game.winner_id,
        created_at=game.created_at,
        completed_at=game.completed_at,
        status=game.status,
        started_at=game.started_at,
        # PvP Specific
        opponent_id=opponent_player.id,
        opponent_name=opponent_player.name,
        opponent_secret=opponent_player.secret,
        opponent_guesses=opponent_player.guesses,
        current_turn=getattr(game, "current_turn", None),
        # AI Specific
        ai_difficulty=getattr(game, "ai_difficulty", None),
    )


@router.post("/new", response_model=GameResponse, status_code=201)
async def create_new_game(
    game_data: GameCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    print("here")
    service = GameService(db)
    try:
        game = await service.create_game(
            user=user,
            game_mode=game_data.game_mode,  # type: ignore
            player_secret=game_data.player_secret,
            ai_difficulty=game_data.ai_difficulty,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return _game_response_from_game(game, user)


@router.get("/{game_id}", response_model=GameResponse)
async def get_game(
    game_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    service = GameService(db)
    try:
        game = await service.get_game(game_id, user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return _game_response_from_game(game, user)


@router.post("/{game_id}/guess", response_model=GameResponse)
async def make_guess(
    game_id: int,
    guess_data: GameGuess,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    service = GameService(db)

    try:
        game = await service.make_guess(game_id, guess_data.guess, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return _game_response_from_game(game, user)


@router.post("/{game_id}/opponent_guess", response_model=GameResponse)
async def opponent_guess(
    game_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    service = GameService(db)

    try:
        game = await service.get_opponent_guess(game_id, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return _game_response_from_game(game, user)
