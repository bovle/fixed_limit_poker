"""This bot tries to counter the actions of the opponent"""
import itertools
from typing import Sequence

from bots.BotInterface import BotInterface
from environment.Constants import Action
from environment.Observation import Observation


class CounterBot(BotInterface):

    def __init__(self, name="counter"):
        super().__init__(name=name)

    def act(self, action_space: Sequence[Action], observation: Observation) -> Action:
        opponent = next(x for x in observation.players if x.name != self.name)
        actions_this_round = opponent.history[observation.stage]
        last_action = actions_this_round[-1] if len(actions_this_round) > 0 else None

        
        if last_action is None:
            # Previous player didn't do anything yet for us to counter, just raise
            return Action.RAISE
        elif last_action in [Action.CHECK, Action.CALL]:
            # opponent checked, try to steal the pot with a raise
            return Action.RAISE
        elif last_action == Action.RAISE :
            # opponent raise, just call, try to steal later
            return Action.CALL

        # default fold
        return Action.FOLD
