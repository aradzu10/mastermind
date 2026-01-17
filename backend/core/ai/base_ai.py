from abc import ABC, abstractmethod
from typing import List


class BaseAI(ABC):
    """Abstract base class for AI players in Mastermind."""
    
    def __init__(self):
        self.previous_guesses: List[dict] = []
    
    @abstractmethod
    def get_next_guess(self) -> str:
        """
        Generate the next guess based on previous feedback.
        
        Returns:
            str: A 4-digit string guess
        """
        pass
    
    def record_guess(self, guess: str, exact: int, wrong_pos: int):
        """
        Record a guess and its feedback for future decision-making.
        
        Args:
            guess: The guess that was made
            exact: Number of exact matches
            wrong_pos: Number of correct digits in wrong positions
        """
        self.previous_guesses.append({
            "guess": guess,
            "exact": exact,
            "wrong_pos": wrong_pos
        })
    
    def reset(self):
        """Reset the AI state for a new game."""
        self.previous_guesses = []
