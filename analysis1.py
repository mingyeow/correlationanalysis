import json
import requests

from numpy import mean
from numpy import std
from matplotlib import pyplot

def find_ratio(r1, r2):
    return float(r1["rate"])/float(r2["rate"])

def find_coin_id(symbol):    
    with open("coinlist.json") as json_file:
        data1 = json.load(json_file
    for x in data1:
        if x["symbol"] == "knc":
            return x["id"]

# get id and data for first coin
name1 = "btc"
id1 = find_coin_id(name1)

# get id and data for second coin
name2 = "eth"
id2 = find_coin_id(name2)

result = map(find_ratio, data1, data2)

ratios = list(result)

pyplot.plot(ratios)

max = max(ratios)
min = min(ratios)
ratio_deviation = max/min

pyplot.xlabel("time")
pyplot.ylabel(name1 + "/" + name2 + " ratio")
pyplot.text(0.3, 0.9, "max deviation:" + str(max/min), transform=pyplot.gcf().transFigure)

pyplot.show()