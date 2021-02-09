import json

with open('btc.json') as json_file:
    data1 = json.load(json_file)

with open('eth.json') as json_file:
    data2 = json.load(json_file)

for r in data1:
  print(r["rate"])
