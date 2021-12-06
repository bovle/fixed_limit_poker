import pickle
import time
from environment.deuces.evaluator import Evaluator
from environment.deuces.card import Card


RANKS = sorted('23456789TJQKA')
SUITS = sorted('cdhs')

start_time = time.time()


def all_combinations(list1, list2):
    for i1 in list1:
        for i2 in list2:
            yield f"{i1}{i2}"


def main():
    c = Card()
    combs = list([c.new(card) for card in all_combinations(RANKS, SUITS)])
    eval = Evaluator()
    res = dict()

    for i1 in range(0, 48):
        print(f"i1: {i1}")
        for i2 in range(i1 + 1, 49):
            for i3 in range(i2 + 1, 50):
                for i4 in range(i3 + 1, 51):
                    for i5 in range(i4 + 1, 52):
                        deck = [combs[i1], combs[i2],
                                combs[i3], combs[i4], combs[i5]]
                        res[tuple(deck)], _ = eval.evaluate(deck, [])

    print("--- Total time: %s seconds ---" % (time.time() - start_time))
    with open("./utils/allhandranks.pckl", 'wb') as f:
        pickle.dump(res, f)
    print(len(res))
    # There are 2598960 unique poker hands ...
    assert len(res) == 2598960


if __name__ == "__main__":
    main()
