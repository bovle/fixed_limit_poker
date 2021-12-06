import itertools
import math
import multiprocessing as mp
import queue
import time
from random import randint
from typing import List

import pandas as pd

from environment.Deck import Deck
from bots import CounterBot, PercentBot
from bots.BotInterface import BotInterface
from environment.FixedLimitPoker import FixedLimitPoker
from bots.tournament_bots.round_6 import abots, ANLI, BotimusPrime, FalBot, Spooky, Mobot, IdaBot

PARTICIPANTS: List[BotInterface] = [
    abots.Abots(),
    ANLI.ANLI(),
    BotimusPrime.BotimusPrime(),
    FalBot.FalBot(),
    Spooky.SpookyBot(),
    Mobot.Mobot(),
    IdaBot.IdaBOT(),
    abots.Abots(),
    ANLI.ANLI(),
    BotimusPrime.BotimusPrime(),
    FalBot.FalBot(),
    Spooky.SpookyBot(),
    Mobot.Mobot(),
    IdaBot.IdaBOT(),
    abots.Abots(),
    ANLI.ANLI(),
    BotimusPrime.BotimusPrime(),
    FalBot.FalBot(),
    Spooky.SpookyBot(),
    Mobot.Mobot(),
    IdaBot.IdaBOT(),
    abots.Abots(),
    ANLI.ANLI(),
    BotimusPrime.BotimusPrime(),
    FalBot.FalBot(),
    Spooky.SpookyBot(),
    Mobot.Mobot(),
    IdaBot.IdaBOT()
]
TOTAL_ROUNDS = 1000
PROCESS_COUNT = mp.cpu_count() - 2
TIMESTAMP = round(time.time())


def play(jobQueue: mp.Queue, roundsPerRoom: int, hands: List[List[str]], stats):
    while not jobQueue.empty():
        try:
            c = jobQueue.get(block=False)
        except queue.Empty:
            break
        room = FixedLimitPoker(c)
        for i in range(roundsPerRoom):
            room.reset(rotatePlayers=True,stackedDeck=hands[i])
            p1 = room.players[0]
            p2 = room.players[1]
            k1 = (p1.bot.name, p2.bot.name)
            if k1 not in stats:
                stats[k1] = 0
            stats[k1] += p1.reward
            k2 = (p2.bot.name, p1.bot.name)
            if k2 not in stats:
                stats[k2] = 0
            stats[k2] += p2.reward


def deduplicate_player_names():
    for idx, p in enumerate(PARTICIPANTS):
        player_player_names = [n.name for n in PARTICIPANTS]
        while player_player_names.count(p.name) > 1:
            print(f"Renaming player '{p.name}'")
            p.name += f"-{idx}"
            player_player_names = [n.name for n in PARTICIPANTS]


def main():
    deduplicate_player_names()
    combinations = list(itertools.combinations(PARTICIPANTS, 2))
    rounds_for_each_pair = 100# math.floor(TOTAL_ROUNDS / len(combinations))
    start_time = time.time()
    hands: List[List[str]] = []
    for _ in range(int((rounds_for_each_pair+1)/2)):
        deck = Deck()
        hand1 = deck.drawMultiple(2)
        hand2 = deck.drawMultiple(2)
        board = deck.drawMultiple(5)
        hands.append(hand1 + hand2 + board)
        hands.append(hand1 + hand2 + board)
    print(f"There are {len(combinations)} combinations")
    print(f"Each combination will be played: {rounds_for_each_pair} times")

    manager = mp.Manager()
    stats = manager.dict()
    jobs = mp.Queue()
    for c in combinations:
        jobs.put(c)

    processes = []
    for _ in range(PROCESS_COUNT):
        p = mp.Process(target=play, args=(jobs, rounds_for_each_pair, hands, stats))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
    duration = time.time() - start_time
    print(duration)
    cols = [x.name for x in PARTICIPANTS]
    res = pd.DataFrame(0, columns=cols, index=cols + ["sum", "pr. round"])
    for key in stats.keys():
        res[key[0]]["sum"] += stats[key]
        res[key[0]][key[1]] = stats[key]

    for c in cols:
        res[c]["pr. round"] = round(
            res[c]["sum"] / (rounds_for_each_pair * (len(PARTICIPANTS) - 1)), 3)

    print(res)

    
    rounds = rounds_for_each_pair * len(combinations)
    duration_pr_sim = round(duration/rounds, 5)
    print(f"-----------------------------------------")
    print(f"Simulation took {duration_pr_sim} seconds pr. round")
    print(f"Using {PROCESS_COUNT} processes")
    print(f"--- {round(duration, 2)} seconds ---")

    # with open(f"./results/challenge-{TIMESTAMP}.csv", 'wb') as file:
    #     res.to_csv(file)
    #     print("Wrote to file ...")
    return res


if __name__ == '__main__':
    main()
