import json
import random
import math
import numpy as np


with open("/home/mike/Development/raspPiProject/stonks.json", "r") as file:
    stonks = json.load(file)

with open("/home/mike/Development/raspPiProject/stonks.json", "w") as file:
    for stonk in stonks:
        daily_vol = random.uniform(0.01, 0.04)
        lastVal = stonk['value']
        newVal = round(lastVal * (1 + np.random.normal(0, daily_vol)), 2)
        stonk['value'] = newVal
        stonk['history'].append(newVal)
        print("${:.2f}".format(stonk['value']))
        if stonk['value'] <= 0:
            stonk['value'] = 10
    json.dump(stonks, file)