from collections import Counter, defaultdict
import itertools
import math
import multiprocessing as mp
from os import name
import queue
import time
from random import randint
from typing import List
from pprint import pprint
from numpy import mat

import pandas as pd

from bots import CounterBot, PercentBot
from bots.BotInterface import BotInterface
from environment.FixedLimitPoker import FixedLimitPoker
from environment.Deck import Deck
from bots.tournament_bots.round_6 import abots, ANLI, BotimusPrime, FalBot, Spooky, Mobot, IdaBot
from utils.multiProcessing import Controller

PARTICIPANTS: List[BotInterface] = [
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


def play(bots, roundsPerRoom: int, hands: List[List[str]]) -> dict[str, int]:
    room = FixedLimitPoker(bots)
    res = defaultdict(int)
    for i in range(roundsPerRoom):
        room.reset(rotatePlayers=True, stackedDeck=hands[i])
        p1 = room.players[0]
        p2 = room.players[1]
        res[p1.bot.name] += p1.reward
        res[p2.bot.name] += p2.reward

    return res #p1.bot.name if res[p1.bot.name] > res[p2.bot.name] else (p2.bot.name if res[p2.bot.name] > res[p1.bot.name] else None) 


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
    start_time = time.time()
    rounds_for_each_pair = 100 #math.floor(TOTAL_ROUNDS / len(combinations))
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

    matchupsPlayed = defaultdict(lambda: set())
    byes = []
    points = {}
    for p in PARTICIPANTS:
        points[p.name] = 0
    
    controller = Controller(PROCESS_COUNT, play)
        
    for round in range(math.ceil(math.log2(len(PARTICIPANTS)))+1):
        roundMatchups = dict()
        sortedBots: List = sorted(points, key=points.get, reverse=True)
        print(f"----------- round: {round} -------")
        print(sortedBots)
        print(matchupsPlayed)
        print(byes)
        print(points.items())
        jobs = []
        if len(sortedBots) % 2 != 0:
            index = len(sortedBots)-1
            while(sortedBots[index] in byes):
                index -= 1
            byeName = sortedBots.pop(index)
            byes.append(byeName)
            # points[byeName] += 1
        while len(sortedBots) != 0:
            bot1Name = sortedBots.pop(0)
            bot1 = next(x for x in PARTICIPANTS if x.name == bot1Name)

            opponentCandidates = [b for b in sortedBots if b not in matchupsPlayed[bot1Name]]
            if len(opponentCandidates) == 0:
                print(f"Could not find an unplayed opponent for: {bot1Name}")
                opponentCandidates = [sortedBots[0]]

            bot2Name = opponentCandidates.pop()
            sortedBots.remove(bot2Name)

            bot2 = next(x for x in PARTICIPANTS if x.name == bot2Name)
            jobs.append([[bot1, bot2], rounds_for_each_pair, hands])
            matchupsPlayed[bot1Name].add(bot2Name)
            matchupsPlayed[bot2Name].add(bot1Name)
            roundMatchups[bot1Name] = bot2Name
            roundMatchups[bot2Name] = bot1Name
            
        controller.addJobs(jobs)
        controller.waitForJobsFinish()
        results = controller.getResults()
        print(results)
        for res in results:
            for player_name, value in res.items():
                points[player_name] += value

    controller.joinAll()

    duration = time.time() - start_time
    print(duration)
    
    return points


if __name__ == '__main__':
    res = main()
    pprint(res)
