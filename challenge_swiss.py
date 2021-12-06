from collections import Counter, defaultdict
import itertools
import math
import multiprocessing as mp
from os import name
import queue
import time
from random import shuffle
from typing import List

import pandas as pd

from bots import CounterBot, PercentBot
from bots.BotInterface import BotInterface
from environment.FixedLimitPoker import FixedLimitPoker
from environment.Deck import Deck
from bots.tournament_bots.round_6 import abots, ANLI, BotimusPrime, FalBot, Spooky, Mobot, IdaBot
from bots.tournament_bots.round_2 import abots as abots_old, ANLI as anli_old, BotimusPrime as bp_old, FalBot as falbot_old, Spooky as spooky_old, Mobot as mobot_old, IdaBot as idabot_old
from utils.multiProcessing import Controller

BOT_CLASSES: List[BotInterface] = [
    abots.Abots,
    ANLI.ANLI,
    BotimusPrime.BotimusPrime,
    FalBot.FalBot,
    Spooky.SpookyBot,
    Mobot.Mobot,
    IdaBot.IdaBOT,
    abots_old.Abots,
    anli_old.ANLI,
    bp_old.BotimusPrime,
    falbot_old.FalBot,
    spooky_old.SpookyBot,
    mobot_old.Mobot,
    idabot_old.IdaBOT
]
PARTICIPANTS = []

TOTAL_ROUNDS = 1000
PROCESS_COUNT = mp.cpu_count() - 2
TIMESTAMP = round(time.time())


def play(bots, roundsPerRoom: int, hands: List[List[str]]):
    room = FixedLimitPoker(bots)
    p1name = room.players[0].bot.name
    p2name = room.players[1].bot.name
    res = defaultdict(int)
    for i in range(roundsPerRoom):
        room.reset(rotatePlayers=True, stackedDeck=hands[i])
        p1 = room.players[0]
        p2 = room.players[1]
        res[p1.bot.name] += p1.reward
        res[p2.bot.name] += p2.reward

    handIdx = -1
    while(res[p1name] == res[p2name]):
        room.reset(rotatePlayers=True, stackedDeck=hands[handIdx])
        p1 = room.players[0]
        p2 = room.players[1]
        res[p1.bot.name] += p1.reward
        res[p2.bot.name] += p2.reward
        handIdx -= 1

    return res


def deduplicate_player_names():
    for idx, p in enumerate(PARTICIPANTS):
        player_player_names = [n.name for n in PARTICIPANTS]
        while player_player_names.count(p.name) > 1:
            print(f"Renaming player '{p.name}'")
            p.name += f"-{idx}"
            player_player_names = [n.name for n in PARTICIPANTS]


def main():
    for bot_class in BOT_CLASSES:
        PARTICIPANTS.append(bot_class())
        PARTICIPANTS.append(bot_class())
        PARTICIPANTS.append(bot_class())
        PARTICIPANTS.append(bot_class())
        PARTICIPANTS.append(bot_class())
        PARTICIPANTS.append(bot_class())

    shuffle(PARTICIPANTS)
    print(len(PARTICIPANTS))
    deduplicate_player_names()
    combinations = list(itertools.combinations(PARTICIPANTS, 2))
    
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
    byes = []
    points = defaultdict(int)
    score = defaultdict(int)
    
    controller = Controller(PROCESS_COUNT, play)

    jobs = []
    start_time = time.time()
    for c in combinations:
        jobs.append([[c[0], c[1]], rounds_for_each_pair, hands])
    controller.addJobs(jobs)
    controller.waitForJobsFinish()
    results = controller.getResults()
    for res in results:
        for name in res:
            points[name] += 1 if res[name] > 0 else 0
            score[name] += res[name]
    duration = time.time() - start_time
    print(duration)
    print([(x,points[x], score[x]) for x in sorted(points, key=lambda key: (points[key], score[key]), reverse=True)])
    print() 

    start_time = time.time()
    for i in range(2):
        byes = []
        points = {}
        score = {}
        matchups = defaultdict(int)
        for bot in PARTICIPANTS:
            points[bot.name] = 0
            score[bot.name] = 0
        
        roundCount =  math.ceil(len(PARTICIPANTS)/2) if i==1 else math.ceil(math.log2(len(PARTICIPANTS)))+2
        print("round count: " + str(roundCount))
        for round in range(roundCount):
            sortedBots: List = sorted(points, key=lambda key: (points[key], score[key]), reverse=True)
            jobs = []
            if len(sortedBots) % 2 != 0:
                index = len(sortedBots)-1
                while(sortedBots[index] in byes):
                    index -= 1
                byeName = sortedBots.pop(index)
                byes.append(byeName)
                points[byeName] += 1
            while len(sortedBots) != 0:
                bot1Name = sortedBots.pop(0)
                bot2Name = sortedBots.pop(0)
                bot1 = next(x for x in PARTICIPANTS if x.name == bot1Name) 
                bot2 = next(x for x in PARTICIPANTS if x.name == bot2Name)
                jobs.append([[bot1, bot2], rounds_for_each_pair, hands])
                
            controller.addJobs(jobs)
            controller.waitForJobsFinish()
            results = controller.getResults()
            for res in results:
                matchups['_'.join(sorted(res.keys()))] += 1
                for name in res:
                    points[name] += 1 if res[name] > 0 else 0
                    score[name] += res[name]
        duration = time.time() - start_time
        print(duration)
        print([(x,points[x], score[x]) for x in sorted(points, key=lambda key: (points[key], score[key]), reverse=True)])
        start_time = time.time()
    print()
    controller.joinAll()

    duration = time.time() - start_time
    print(duration)
    
    return points


if __name__ == '__main__':
    main()
