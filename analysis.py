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

def download_data(symbol):
    now = int(time.time())
    year_ago = now - (365*24*60*60)

    u = f"https://api.coingecko.com/api/v3/coins/{symbol}/market_chart/range?vs_currency=usd&from={year_ago}&to={now}"
    r = requests.get(u)
    raw_data = r.json()
    p=raw_data["prices"]
    return p

name1 = "kyber-network"
data1 = download_data(name1)

name2 = "usd-coin"
data2 = download_data(name2)

ratios = list(map(find_ratio, data1, data2))

max = max(ratios)
min = min(ratios)
max_deviation = max/min

pyplot.subplot(1, 2, 1)
pyplot.plot(ratios)
pyplot.xlabel("time")
pyplot.ylabel(name1 + "/" + name2 + " ratio")
pyplot.text(0.3, 0.9, "max deviation:" + str(max_deviation), transform=pyplot.gcf().transFigure)

pyplot.subplot(1, 2, 2)
deviations = [0, 1, 2, 3, 4]
pyplot.xlabel("proportion to min")

pyplot.plot(deviations)

pyplot.show()

# with open(get_filename(symbol), 'w') as outfile:
#     json.dump(p, outfile)
# check if files exists. if not, download
# try:
#     f1 = open(file1)
# except:
#     download_data(name1)
# def check_or_download(name):
#     return True
# check_or_download(name2)
# file2 = f"data/{name2}.json"
# with open(file1) as json_file:
#     data1 = json.load(json_file)

# with open(file2) as json_file:
#     name2 = "eth"
#     data2 = json.load(json_file)
