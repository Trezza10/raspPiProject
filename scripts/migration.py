import json

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