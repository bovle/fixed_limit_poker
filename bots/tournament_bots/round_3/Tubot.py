import random
from typing import Sequence

from environment.Constants import Action, Stage
from bots.BotInterface import BotInterface
from environment.Constants import Action
from environment.Observation import Observation
from utils import handValue
from utils.createHandRankings import *
from utils.deuces import *
from utils.handValue import *

# your bot class, rename to match the file name
class Tubot(BotInterface):

    # change the name of your bot here
    def __init__(self, name="Tubot"):
        '''init function'''
        super().__init__(name=name)

    def act(self, action_space:Sequence[Action], observation:Observation) -> Action: 
        '''
            This function gets called whenever it's your bots turn to act.
                Parameters:
                    action_space (Sequence[Action]): list of actions you are allowed to take at the current state. 
                    observation (Observation): all information available to your bot at the current state. See environment/Observation for details
                returns:
                    action (Action): the action you want you bot to take. Possible actions are: FOLD, CHECK, CALL and RAISE
            If this function takes longer than 1 second, your bot will fold
        '''

        if observation.stage == Stage.PREFLOP:
            return self.handlePreFlop(observation, action_space)
        else:
            return self.handlePostFlop(observation, action_space)

    def handlePostFlop(self, observation: Observation, action_space:Sequence[Action]) -> Action:
        handPercent, cards = getHandPercent(observation.myHand,observation.boardCards)
        handType, bestCards = getHandType(observation.myHand, observation.boardCards)
        boardType = getBoardHandType(observation.boardCards)
        longestStraight = getLongestStraight(observation.myHand, observation.boardCards)


        if (handType == HandType.STRAIGHTFLUSH):
            return Action.RAISE

        if (handType == HandType.STRAIGHT):
            return Action.RAISE

        if handType == HandType.THREEOFAKIND and boardType != handType.THREEOFAKIND:
            return Action.RAISE

        if handPercent <= .3:
            return Action.RAISE
        elif handPercent <= .8:
            return Action.CALL

        if handType == HandType.TWOPAIR and boardType != HandType.TWOPAIR: 
            return Action.CALL

        return Action.FOLD


    def handlePreFlop(self, observation: Observation, action_space:Sequence[Action]) -> Action:
        handPercent, cards = getHandPercent(observation.myHand,observation.boardCards)
        handType, bestCards = getHandType(observation.myHand, observation.boardCards)
        boardType = getBoardHandType(observation.boardCards)
        if (handType == HandType.TWOPAIR): 
            return Action.RAISE
        elif handPercent > 0.8:
            return Action.FOLD
        else: 
            return Action.CALL
        #elif handPercent <= .30:
        #    action = Action.RAISE
        #elif handPercent <= .80:
        #    action = Action.CALL
        #else:
        #    action = Action.FOLD