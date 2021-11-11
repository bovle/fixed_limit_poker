"""Random player"""
import random
from typing import Sequence

from bots.BotInterface import BotInterface
from environment.Constants import Action, HandType
from environment.Observation import Observation
from utils.handValue import getHandPercent, getHandType

# your bot class, rename to match the file name
class ManagerBot(BotInterface):

    # change the name of your bot here
    def __init__(self, name="ManagerBot"):
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
        

        stage = observation.stage
        if stage == stage.PREFLOP:
            if self.doIHaveAGoodHand:
                return Action.RAISE
            return self.handlePreFlop(observation)

        return self.handlePostFlop(observation)

        # do a random action
        # action = random.choice(action_space)
        # return action
    
    def doIHaveAGoodHand(self, observation: Observation):
        handtype = getHandType(observation.myHand)
        if handtype[0] == HandType.PAIR or HandType.HIGHCARD:
            return True

        return False

    def doIHaveAGoodHandAgainstTheTable(self, observation:Observation):
        handtype = getHandType(observation.myHand, observation.boardCards)
        return False

    def handlePreFlop(self, observation: Observation) -> Action:
        # get my hand's percent value (how good is this 2 card hand out of all possible 2 card hands)
        handPercent, _ = getHandPercent(observation.myHand)
        # if my hand is top 20 percent: raise
        if handPercent < .20:
            return Action.RAISE
        # if my hand is top 60 percent: call
        elif handPercent < .60:
            return Action.CALL
        # else fold
        return Action.FOLD

    def handlePostFlop(self, observation: Observation) -> Action:
        # get my hand's percent value (how good is the best 5 card hand i can make out of all possible 5 card hands)
        handPercent, cards = getHandPercent(
            observation.myHand, observation.boardCards)
        # if my hand is top 30 percent: raise
        if handPercent <= .30:
            return Action.RAISE
        # if my hand is top 80 percent: call
        elif handPercent <= .80:
            return Action.CALL
        # else fold
        return Action.FOLD