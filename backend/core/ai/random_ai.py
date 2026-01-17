import random

from backend.core.ai.base_ai import BaseAI
from backend.core.game_engine import MasterMindGame


class RandomAI(BaseAI):
    def __init__(self, master_mind_game: MasterMindGame):
        super().__init__(master_mind_game)
        self.used_guesses = set(g.guess for g in self.master_mind_game.history)

    @property
    def name(self) -> str:
        return "Brad"

    def get_next_guess(self) -> str:
        max_attempts = 100
        for _ in range(max_attempts):
            guess = "".join(str(random.randint(0, 9)) for _ in range(4))
            if guess not in self.used_guesses:
                return guess

        return "".join(str(random.randint(0, 9)) for _ in range(4))
