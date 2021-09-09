import json
import random
import os

VERSION = 2

#############
# VERSION 2
#############
if (VERSION == 2):
    with open(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+"/data/accounts.json", "r") as file:
        allAccounts = json.load(file)

    for account in allAccounts:
        assetValue = 0

        with open(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+"/data/stonks.json", "r") as file:
            liveStonks = json.load(file)

        for _stonk in account['stonks']:
            for liveStonk in liveStonks:
                if liveStonk['stonk'] == _stonk['stonk']:
                    haveStonk = liveStonk

            for _own in _stonk['own']:
                assetValue += float(_own['quantity']) * float(haveStonk['value'])
            
        netWorth = float(assetValue) + float(account['value'])
        
        ALL_BITCH_TRAITS = ['keep_job', 'best_job', 'card_count', 'finese_the_dealer', 'slight_of_hand']
        randomTrait = random.choice(ALL_BITCH_TRAITS)
        ALL_BITCH_TRAITS.remove(randomTrait)
        secondTrait = random.choice(ALL_BITCH_TRAITS)
        ALL_BITCH_TRAITS.remove(secondTrait)
        thirdTrait = random.choice(ALL_BITCH_TRAITS)
        account['bitch']['traits'] = []
        if (account['bitch']['value'] >= 20 and account['bitch']['value'] < 60):
            account['bitch']['traits'].append(randomTrait)
        elif (account['bitch']['value'] < 99):
            account['bitch']['traits'].append(randomTrait)
            account['bitch']['traits'].append(secondTrait)
        elif (account['bitch']['value'] == 100):
            account['bitch']['traits'].append(randomTrait)
            account['bitch']['traits'].append(secondTrait)
            account['bitch']['traits'].append(thirdTrait)
        account['bitch']['balance'] = int(netWorth * (account['bitch']['value']/100) * 0.1)

    with open(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+"/data/accounts.json", "w") as file:
        json.dump(allAccounts, file)



#############
# VERSION 1
#############
if (VERSION == 1):
    with open(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+"/data/accounts.json", "r") as file:
        allAccounts = json.load(file)

    for account in allAccounts:
        account['job']['date'] = -1

    with open(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+"/data/accounts.json", "w") as file:
        json.dump(allAccounts, file)




    with open(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+"/data/accounts.json", "r") as file:
        allStonks = json.load(file)

    for stonk in allStonks:
        stonk['dailyVolatility'] = [0.01, 0.03]
        stonk['influence'] = 0

    with open(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+"/data/accounts.json", "w") as file:
        json.dump(allStonks, file)