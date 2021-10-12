import pickle
from typing import Dict, List, Sequence
from collections import defaultdict
from environment.Constants import RANKS, HandType
from utils.deuces.card import Card
from utils.deuces.evaluator import Evaluator



def _getPreflopHandType(hand: Sequence[str]) -> str:
    """
    Translate from list of cards i.e. ['Ac', 'As'] to 'AA', or ['2c', 3s'] to '32o' (off suit), or ['2c', '3c'] to '32s'
    """
    hand = sorted(hand, key=lambda x: RANKS.index(x[0]), reverse=True)

    if hand[0][0] == hand[1][0]:
        return hand[0][0] + hand[1][0]
    elif hand[0][1] == hand[1][1]:
        return hand[0][0] + hand[1][0] + 's'
    else:
        return hand[0][0] + hand[1][0] + 'o'

def getHandPercent(hand: Sequence[str], board: Sequence[str] = []) -> float:
    if len(board) == 0:
        with open('./utils/preflopHandRankings.pckl', 'rb') as rankingsFile:
            rankings = pickle.load(rankingsFile)
            preflopHandType = _getPreflopHandType(hand)
            return rankings[preflopHandType]
    else:
        evaluator = Evaluator()
        d_hand = [Card().new(c) for c in hand]
        d_board = [Card().new(c) for c in board]
        rank = evaluator.evaluate(d_hand, d_board)
        percentage = evaluator.get_five_card_rank_percentage(rank)  # higher better here
        return percentage * 100


def getHandType(hand: List[str], board: List[str] = []):
    if len(board) == 0:
        return _getPreflopHandType(hand)
    else:    
        d_hand = [Card().new(c) for c in hand]
        d_board = [Card().new(c) for c in board]
        evaluator = Evaluator()
        return HandType(evaluator.get_rank_class(evaluator.evaluate(d_hand, d_board)))

def getLongestStraight(hand: List[str], board: List[str] = []):
    cardRanks = [RANKS.index(c[0]) for c in hand + board]
    if RANKS.index('A') in cardRanks:
        cardRanks.append(-1) # add low ace
    cardRanksSet = set(cardRanks)

    ans = 0
    startRank = 0
    for rank in cardRanksSet:  
        j = rank + 1

        while j in cardRanksSet:
            j = j + 1

        if j - rank > ans:
            ans = j - rank
            startRank = rank
    
    if startRank == -1:
        return ans, "A", RANKS[startRank + ans - 1]
    return ans, RANKS[startRank], RANKS[startRank + ans - 1]

def getHighestSuitCount(hand: List[str], board: List[str] = []):
    suitCounts: Dict[str, int] = defaultdict(lambda: 0)
    for c in hand + board:
        suitCounts[c[1]] += 1
    maxSuit = max(suitCounts, key=suitCounts.get)
    return suitCounts[maxSuit], maxSuit