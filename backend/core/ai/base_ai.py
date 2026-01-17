from abc import ABC, abstractmethod

from backend.core.game_engine import MasterMindGame
from backend.db.models.user import User


class BaseAI(ABC):
    def __init__(self, master_mind_game: MasterMindGame):
        self.master_mind_game = master_mind_game

    @staticmethod
    @abstractmethod
    def user() -> User:
        pass

    @abstractmethod
    def get_next_guess(self) -> str:
        pass
