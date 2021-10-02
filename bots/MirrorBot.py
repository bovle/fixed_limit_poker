"""This bot mirrors the actions of the opponent"""
from environment.Observation import Observation
from environment.Constants import Action
from typing import Sequence
from bots.BotInterface import BotInterface
import itertools


class MirrorBot(BotInterface):

    def __init__(self, name="mirror"):
        super().__init__(name=name)

    def act(self, action_space: Sequence[Action], observation: Observation) -> Action:
        opponent = next(x for x in observation.players if x.name != self.name)
        last_actions = list(itertools.chain(*opponent.history.values()))
        last_action = last_actions[-1] if last_actions else None

        # Previous player didn't do anything yet for us to mirror, just check / call
        if last_action is None:
            if Action.CHECK in action_space:
                return Action.CHECK
            else:
                Action.CALL
        elif last_action in action_space:
            # repeat action if allowed
            return last_action
        else:
            # We cannot do the same, so we fold
            return Action.FOLD
