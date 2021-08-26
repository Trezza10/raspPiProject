import json

with open("/home/mike/Development/raspPiProject/accounts.json", "r") as file:
    accounts = json.load(file)

with open("/home/mike/Development/raspPiProject/accounts.json", "w") as file:
    for account in accounts:
        account['value'] += account['job']['rate']
    json.dump(accounts, file)