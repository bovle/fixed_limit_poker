from bots import PercentBot
from environment.FixedLimitPoker import FixedLimitPoker
from environment.observers.JsonObserver import JsonObserver

def main():
    obs = JsonObserver()
    observers = [obs]
    env = FixedLimitPoker(
        [PercentBot("player1"), PercentBot("player2")], observers=observers)
    env.reset()
    env.reset(rotatePlayers=True)
    env.reset(rotatePlayers=True)
    env.reset(rotatePlayers=True)
    res = obs.ToJson(1, "quaters")
    print()

if __name__ == '__main__':
    main()