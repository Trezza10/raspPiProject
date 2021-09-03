import json
import random
import math
import numpy as np


with open("stonks.json", "r") as file:
    stonks = json.load(file)

with open("stonks.json", "w") as file:
    for stonk in stonks:
        daily_vol = random.uniform(stonk['dailyVolatility'][0], stonk['dailyVolatility'][1])
        lastVal = stonk['value']
        newVal = round(lastVal * (1 + np.random.normal(stonk['influence'], daily_vol)), 2)
        stonk['value'] = newVal
        stonk['history'].append(newVal)
        print("${:.2f}".format(stonk['value']))
        if stonk['value'] <= 0:
            stonk['value'] = 10
    json.dump(stonks, file)
