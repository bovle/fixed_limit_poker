from unittest import TestCase
from utils import handValue

class TestUtils(TestCase):

    def testPercentValueAces(self):
        hand = ['As', 'Ah']
        val, _ = handValue.getHandPercent(hand)
        self.assertTrue(val < .1)

    def testBoardHandType(self):
        board = ['As', 'As', 'Kh', 'Kc']
        val = handValue.getBoardHandType(board)
        print()
