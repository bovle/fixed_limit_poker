"""Troels"""
from typing import Sequence

from bots.BotInterface import BotInterface
from environment.Constants import Action, Stage
from environment.Observation import Observation
from utils.handValue import getHandPercent

RAISE_PRE_FLOP = .40
CALL_PRE_FLOP = .80
RAISE_POST_FLOP = .60
CALL_POST_FLOP = .90

class SpookyBot(BotInterface):
    """
    Based on counterbot...
    """

    def __init__(self, name="SpookyBot"):
        super().__init__(name=name)

    def act(self, action_space: Sequence[Action], observation: Observation) -> Action:
        stage = observation.stage       
        if stage == Stage.PREFLOP:
            return self.handlePreFlop(observation)

        return self.handlePostFlop(observation)

    def handlePreFlop(self, observation: Observation) -> Action:
        opponent_actions_this_round = observation.get_opponent_history_current_stage()
        last_action = opponent_actions_this_round[-1] if len(opponent_actions_this_round) > 0 else None
        # get my hand's percent value (how good is this 2 card hand out of all possible 2 card hands)
        handPercent, _ = getHandPercent(observation.myHand)
        if last_action is None:
            if handPercent < RAISE_PRE_FLOP:
                return Action.RAISE
            elif handPercent < CALL_PRE_FLOP:
                return Action.CALL
        elif last_action in (Action.CHECK, Action.CALL):
            if handPercent < 0.8:
                return Action.RAISE
        elif last_action == Action.RAISE:
            if handPercent < 0.3:
                return Action.RAISE
            elif handPercent < 0.5:
                return Action.CALL
            
            return Action.FOLD
            
        # else fold
        return Action.FOLD

    def handlePostFlop(self, observation: Observation) -> Action:
        opponent_actions_this_round = observation.get_opponent_history_current_stage()
        last_action = opponent_actions_this_round[-1] if len(opponent_actions_this_round) > 0 else None
        # get my hand's percent value (how good is this 2 card hand out of all possible 2 card hands)
        handPercent, _ = getHandPercent(observation.myHand)
        if last_action is None:
            if handPercent < RAISE_PRE_FLOP:
                return Action.RAISE
            elif handPercent < CALL_PRE_FLOP:
                return Action.CALL
        elif last_action in (Action.CHECK, Action.CALL):
            if handPercent < 0.8:
                return Action.RAISE
        elif last_action == Action.RAISE:
            if handPercent < 0.3:
                return Action.RAISE
            elif handPercent < 0.5:
                return Action.CALL
