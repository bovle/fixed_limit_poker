from unittest import TestCase
from environment.Constants import SUITS, HandType
from utils import handValue


class TestUtils(TestCase):

    def testPercentValues(self):
        hand = ['As', 'Ah']
        val, _ = handValue.getHandPercent(hand)
        self.assertLess(val, 0.1)
        hand = ['3s', '2h']
        val, _ = handValue.getHandPercent(hand)
        self.assertEqual(val, 1)

    def testHandTypePreFlop(self):
        hand = ['7s', 'Ah']
        handType, cards = handValue.getHandType(hand)
        self.assertEqual('A7o', handType)
        hand = ['Ac', '2h']
        handType, cards = handValue.getHandType(hand)
        self.assertEqual('A2o', handType)
        print()
        hand = ['4h', 'Ah']
        handType, cards = handValue.getHandType(hand)
        self.assertEqual('A4s', handType)
        hand = ['Ac', 'Ah']
        handType, cards = handValue.getHandType(hand)
        self.assertEqual('AA', handType)

    def testHandTypePostFlop(self):
        board = ['As', '3s', 'Kh', '2d', 'Kc']
        hand = ['7s', 'Ah']
        handType, cards = handValue.getHandType(hand, board)
        self.assertEqual(HandType.TWOPAIR, handType)
        board = ['5s', '3s', 'Kh', '2d', 'Kc']
        hand = ['4s', 'Ah']
        handType, cards = handValue.getHandType(hand, board)
        self.assertEqual(HandType.STRAIGHT, handType)
        board = ['As', '3s', 'Kh', '2d', 'Kc']
        hand = ['Ac', 'Ah']
        handType, cards = handValue.getHandType(hand, board)
        self.assertEqual(HandType.FULLHOUSE, handType)
        print()

    def testStraightCount(self):
        board = ['As', '3s', 'Kh', '2d', 'Kc']
        hand = ['7s', 'Ah']
        count, startRank, endRank = handValue.getLongestStraight(hand, board)
        self.assertEqual(count, 3)
        self.assertEqual(startRank, 'A')
        self.assertEqual(endRank, '3')
        board = ['As', '3s', 'Kh', '2d', 'Qc']
        hand = ['Js', 'Ah']
        count, startRank, endRank = handValue.getLongestStraight(hand, board)
        self.assertEqual(count, 4)
        self.assertEqual(startRank, 'J')
        self.assertEqual(endRank, 'A')
        board = ['As', '3s', 'Kh', '4d', 'Qc']
        hand = ['Js', 'Ah']
        count, startRank, endRank = handValue.getLongestStraight([], board)
        self.assertEqual(count, 3)
        self.assertEqual(startRank, 'Q')
        self.assertEqual(endRank, 'A')
        print()

    def testSuitCount(self):
        board = ['As', '3s', 'Kh', '2d', 'Kc']
        hand = ['7s', 'Ah']
        count, suit = handValue.getHighestSuitCount(hand, board)
        self.assertEqual(count, 3)
        self.assertEqual(suit, 's')
        count, suit = handValue.getHighestSuitCount([], board)
        self.assertEqual(count, 2)
        self.assertEqual(suit, 's')

    def testBoardHandType(self):
        board = ['As', '3s', 'Kh']
        val = handValue.getBoardHandType(board)
        self.assertEqual(val, HandType.HIGHCARD)
        board = ['As', '3s', 'Kh', '2s']
        val = handValue.getBoardHandType(board)
        self.assertEqual(val, HandType.HIGHCARD)
        board = ['As', 'As', 'Kh']
        val = handValue.getBoardHandType(board)
        self.assertEqual(val, HandType.PAIR)
        board = ['As', 'As', 'Kh', '2s']
        val = handValue.getBoardHandType(board)
        self.assertEqual(val, HandType.PAIR)
        board = ['As', 'As', 'Kh', 'Kc']
        val = handValue.getBoardHandType(board)
        self.assertEqual(val, HandType.TWOPAIR)
        board = ['As', 'As', 'Ah']
        val = handValue.getBoardHandType(board)
        self.assertEqual(val, HandType.THREEOFAKIND)
        board = ['As', 'As', 'Ah', 'Kc']
        val = handValue.getBoardHandType(board)
        self.assertEqual(val, HandType.THREEOFAKIND)
        board = ['As', 'As', 'Ah', 'Ac']
        val = handValue.getBoardHandType(board)
        self.assertEqual(val, HandType.FOUROFAKIND)
        print()

    def testLazyPercent(self):
        hand = ["7h", "Kh"]
        community = ["Qh", "Jh", "Th", "9h", "8h"]
        lazyValue, lazyCards = handValue.lazyGetHandPercent(hand, community)
        value, cards = handValue.getHandPercent(hand, community)
        self.assertEqual(lazyValue, value)
        self.assertSequenceEqual(lazyCards, cards)
        print(value)
        print(cards)
