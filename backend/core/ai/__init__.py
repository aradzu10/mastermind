from backend.core.ai.base_ai import BaseAI
from backend.core.ai.random_ai import RandomAI
from backend.core.ai.aradz_bot import AradzBot
from backend.core.game_engine import MasterMindGame


def get_ai_player(difficulty: str, master_mind_game: MasterMindGame) -> BaseAI:
    if difficulty == "easy":
        return RandomAI(master_mind_game)
    elif difficulty == "hard":
        return AradzBot(master_mind_game)
    # Future implementations:
    # elif difficulty == "medium":
    #     return HeuristicAI()
    else:
        raise ValueError(f"Unknown AI difficulty level: {difficulty}")


__all__ = ["BaseAI", "RandomAI", "AradzBot", "get_ai_player"]
