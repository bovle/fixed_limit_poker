"""Random player"""
import random
from typing import Sequence

from bots.BotInterface import BotInterface
from environment.Constants import Action, Stage
from environment.Observation import Observation
from utils.handValue import getBoardHandType, getHandPercent, getHandType


# your bot class, rename to match the file name
class Mobot(BotInterface):

    # change the name of your bot here
    def __init__(self, name="mobot"):
        '''init function'''
        super().__init__(name=name)

    def act(self, action_space: Sequence[Action], observation: Observation) -> Action:
        # use different strategy depending on pre or post flop (before or after community cards are delt)
        stage = observation.stage
 
        if stage == Stage.PREFLOP:
            return self.handlePreFlop(observation)

        if stage == Stage.FLOP:
            return self.handleFlop(observation)

        if stage == Stage.TURN:
            return self.handleTurn(observation)

        return self.handleRiver(observation)

    def handlePreFlop(self, observation: Observation) -> Action:
        # get my hand's percent value (how good is this 2 card hand out of all possible 2 card hands)
        handPercent, _ = getHandPercent(observation.myHand)
        # if my hand is top 20 percent: raise
        if handPercent < .3:
            return Action.RAISE

        elif handPercent < .50:
            return Action.CALL

        # else check
        return Action.CHECK


    def handleFlop(self, observation: Observation) -> Action:
        # get my hand's percent value (how good is this 2 card hand out of all possible 2 card hands)
        myTwoCardHandPercent, _ = getHandPercent(observation.myHand)
        communityHandPercent, cards = getHandPercent(observation.myHand, observation.boardCards)

        handTypeValue, c = getHandType(observation.myHand, observation.boardCards)

        # if my hand is top 20 percent: raise
        if myTwoCardHandPercent < .15:
            return Action.RAISE

        if communityHandPercent < .25:
            return Action.RAISE

        if handTypeValue < 7:
            return Action.RAISE

        # if my hand is top 60 percent: call
        elif myTwoCardHandPercent < .45:
            return Action.CALL
       
        # else fold
        return Action.CHECK

    def handleTurn(self, observation: Observation) -> Action:
        communityHandPercent, cards = getHandPercent(observation.myHand, observation.boardCards)
        handTypeValue, c = getHandType(observation.myHand, observation.boardCards)
        handTypeValueBoard = getBoardHandType(observation.boardCards)

        if communityHandPercent < 0.2:
            return Action.RAISE
    
        if handTypeValue.value < handTypeValueBoard.value-1:
            return Action.RAISE

        if handTypeValue < 5:
            return Action.RAISE

        if handTypeValue.value < handTypeValueBoard.value:
            return Action.CALL

        if communityHandPercent > 0.7:
            return Action.CHECK

        return Action.CALL

    def handleRiver(self, observation: Observation) -> Action:
        communityHandPercent, cards = getHandPercent(observation.myHand, observation.boardCards)

        handTypeValue, c = getHandType(observation.myHand, observation.boardCards)
        handTypeValueBoard = getBoardHandType(observation.boardCards)

        if communityHandPercent < 0.25:
            return Action.RAISE

        if handTypeValue.value < handTypeValueBoard.value-1:
            return Action.RAISE

        if handTypeValue < 5:
            return Action.RAISE

        if handTypeValue.value < handTypeValueBoard.value:
            return Action.CALL

        if communityHandPercent > 0.7:
            return Action.CHECK

        return Action.CALL

