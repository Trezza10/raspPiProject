import json

with open("/home/mike/Development/raspPiProject/data/accounts.json", "r") as file:
    accounts = json.load(file)

with open("/home/mike/Development/raspPiProject/data/accounts.json", "w") as file:
    for account in accounts:
        account['value'] += int(account['job']['rate'])
    json.dump(accounts, file)