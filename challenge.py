from collections import defaultdict
from json.encoder import JSONEncoder
import pickle
import queue
from typing import Dict
from environment.FixedLimitPoker import FixedLimitPoker
from bots import Example1Bot, MirrorBot, RandomBot, CallBot, FoldBot
import itertools
import math
import time
import json
import multiprocessing as mp

PARTICIPANTS = [Example1Bot("player1"), Example1Bot("player2"), Example1Bot("player3"), Example1Bot("player4"), Example1Bot("player5")]
TOTAL_ROUNDS = 1000


class ChallengeResult:
    stats: Dict[str, int]
    timestamp: int
    iterations: int

    def __init__(self, stats, timestamp, iterations) -> None:
        self.stats = stats
        self.timestamp = timestamp
        self.iterations = iterations


class ChallengeResultEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


def play(jobQueue: mp.Queue, roundsPerRoom: int, stats):
    while not jobQueue.empty():
        try:
            c = jobQueue.get(block=False)
        except queue.Empty:
            break
        room = FixedLimitPoker(c)
        for _ in range(roundsPerRoom):
            room.reset(rotatePlayers=True)
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

def main():
    combinations = list(itertools.combinations(PARTICIPANTS, 2))
    rounds_for_each_pair = math.floor(TOTAL_ROUNDS / len(combinations))

    print(f"There are {len(combinations)} combinations")
    print(f"Each combination will be played: {rounds_for_each_pair} times")

    start_time = time.time()
    manager = mp.Manager()
    stats = manager.dict()
    jobs = mp.Queue()
    for c in combinations:
        jobs.put(c)

    processes = []
    for _ in range(mp.cpu_count() - 2):
        p = mp.Process(target=play, args=(jobs,rounds_for_each_pair,stats))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    res = defaultdict(dict)
    for key in stats.keys():
        if "sum" not in res[key[0]]:
            res[key[0]]["sum"] = 0
        res[key[0]]["sum"] += stats[key]
        res[key[0]][key[1]] = stats[key]
    
    duration = time.time() - start_time
    rounds = rounds_for_each_pair * len(combinations)
    duration_pr_sim = round(duration/rounds, 5)
    print(f"-----------------------------------------")
    print(f"Simulation took {duration_pr_sim} seconds pr. round")
    print(f"--- {round(duration, 2)} seconds ---")
    
    timestamp = round(time.time())
    with open(f"./results/challenge-{timestamp}-{'-'.join(p.name for p in PARTICIPANTS)}.pckl", 'wb') as file:
        challenge_result = ChallengeResult(res, timestamp, rounds)
        results_as_json = json.dumps(
            challenge_result, cls=ChallengeResultEncoder)
        pickle.dump(results_as_json, file)


if __name__ == '__main__':
    main()
