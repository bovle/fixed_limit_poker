from asyncio.tasks import sleep
import pickle
import json
from os import listdir
from os.path import isfile, join
import threading
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

import asyncio
import websockets


class WebsocketWorker(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.connected = set()
        self.connectedProgress = dict()
        self.results = []
        self.stopFlag = False

    def load_file(self, path):
        with open(path, "rb") as f:
            self.results.append(json.loads(pickle.load(f)))

    def run(self):
        while not self.stopFlag:
            for ws in list(self.connectedProgress.keys()).copy():
                while ws in self.connectedProgress and self.connectedProgress[ws] < len(self.results):
                    to_send = self.results[self.connectedProgress[ws]]
                    try:
                        coro = ws.send(json.dumps(to_send))
                        future = asyncio.run_coroutine_threadsafe(coro, loop)
                        future.result()
                        self.connectedProgress[ws] += 1
                    except websockets.exceptions.ConnectionClosedError as ex:
                        print("Error in websocket: ", ex)
                        del self.connectedProgress[ws]

            time.sleep(2)

    async def handler(self, websocket, path):
        self.connected.add(websocket)
        self.connectedProgress[websocket] = 0
        try:
            while True:
                await sleep(1)
        except websockets.exceptions.ConnectionClosed:
            print("connection closed?!")
        finally:
            self.connected.remove(websocket)


def on_modified(event):
    print(f"{event.src_path} has been created!")
    time.sleep(0.1)
    worker.load_file(event.src_path)


if __name__ == "__main__":
    worker = WebsocketWorker()

    results_dir = "./results/"
    onlyfiles = [join(results_dir, f)
                 for f in listdir(results_dir) if isfile(join(results_dir, f)) and f.endswith(".pckl")]

    for fp in onlyfiles:
        worker.load_file(fp)

    my_event_handler = PatternMatchingEventHandler()
    my_event_handler.on_modified = on_modified
    observer = Observer()
    observer.schedule(my_event_handler, results_dir, recursive=True)
    observer.daemon = True
    observer.start()

    worker.daemon = True
    worker.start()

    try:
        ws_server = websockets.serve(worker.handler, '0.0.0.0', 8765)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(ws_server)
        loop.run_forever()
    except KeyboardInterrupt:
        worker.stopFlag = True
    finally:
        observer.stop()
        observer.join()
