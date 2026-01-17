from abc import ABC, abstractmethod

from backend.core.game_engine import MasterMindGame


class BaseAI(ABC):
    def __init__(self, master_mind_game: MasterMindGame):
        self.master_mind_game = master_mind_game

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def elo(self) -> int:
        pass

    @abstractmethod
    def get_next_guess(self) -> str:
        pass
