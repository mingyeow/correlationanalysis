# cater to shortest array

import json
import requests
import time
import copy

from numpy import mean
from numpy import std
from numpy import cov
from matplotlib import pyplot
from scipy.stats import spearmanr

days = 365

def get_filename(symbol):
    return f'{symbol}.json'

def find_ratio(r1, r2):
    assert (r1[0] == r2[0])
    return float(r1[1])/float(r2[1])

def get_price(r):
    return float(r[1])

def find_devitation(r, min_r):
    return r/min_r

def find_recommended_amp(d):
    x = d/(1-d)
    return (x+x**2)**0.5 -x

def download_data(symbol):
    now = int(time.time())
    year_ago = now - (days*24*60*60)

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
prices1 = list(map(get_price, data1))

data2 = download_data(id2)
prices2 = list(map(get_price, data2))

# create the ratios
ratios = list(map(find_ratio, data1, data2))

# get min/max and max_deviations
max_ratio = max(ratios)
min_ratio = min(ratios)
mean = mean(ratios)
amplitude = max_ratio/min_ratio
recommended_amp = find_recommended_amp(amplitude)

standard_deviation = std(ratios)
standard_deviation_to_mean = standard_deviation/mean


# trim off outliers
trimmed_ratios = copy.deepcopy(ratios)
trimmed_ratios.remove(max(trimmed_ratios))
trimmed_ratios.remove(max(trimmed_ratios))
trimmed_ratios.remove(min(trimmed_ratios))
trimmed_ratios.remove(min(trimmed_ratios))

trimmed_max =  max(trimmed_ratios)
trimmed_min =  min(trimmed_ratios)
trimmed_amplitude = trimmed_max/trimmed_min
recommended_trimmed_amp = find_recommended_amp(trimmed_amplitude)

higher_max_ratio = max([trimmed_max/1, 1/trimmed_min])
amplitude_from_mean = higher_max_ratio/mean
recommended_amp_assuming_mean_start = find_recommended_amp(amplitude_from_mean)

#get the ratios
ratio_deriatives = list(map(lambda r: r/min_ratio, ratios))
# correlation = cov(data1,  data2)
# corr, _ = spearmanr(prices1, prices2)

print("ALL DATA POINTS")
print(f"max ratio: {max(trimmed_ratios)}")
print(f"min ratio: {min(trimmed_ratios)}")
print(f"amplitude: {amplitude}")
print(f"amplification factor: {recommended_amp}")


print("\n")
print("EXCLUDING ~1%")
print(f"max trimmed ratio: {max(trimmed_ratios)}")
print(f"min trimmed ratio: {min(trimmed_ratios)}")
print(f"amplitude (ex outliers): {trimmed_amplitude}")
print(f"amplification (ex outliers): {recommended_trimmed_amp}")

print("\n")
print("FROM MEAN")
print(f"mean: {mean}")
print(f"amplitude (ex outliers, from mean): {amplitude_from_mean}")
print(f"amplification (ex outliers, from mean): {recommended_amp_assuming_mean_start}")



# pyplot.text(0.12, 0.95, f"pair: {name1} / {name2}" , transform=pyplot.gcf().transFigure)
# pyplot.text(0.12, 0.9, f"SD to mean: {'{:.3f}'.format(standard_deviation_to_mean)}" , transform=pyplot.gcf().transFigure)
# pyplot.text(0.4, 0.95, f"amplitude: {'{:.3f}'.format(amplitude)}" , transform=pyplot.gcf().transFigure)
# pyplot.text(0.4, 0.9, f"amplitude (ex outliers): {'{:.3f}'.format(trimmed_amplitude)}" , transform=pyplot.gcf().transFigure)

# pyplot.text(0.12, 0.95, f"pair: {name1} / {name2}" , transform=pyplot.gcf().transFigure)
# pyplot.text(0.12, 0.9, f"amplification: {'{:.3f}'.format(recommended_amp)}" , transform=pyplot.gcf().transFigure)
# pyplot.text(0.4, 0.95, f"amplification(ex 1% outliers): {'{:.3f}'.format(recommended_trimmed_amp)}" , transform=pyplot.gcf().transFigure)
# pyplot.text(0.4, 0.9, f"amplification(starting from mean): {'{:.3f}'.format(recommended_amp_assuming_mean_start)}" , transform=pyplot.gcf().transFigure)

pyplot.text(0.05, 0.95, f"amplitude(ex 1%): {'{:.3f}'.format(trimmed_amplitude)}" , transform=pyplot.gcf().transFigure)
pyplot.text(0.05, 0.9, f"amplitude (ex 1%, from mean): {'{:.3f}'.format(amplitude_from_mean)}" , transform=pyplot.gcf().transFigure)
pyplot.text(0.5, 0.95, f"amplification: {'{:.3f}'.format(recommended_trimmed_amp)}" , transform=pyplot.gcf().transFigure)
pyplot.text(0.5, 0.9, f"amplification(ex 1%, from mean): {'{:.3f}'.format(recommended_amp_assuming_mean_start)}" , transform=pyplot.gcf().transFigure)


# plot the ratios
pyplot.plot(ratios)
pyplot.xlabel(f"last {days} days")
pyplot.ylabel(name1 + "/" + name2 + " ratio")
pyplot.show()