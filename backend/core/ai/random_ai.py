import random

from backend.core.ai.base_ai import BaseAI


class RandomAI(BaseAI):
    """AI that makes completely random valid guesses."""
    
    def __init__(self):
        super().__init__()
        self.used_guesses = set()
    
    def get_next_guess(self) -> str:
        """
        Generate a random 4-digit guess.
        Avoids repeating previous guesses for efficiency.
        
        Returns:
            str: A random 4-digit string
        """
        # Keep trying until we find an unused guess
        # In worst case, there are 10,000 possible combinations
        max_attempts = 100
        for _ in range(max_attempts):
            guess = "".join(str(random.randint(0, 9)) for _ in range(4))
            if guess not in self.used_guesses:
                self.used_guesses.add(guess)
                return guess
        
        # Fallback: just return a random guess even if repeated
        return "".join(str(random.randint(0, 9)) for _ in range(4))
    
    def reset(self):
        """Reset the AI state for a new game."""
        super().reset()
        self.used_guesses = set()
