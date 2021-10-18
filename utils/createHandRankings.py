list = ["AA","KK","QQ","JJ","TT","99","88","AKs","AQs","AKo","77","AJs","ATs","AQo","KQs","AJo","KJs","A9s","66","KTs","ATo","A8s","KQo","A7s","QJs","KJo","K9s","A9o","55","QTs","A6s","A5s","A8o","A4s","KTo","K8s","Q9s","QJo","A7o","A3s","JTs","K7s","A2s","44","K9o","QTo","K6s","A5o","A6o","Q8s","K5s","J9s","A4o","K8o","Q9o","K4s","A3o","JTo","Q7s","33","K7o","J8s","T9s","A2o","K3s","Q6s","K2s","K6o","Q8o","Q5s","J9o","K5o","J7s","T8s","Q4s","K4o","Q3s","22","98s","T9o","Q7o","T7s","J6s","J8o","K3o","Q2s","Q6o","J5s","K2o","Q5o","T8o","J7o","J4s","97s","T6s","J3s","Q4o","87s","J2s","T5s","96s","98o","J6o","Q3o","T7o","T4s","Q2o","J5o","86s","T3s","95s","97o","T6o","T2s","J4o","76s","85s","J3o","94s","87o","75s","J2o","T5o","93s","96o","92s","84s","65s","T4o","86o","T3o","74s","95o","83s","64s","76o","54s","T2o","82s","73s","85o","94o","53s","63s","75o","93o","72s","65o","84o","43s","92o","62s","52s","74o","42s","83o","54o","64o","32s","82o","73o","53o","63o","43o","72o","52o","62o","42o","32o"]

count = 0
res = {}
for hand in list:
    if len(hand) == 2:
        count += 6
    elif hand[2] == "s":
        count += 4
    elif hand[2] == "o":
        count += 12
    res[hand] = (count/1326)

import pickle

dbfile = open("./utils/preflopHandRankings.pckl", 'ab')
pickle.dump(res, dbfile)
dbfile.close()
print()