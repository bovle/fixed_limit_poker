import random
from typing import Sequence

from environment.Constants import Action, Stage
from bots.BotInterface import BotInterface
from environment.Constants import Action
from environment.Observation import Observation
from environment.Player import Player
from environment.PlayerObservation import PlayerObservation
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
        #elif observation.stage == Stage.RIVER:
            #return self.handleRiver(observation, action_space)
        else:
            return self.handlePostFlop(observation, action_space)

    def handlePostFlop(self, observation: Observation, action_space:Sequence[Action]) -> Action:
        handPercent, cards = getHandPercent(observation.myHand,observation.boardCards)
        handType, bestCards = getHandType(observation.myHand, observation.boardCards)
        boardType = getBoardHandType(observation.boardCards)
        longestStraight = getLongestStraight(observation.myHand, observation.boardCards)


        opponentActions = observation.get_opponent_history_current_stage()

        opponentRaiseFactor = opponentActions.count(Action.RAISE)/100

        opponent_actions_this_round = observation.get_opponent_history_current_stage()
        if (self.goodHandFactor(observation,handType, handPercent) - opponentRaiseFactor > 0.7):
            return Action.RAISE
        elif (self.goodHandFactor(observation, handType, handPercent) - opponentRaiseFactor > 0.5):
            return Action.CALL
        elif (self.goodHandFactor(observation, handType, handPercent) - opponentRaiseFactor > 0.3):
            return Action.CHECK
        elif (self.goodHandFactor(observation, handType, handPercent) - opponentRaiseFactor < 0.3):
            return Action.FOLD

    def goodHandFactor(self, observation: Observation, handType, handPercent) -> float:

        result = 1
        if (handType == HandType.STRAIGHTFLUSH):
            result*=1

        if (handType == HandType.STRAIGHT):
            result*=1

        if handType == HandType.FLUSH:
            result*=1

        if handType == HandType.THREEOFAKIND:
            result*=0.9

        if handType == HandType.FULLHOUSE:
            result*=0.9

            result*=-(0-handPercent)
        return result

        

    def checkIfBadHand(self, observation: Observation) -> bool:
        handPercent, cards = getHandPercent(observation.myHand,observation.boardCards)
        handType, bestCards = getHandType(observation.myHand, observation.boardCards)
        if handType not in [HandType.FLUSH, HandType.FOUROFAKIND]:
            return True

    def checkIfBadHand(self, observation: Observation) -> bool:
        handPercent, cards = getHandPercent(observation.myHand,observation.boardCards)
        handType, bestCards = getHandType(observation.myHand, observation.boardCards)
        if handType not in [HandType.FLUSH, HandType.FOUROFAKIND]:
            return True

    def handleRiver(self, observation: Observation, action_space:Sequence[Action]) -> Action:
        handPercent, cards = getHandPercent(observation.myHand,observation.boardCards)
        handType, bestCards = getHandType(observation.myHand, observation.boardCards)
        boardType = getBoardHandType(observation.boardCards)
        longestStraight = getLongestStraight(observation.myHand, observation.boardCards)

        #if (handPercent > 0.8):
            #return Action.FOLD

        if (handType == HandType.STRAIGHTFLUSH):
            return Action.RAISE

        if (handType == HandType.STRAIGHT):
            return Action.RAISE

        if handType == HandType.THREEOFAKIND and boardType != handType.THREEOFAKIND:
            return Action.RAISE

        if handType == HandType.FLUSH:
            return Action.RAISE

        #if handType == HandType.FULLHOUSE:
        #    return Action.RAISE


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
        if (handType == HandType.PAIR): 
            return Action.CALL
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