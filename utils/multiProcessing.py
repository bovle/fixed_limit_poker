import queue
import multiprocessing as mp
from time import sleep
from typing import List

def worker(func, jobQueue: mp.Queue, stopSignal: mp.Queue, doneSignals: mp.Queue, results: mp.Queue):
    while stopSignal.empty():
        
        while not jobQueue.empty():
            try:
                args = jobQueue.get(block=False)
            except queue.Empty:
                break
            results.put(func(*args))
            doneSignals.put("done")

class Controller:

    def __init__(self, processCount, func):
        self.manager = mp.Manager()
        self.results = mp.Queue()
        self.jobs = mp.Queue()
        self.stopSignal = mp.Queue()
        self.doneSignals = mp.Queue()
        self.processCount = processCount
        
        self.processes = []
        for _ in range(processCount):
            p = mp.Process(target=worker, args=(func, self.jobs, self.stopSignal, self.doneSignals, self.results))
            self.processes.append(p)
            p.start()
    
    def addJobs(self, argses):
        self.jobCount = len(argses)
        for args in argses:
            self.jobs.put(args)

    def waitForJobsFinish(self):
        for _ in range(self.jobCount):
            self.doneSignals.get()
    
    def getResults(self):
        res = []
        while not self.results.empty():
            res.append(self.results.get())
        return res
    
    def joinAll(self):
        self.stopSignal.put("stop")
        for p in self.processes:
            p.join()

