"""Random player"""
import random
from typing import Sequence

from bots.BotInterface import BotInterface
from environment.Constants import Action
from environment.Observation import Observation

# your bot class, rename to match the file name
class KaijiBot(BotInterface):

    # change the name of your bot here
    def __init__(self, name="nc_template"):
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

        
        round = observation.stage

        # Check if percent is high enough
        if round == Stage.PREFLOP:
            handpercent = getHandPercent(observation.myHand)
            if handPercent < .20:        
                return Action.RAISE
            elif handPercent < .40:
                return Action.CALL
            elif handpercent < 0.80:
                return Action.CHECK
        else: 
            handpercent = getHandPercent(observation.myHand, observation.boardCards)
            if handPercent < .20:        
                return Action.RAISE
            elif handPercent < .40:
                return Action.CALL
            elif handpercent < 0.80:
                return Action.CHECK

        return action