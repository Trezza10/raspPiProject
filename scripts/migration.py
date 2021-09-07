import json
import random

VERSION = 2

#############
# VERSION 2
#############
if (VERSION == 2):
    with open("../data/accounts.json", "r") as file:
        allAccounts = json.load(file)

    for account in allAccounts:
        assetValue = 0

        with open("../data/stonks.json", "r") as file:
            liveStonks = json.load(file)

        for _stonk in account['stonks']:
            for liveStonk in liveStonks:
                if liveStonk['stonk'] == _stonk['stonk']:
                    haveStonk = liveStonk

            for _own in _stonk['own']:
                assetValue += float(_own['quantity']) * float(haveStonk['value'])
            
        netWorth = float(assetValue) + float(account['value'])

        account['bitch']['trait'] = random.choice(['gamble', 'jobs'])
        account['bitch']['balance'] = netWorth * (account['bitch']['value']/100) * 0.2

    with open("../data/accounts.json", "w") as file:
        json.dump(allAccounts, file)



#############
# VERSION 1
#############
if (VERSION == 1):
    with open("../data/accounts.json", "r") as file:
        allAccounts = json.load(file)

    for account in allAccounts:
        account['job']['date'] = -1

    with open("../data/accounts.json", "w") as file:
        json.dump(allAccounts, file)




    with open("../data/stonks.json", "r") as file:
        allStonks = json.load(file)

    for stonk in allStonks:
        stonk['dailyVolatility'] = [0.01, 0.03]
        stonk['influence'] = 0

    with open("../data/stonks.json", "w") as file:
        json.dump(allStonks, file)