import random

from backend.core.ai.base_ai import BaseAI
from backend.core.game_engine import MasterMindGame
from backend.db.models.user import User


class AradzBot(BaseAI):
    """
    Advanced AI that systematically tests all possibilities (0-9999)
    and validates each against all known constraints.
    """

    def __init__(self, master_mind_game: MasterMindGame):
        super().__init__(master_mind_game)

    @staticmethod
    def user() -> User:
        return User(
            id=0,
            email="aradz@ai.mastermind",
            display_name="Aradz",
            is_guest=False,
            elo_rating=2000.0,
        )

    def get_next_guess(self) -> str:
        """
        Try numbers from 0000 to 9999, checking if each passes all constraints
        from previous guesses.
        """
        numbers = list(range(10000))
        random.shuffle(numbers)
        for num in numbers:
            candidate = str(num).zfill(4)

            if self._is_valid_candidate(candidate):
                return candidate

        return "0000"

    def _is_valid_candidate(self, candidate: str) -> bool:
        mastermind = MasterMindGame(player_secret=candidate)
        for guess_record in self.master_mind_game.history:
            previous_guess = guess_record.guess
            expected_exact = guess_record.exact
            expected_wrong_pos = guess_record.wrong_pos

            exact, wrong_pos = mastermind.evaluate_guess(previous_guess)

            if exact != expected_exact or wrong_pos != expected_wrong_pos:
                return False

        return True
