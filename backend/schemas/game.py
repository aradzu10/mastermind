from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime


class GuessRecord(BaseModel):
    guess: str = Field(..., min_length=4, max_length=4, pattern="^[0-9]{4}$")
    exact: int = Field(..., ge=0, le=4)
    wrong_pos: int = Field(..., ge=0, le=4)


class GameCreate(BaseModel):
    game_mode: str = Field(default="single", pattern="^(single|ai|pvp)$")
    player_secret: Optional[str] = Field(None, min_length=4, max_length=4, pattern="^[0-9]{4}$")  # For AI mode


class GameGuess(BaseModel):
    guess: str = Field(..., min_length=4, max_length=4, pattern="^[0-9]{4}$")


class GameResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: Optional[int]
    attempts: int
    won: bool
    game_mode: str
    guesses: List[GuessRecord]
    completed_at: Optional[datetime]
    created_at: datetime
    opponent_type: str = "none"  # none, ai, human
    ai_guesses: Optional[List[GuessRecord]] = None  # AI's guesses against player's secret
    player_secret: Optional[str] = None  # Hidden unless game is over
    ai_won: Optional[bool] = None  # Did the AI win?


class GameGuessResponse(BaseModel):
    game_id: int
    guess: str
    exact: int
    wrong_pos: int
    is_winner: bool
    attempts: int
    game_over: bool
    ai_move: Optional[dict] = None  # Contains ai_guess, exact, wrong_pos, ai_won if AI mode
