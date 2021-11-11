"""You have been terminated!"""
from typing import Sequence

from bots.BotInterface import BotInterface
from environment.Constants import Action, HandType, Stage
from environment.Observation import Observation
from utils.handValue import getBoardHandType, getHandPercent, getHandType, getLongestStraight

# your bot class, rename to match the file name
class T800(BotInterface):

    # change the name of your bot here
    def __init__(self, name="T-800"):
        '''init function'''
        super().__init__(name=name)

    def act(self, action_space: Sequence[Action], observation: Observation) -> Action:
        # use different strategy depending on pre or post flop (before or after community cards are delt)
        stage = observation.stage
        opponent_actions_this_round = observation.get_opponent_history_current_stage()
        # Get the last action the opponent have done
        handType, handTypeCards = getHandType(
            observation.myHand, observation.boardCards)
        if handType in [HandType.STRAIGHTFLUSH,
                        HandType.FOUROFAKIND,
                        HandType.FULLHOUSE,
                        HandType.FLUSH,
                        HandType.STRAIGHT,
                        HandType.THREEOFAKIND,
                        HandType.TWOPAIR]:
            return Action.RAISE
        handPercent, cards = getHandPercent(
            observation.myHand, observation.boardCards)

        if handPercent > 0.9:
            Action.FOLD
        last_action = opponent_actions_this_round[-1] if len(
            opponent_actions_this_round) > 0 else None
        if stage == Stage.PREFLOP:
            return self.handlePreFlop(observation)
        if stage == Stage.FLOP:
            return self.handlePostFlop(observation)
        if stage == Stage.TURN:
            return self.handleTurn(observation)
        return self.handleRiver(observation)

    def handlePreFlop(self, observation: Observation) -> Action:
        # get my hand's percent value (how good is this 2 card hand out of all possible 2 card hands)
        handPercent, _ = getHandPercent(observation.myHand)
        handType, cards = getHandType(observation.myHand)
        # if my hand is top 20 percent: raise
        
        if handPercent < .20:
            return Action.RAISE
        # if my hand is top 60 percent: call
        elif handPercent < .70:
            return Action.CALL
        # else fold
        return Action.FOLD

    def handlePostFlop(self, observation: Observation) -> Action:
        # get my hand's percent value (how good is the best 5 card hand i can make out of all possible 5 card hands)
        handPercent, cards = getHandPercent(
            observation.myHand, observation.boardCards)
        handType = getHandType(observation.myHand)
        handBoardType = getHandType(observation.myHand, observation.boardCards)

        # if my hand is top 30 percent: raise
        if handPercent <= .30 and handType != handBoardType:
            return Action.RAISE
        # if my hand is top 80 percent: call
        elif handPercent <= .60:
            return Action.CALL
        # else fold
        straight, _, _ = getLongestStraight(observation.myHand, observation.boardCards)
        if straight == 4:
            return Action.CALL
        flush, _, _ = getLongestStraight(observation.myHand, observation.boardCards)
        if flush == 4:
            return Action.CALL
        return Action.FOLD

    def handleTurn(self, observation: Observation) -> Action:
        # get my hand's percent value (how good is the best 5 card hand i can make out of all possible 5 card hands)
        handPercent, cards = getHandPercent(
            observation.myHand, observation.boardCards)
        # if my hand is top 30 percent: raise
        handType = getHandType(observation.myHand)
        handBoardType = getHandType(observation.myHand, observation.boardCards)
        # if my hand is top 30 percent: raise
        if handPercent <= .30 and handType != handBoardType:
            return Action.RAISE
        # if my hand is top 80 percent: call
        elif handPercent <= .80 and handType != handBoardType:
            return Action.CALL
        # else fold
        straight, _, _ = getLongestStraight(observation.myHand, observation.boardCards)
        if straight == 4:
            return Action.CALL
        flush, _, _ = getLongestStraight(observation.myHand, observation.boardCards)
        if flush == 4:
            return Action.CALL
        return Action.FOLD

    def handleRiver(self, observation: Observation) -> Action:
        # get my hand's percent value (how good is the best 5 card hand i can make out of all possible 5 card hands)
        handPercent, cards = getHandPercent(
            observation.myHand, observation.boardCards)
        # if my hand is top 30 percent: raise
        handType = getHandType(observation.myHand)
        handBoardType = getHandType(observation.myHand, observation.boardCards)
        if handPercent <= .30 and handType != handBoardType:
            return Action.RAISE
        # if my hand is top 80 percent: call
        elif handPercent <= .80 and handType != handBoardType:
            return Action.CALL
        # else fold
        elif observation.totalPot > 300:
            return Action.CALL
        return Action.FOLD


    def opponentNotRaise(self, observation: Observation) -> bool:
        if observation.myPosition == 0:
            opponent = 1
        else: 
            opponent = 0
        return not observation.players[opponent].history[observation.stage-1] == Action.RAISE

    def opponentNotDoubleRaise(self, observation: Observation) -> bool:
        if observation.myPosition == 0:
            opponent = 1
        else: 
            opponent = 0
        return not observation.players[opponent].history[observation.stage-1] == Action.RAISE and observation.players[opponent].history[observation.stage-2] == Action.RAISE