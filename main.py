import time
start_time = time.time()

from utils.handValue import _getHandPercent, _getHandType, _getPreflopHandType, _getBoardHandType, _getHighestSuitCount, _getLongestStraight
from environment.observers.LoggingObserver import LoggingObserver
from environment.FixedLimitPoker import FixedLimitPoker
from bots import CounterBot, PercentBot, TemplateBot
import itertools


def debug():
    observers = [LoggingObserver()]
    env = FixedLimitPoker([
        # Change the bots here to change the participants
        PercentBot(),
        TemplateBot()
    ], observers=observers, punishSlowBots=False)
    env.reset()
    env.reset(rotatePlayers=True)


def benchmark():
    bots = [
        # Change the bots here to change the participants
        CounterBot(),
        PercentBot(),
        # TemplateBot(),
    ]
    combinations = list(itertools.combinations(bots, 2))
    roundsPerPair = 1000
    cols = [x.name for x in bots]
    # Import only pandas if we need to, since it's slow.
    from pandas import DataFrame
    stats = DataFrame(0, columns=cols, index=cols + ["sum", "pr. round"])
    for c in combinations:
        room = FixedLimitPoker(c, punishSlowBots=False)
        for _ in range(roundsPerPair):
            room.reset(rotatePlayers=True)
            p1 = room.players[0]
            p2 = room.players[1]
            stats[p1.bot.name][p2.bot.name] += p1.reward
            stats[p1.bot.name]["sum"] += p1.reward
            stats[p2.bot.name][p1.bot.name] += p2.reward
            stats[p2.bot.name]["sum"] += p2.reward
    for bot in bots:
        stats[bot.name]["pr. round"] = stats[bot.name]["sum"] / \
            (roundsPerPair*(len(bots)-1))
    print(stats)


if __name__ == '__main__':
    benchmark()
    # debug()
    print(f"_getHandPercent: {_getHandPercent.cache_info()}")
    print(f"_getHandType: {_getHandType.cache_info()}")
    print(f"_getPreflopHandType: {_getPreflopHandType.cache_info()}")
    print(f"_getBoardHandType: {_getBoardHandType.cache_info()}")
    print(f"_getHighestSuitCount: {_getHighestSuitCount.cache_info()}")
    print(f"_getLongestStraight: {_getLongestStraight.cache_info()}")
    print("--- Total time: %s seconds ---" % (time.time() - start_time))
