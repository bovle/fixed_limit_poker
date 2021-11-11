"""Random player"""
from pickle import FALSE, TRUE
import random
from typing import Sequence

from bots.BotInterface import BotInterface
from environment.Constants import Action, Stage
from environment.Observation import Observation
from utils.handValue import getHandPercent, getHandType

# your bot class, rename to match the file name
class MIKH_Bot(BotInterface):
    should_bluff = TRUE
    hand_value = 0

    # change the name of your bot here
    def __init__(self, name="MIKH"):
        '''init function'''
        super().__init__(name=name)

    def act(self, action_space:Sequence[Action], observation:Observation) -> Action:

        myCards = observation.myHand

        # If having a pair - go crazy!
        if(myCards[0][0] == myCards[1][0]):
            return Action.RAISE

        stage = observation.stage

        # Make an inital strategy
        if stage == Stage.PREFLOP:
            if(random.random() < 0.05):
                self.should_bluff = TRUE
            else:
                self.should_bluff = FALSE

            if myCards[0][0] == myCards[1][0]:
                self.hand_value = 1
            elif myCards[0][1] == myCards[1][1]:
                self.hand_value = 0.2

        if self.should_bluff:
            if random.random() < 0.75:
                    return Action.RAISE
            else:
                return Action.CALL

        
        if stage == Stage.PREFLOP:
            return self.handlePreFlop(observation)
        else:
            return self.handleEnd(observation)
        '''
        stage = observation.stage
        if stage == Stage.PREFLOP:
            return self.handlePreFlop(observation)

        elif stage == Stage.RIVER:
            return self.handlePostRiver(observation)
        elif stage == Stage.TURN:
            return self.handlePostTurn(observation)
        else:
            return self.handlePostFlop(observation)
        '''


        '''
            This function gets called whenever it's your bots turn to act.
                Parameters:
                    action_space (Sequence[Action]): list of actions you are allowed to take at the current state. 
                    observation (Observation): all information available to your bot at the current state. See environment/Observation for details
                returns:
                    action (Action): the action you want you bot to take. Possible actions are: FOLD, CHECK, CALL and RAISE
            If this function takes longer than 1 second, your bot will fold
        '''
    def handlePreFlop(self, observation: Observation) -> Action:
        # get my hand's percent value (how good is this 2 card hand out of all possible 2 card hands)
        handPercent, _ = getHandPercent(observation.myHand)
        # if my hand is top 20 percent: raise
        if handPercent < .25:
            return Action.RAISE
        # if my hand is top 60 percent: call
        elif handPercent < .70:
            return Action.CALL
        # else fold
        return Action.FOLD

    def handlePostFlop(self, observation: Observation) -> Action:
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
    
    def handleEnd(self, observation: Observation) -> Action:
        opponent_actions_this_round = observation.get_opponent_history_current_stage()
        # Get the last action the opponent have done
        handPercent, _ = getHandPercent(observation.myHand)
        last_action = opponent_actions_this_round[-1] if len(
            opponent_actions_this_round) > 0 else None

        if last_action is None:
            # opponent didn't do anything yet for us to counter, just raise
            return Action.RAISE
        elif last_action in [Action.CHECK, Action.CALL]:
            # opponent checked, try to steal the pot with a raise
            return Action.RAISE
        elif last_action == Action.RAISE:
            # opponent raise, probably has good cards so fold
            if ((random.random() < 0.2 and handPercent > 0.25) or handPercent > 0.5):
                return Action.FOLD
            else:
                return Action.CALL
        '''
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
        '''

    def handlePostRiver(self, observation: Observation) -> Action:
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

    def handlePostTurn(self, observation: Observation) -> Action:
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