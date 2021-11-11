"""Random player"""
import random
from typing import Sequence

from bots.BotInterface import BotInterface
from environment.Constants import Action, Stage
from environment.Observation import Observation
from utils.handValue import getHandPercent

# your bot class, rename to match the file name
class KaijiBot(BotInterface):

    # change the name of your bot here
    def __init__(self, name="KaijiBot"):
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
        
        position = observation.myPosition
        
        stage = observation.stage
        opponent_actions_this_round = observation.get_opponent_history_current_stage()
        # Get the last action the opponent have done
        last_action = None
        last_last_action = None
        if len(opponent_actions_this_round) > 0:
            last_action = opponent_actions_this_round[-1] 
            if len(opponent_actions_this_round) > 1:
               last_last_action = opponent_actions_this_round[-2]
        else: 
            None

        if position == 0:
            if stage == Stage.PREFLOP:
                handpercent, _  = getHandPercent(observation.myHand)
                if handpercent < .30:        
                    return Action.RAISE
                elif handpercent < .50:
                    return Action.CALL
                elif handpercent < 0.90:
                    return Action.CHECK
                else: 
                    return Action.FOLD
            else:
                handpercent, cards  = getHandPercent(observation.myHand, observation.boardCards)
                if handpercent < .15:        
                    return Action.RAISE
                elif handpercent < 0.30 and last_action != Action.RAISE:
                    return Action.RAISE
                elif handpercent < .50 and last_action != Action.RAISE:
                    return Action.CALL
                elif handpercent < 0.70:
                    return Action.CHECK
                else:
                    return Action.FOLD
        else:
            if stage == Stage.PREFLOP:
                handpercent, _  = getHandPercent(observation.myHand)
                if handpercent < .40:        
                    return Action.RAISE
                elif handpercent < 0.90:
                    return Action.CHECK
                else: 
                    return Action.FOLD
            else:
                handpercent, cards  = getHandPercent(observation.myHand, observation.boardCards)
                if handpercent < .15:        
                    return Action.RAISE
                elif handpercent < 0.30 and last_action != Action.RAISE:
                    return Action.RAISE
                elif handpercent < 0.70:
                    return Action.CHECK
                else:
                    return Action.FOLD