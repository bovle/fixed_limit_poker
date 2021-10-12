from unittest import TestCase
from utils import handValue

class TestUtils(TestCase):

    def testPercentValueAces(self):
        hand = ['As', 'Ah']
        val = handValue.getHandPercent(hand)
        self.assertTrue(val < 1)
