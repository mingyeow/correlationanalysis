import json
import requests

from numpy import mean
from numpy import std
from matplotlib import pyplot

def find_ratio(r1, r2):
    return float(r1["rate"])/float(r2["rate"])

# def download_data(symbol):
#     symbol = "XRP"
#     curl -X GET "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range?vs_currency=usd&from=1592875879&to=1612875879" -H "accept: application/json"
#     u = f"https://api.nomics.com/v1/exchange-rates/history?key=4f218abd568f894f4c75035587645792&currency={symbol}&start=2020-01-01T00%3A00%3A00Z&end=2021-02-01T00%3A00%3A00Z"
#     r = requests.get(u)
# check if files exists. if not, download
# try:
#     f1 = open(file1)
# except:
#     download_data(name1)

def check_or_download(name):
    return True

name1 = "btc"
check_or_download(name1)
file1 = f"data/{name1}.json"

name2 = "eth"
check_or_download(name2)
file2 = f"data/{name2}.json"

with open(file1) as json_file:
    data1 = json.load(json_file)

with open(file2) as json_file:
    name2 = "eth"
    data2 = json.load(json_file)


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