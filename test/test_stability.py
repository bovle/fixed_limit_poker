from bots import StallBot
from environment.Constants import Action
from environment.FixedLimitPoker import FixedLimitPoker
from bots import ExceptionBot, UnitTesterBot
from unittest import TestCase


class TestStability(TestCase):
    def test_no_crash_on_exception(self):
        ut_bot = UnitTesterBot(actions=[Action.RAISE])
        env = FixedLimitPoker(
            [ut_bot, ExceptionBot()])
        _, _, _, isDone = env.reset()
        winner_position = env.getWinnerPositions()[0]
        winner = env.players[winner_position]
        self.assertTrue(
            isDone, "The exception should cause a fold, and other player wins")
        self.assertEqual(ut_bot.name, winner.bot.name,
                         "The non-crashing bot should win.")

    def test_timeout(self):
        ut_bot = UnitTesterBot(actions=[Action.RAISE, Action.FOLD])
        env = FixedLimitPoker(
            [ut_bot, StallBot(stallTime=1)])
        _, _, _, isDone = env.reset()
        winner_position = env.getWinnerPositions()[0]
        winner = env.players[winner_position]
        self.assertTrue(
            isDone, "The exception should cause a fold, and other player wins")
        self.assertEqual(ut_bot.name, winner.bot.name,
                         "The non-crashing bot should win.")
