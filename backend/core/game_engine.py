import random
from collections import Counter
from dataclasses import dataclass


@dataclass
class GuessRecord:
    guess: str
    exact: int
    wrong_pos: int


class MasterMindGame:
    def __init__(self, player_secret: str | None = None, history: list[GuessRecord] | None = None):
        self.num_digits = 4
        self.secret = player_secret or self._generate_secret_number()
        self.history: list[GuessRecord] = history or []
        self.attempts = len(self.history)

    def _generate_secret_number(self) -> str:
        digits = random.choices(range(10), k=self.num_digits)
        return "".join(map(str, digits))

    def validate_guess(self, guess: str) -> bool:
        return len(guess) == self.num_digits and guess.isdigit()

    def evaluate_guess(self, guess: str) -> tuple[int, int]:
        exact_matches = 0

        for secret_digit, guess_digit in zip(self.secret, guess):
            if secret_digit == guess_digit:
                exact_matches += 1

        secret_counter = Counter(self.secret)
        guess_counter = Counter(guess)

        total_matches = 0
        for digit in guess_counter:
            total_matches += min(secret_counter[digit], guess_counter[digit])

        wrong_position_matches = total_matches - exact_matches

        return exact_matches, wrong_position_matches

    def make_guess(self, guess: str) -> tuple[int, int, bool]:
        self.attempts += 1
        exact, wrong_pos = self.evaluate_guess(guess)
        is_winner = exact == self.num_digits
        self.history.append(GuessRecord(guess, exact, wrong_pos))

        return exact, wrong_pos, is_winner
