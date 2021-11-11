"""Random player"""
import random
from typing import Sequence

from bots.BotInterface import BotInterface
from environment import observers
from environment.Constants import Action, Stage
from environment.Observation import Observation

from utils.handValue import *

# your bot class, rename to match the file name


class FalBot(BotInterface):

    # change the name of your bot here
    def __init__(self, name="FalBot"):
        '''init function'''
        super().__init__(name=name)

    def act(self, action_space: Sequence[Action], observation: Observation) -> Action:
        '''
            This function gets called whenever it's your bots turn to act.
                Parameters:
                    action_space (Sequence[Action]): list of actions you are allowed to take at the current state. 
                    observation (Observation): all information available to your bot at the current state. See environment/Observation for details
                returns:
                    action (Action): the action you want you bot to take. Possible actions are: FOLD, CHECK, CALL and RAISE
            If this function takes longer than 1 second, your bot will fold
        '''
        handType, handTypeCards = getHandType(observation.myHand, observation.boardCards)
        if (handType in [HandType.STRAIGHTFLUSH,
                        HandType.FOUROFAKIND,
                        HandType.FULLHOUSE,
                        HandType.FLUSH,
                        HandType.STRAIGHT,
                        HandType.THREEOFAKIND,
                        HandType.TWOPAIR]) and self.handInBest(observation.myHand, handTypeCards):
            return Action.RAISE
        
        # handPercent, cards = getHandPercent(
        #     observation.myHand, observation.boardCards)

        # longestStraight = getLongestStraight(observation.myHand, observation.boardCards)[0]
        # if longestStraight == 4 and observation.stage.__index__() < 2:
        #     return Action.RAISE
        if observation.stage == Stage.PREFLOP:
            return self.handlePreFlop(observation)

        return self.handlePostFlop(observation)

    def handlePreFlop(self, observation: Observation) -> Action:
        # get my hand's percent value (how good is this 2 card hand out of all possible 2 card hands)
        handPercent, cards = getHandPercent(observation.myHand)
        # if my hand is top 20 percent: raise
        if handPercent < .20 and self.handInBest(observation.myHand, cards):
            return Action.RAISE
        # if my hand is top 60 percent: call
        elif handPercent < .60:
            return Action.CALL
        # else fold
        return Action.FOLD

    def handlePostFlop(self, observation: Observation) -> Action:
        # get my hand's percent value (how good is the best 5 card hand i can make out of all possible 5 card hands)
        opponentActions = observation.get_opponent_history_current_stage()
        if len(opponentActions) > 0:
            lastOpponenActionsIsRaise = opponentActions[-1] = Action.RAISE
        else:
            lastOpponenActionsIsRaise = False
        handPercent, cards = getHandPercent(
            observation.myHand, observation.boardCards)
        # if my hand is top 30 percent: raise
        if handPercent <= .30:
            return Action.RAISE
        # if my hand is top 80 percent: call
        elif lastOpponenActionsIsRaise and handPercent <= .60:
            return Action.CALL
        elif not lastOpponenActionsIsRaise and handPercent <= .80:
            return Action.CALL
        # else fold
        return Action.FOLD

    def handInBest(self, hand: Sequence[str], usedCards: list[str]) -> bool:
        for c in hand:
            if (c in usedCards):
                return True
        return False
