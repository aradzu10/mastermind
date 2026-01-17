from backend.core.ai.base_ai import BaseAI
from backend.core.ai.random_ai import RandomAI


def get_ai_player(difficulty: str = "random") -> BaseAI:
    """
    Factory function to get the appropriate AI player.
    
    Args:
        difficulty: AI difficulty level ("random", "medium", "hard")
    
    Returns:
        BaseAI: An AI player instance
    """
    if difficulty == "random" or difficulty == "ai":
        return RandomAI()
    # Future implementations:
    # elif difficulty == "medium":
    #     return HeuristicAI()
    # elif difficulty == "hard":
    #     return MinimaxAI()
    else:
        # Default to random
        return RandomAI()


__all__ = ["BaseAI", "RandomAI", "get_ai_player"]
