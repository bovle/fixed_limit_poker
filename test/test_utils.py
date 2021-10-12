from unittest import TestCase
from utils.handValue import getHandPercent


class TestUtils(TestCase):
    def testPercentValueBestHand(self):
        hand = ['As', 'Ah']
        val = getHandPercent(hand)
        self.assertEqual(val, 0)

    def testPercentValueWorstHand(self):
        hand = ['3s', '2c']
        val = getHandPercent(hand)
        self.assertEqual(val, 100)
