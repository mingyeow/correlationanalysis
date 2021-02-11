#write max supported amplification
# plot out max deviation

import json
import requests
import time

from numpy import mean
from numpy import std
from matplotlib import pyplot

def get_filename(symbol):
    return f'{symbol}.json'

def find_ratio(r1, r2):
    assert (r1[0] == r2[0])
    return float(r1[1])/float(r2[1])

def find_devitation(r, min_r):
    return r/min_r

def find_recommended_amp(d):
    x = d/(1-d)
    return (x+x**2)**0.5 -x

def download_data(symbol):
    now = int(time.time())
    year_ago = now - (365*24*60*60)

    u = f"https://api.coingecko.com/api/v3/coins/{symbol}/market_chart/range?vs_currency=usd&from={year_ago}&to={now}"
    r = requests.get(u)
    raw_data = r.json()
    p=raw_data["prices"]
    return p

def find_coin_id(symbol):    
    with open("coinlist.json") as json_file:
        data1 = json.load(json_file)
    for x in data1:
        if x["symbol"] == symbol:
            return x["id"]


# get id and data for first coin
name1 = input("First Symbol? ")
id1 = find_coin_id(name1)

name2 = input("Second Symbol? ")
id2 = find_coin_id(name2)

#  get data
data1 = download_data(id1)
data2 = download_data(id2)

# create the ratios
ratios = list(map(find_ratio, data1, data2))

# get min/max and max_deviations
max = max(ratios)
min = min(ratios)

max_deviation = max/min
recommended_amp = find_recommended_amp(max_deviation)
standard_deviation = std(ratios)

#get the ratios
ratio_deriatives = list(map(lambda r: r/min, ratios))

pyplot.text(0.12, 0.95, f"pair: {name1} / {name2}" , transform=pyplot.gcf().transFigure)
pyplot.text(0.12, 0.9, f"max ratio/min ratio: {'{:.4f}'.format(max_deviation)}" , transform=pyplot.gcf().transFigure)
pyplot.text(0.5, 0.95, f"max amp to cater: {'{:.4f}'.format(recommended_amp)}" , transform=pyplot.gcf().transFigure)
pyplot.text(0.5, 0.9, f"standard deviation: {'{:.4f}'.format(std(ratios))}" , transform=pyplot.gcf().transFigure)

# plot the ratios
pyplot.plot(ratios)
pyplot.xlabel("last year")
pyplot.ylabel(name1 + "/" + name2 + " ratio")
pyplot.show()