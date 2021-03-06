from typing import Dict, List, Sequence

from bots import BotInterface
from environment import Action, Stage


class Player:
    bot: BotInterface
    stack: int
    contribution: int
    position: int
    active: bool
    win: bool
    reward: int
    history: Dict[Stage, List[Action]]
    hand: Sequence[str]

    def __init__(self, bot: BotInterface) -> None:
        self.bot = bot

    def reset(self, stack: int, position: int) -> None:
        self.stack = stack
        self.contribution = 0
        self.position = position
        self.active = True
        self.hand = []
        self.history = {}
        self.win = False
        self.reward = 0
        for stage in Stage:
            self.history[stage] = []

    def postAmount(self, amount: int) -> None:
        self.contribution += amount
        self.stack -= amount

    def isAutoPlayer(self) -> bool:
        return self.bot.autoPlay
