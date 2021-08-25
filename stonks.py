import json
import random

with open("stonks.json", "r") as file:
    stonks = json.load(file)

with open("stonks.json", "w") as file:
    for stonk in stonks:
        rand = (random.randrange(-10,10))
        if stonk['value'] + rand >= 0:
            stonk['value'] += rand
        else: 
            stonk['value'] = 0
        
    json.dump(stonks, file)