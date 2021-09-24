#!/bin/python3
import os
import discord
from discord.ext import tasks
import json
import random
import datetime

intents = discord.Intents.default()
intents.members = True
intents.reactions = True
intents.guilds = True

client = discord.Client()

file = open(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))+"/token.txt")
token = file.read()
file.close()

#token = os.getenv('BOT_TOKEN')

@client.event
async def on_ready():
    channel = client.get_channel(882939847998861362)
    with open(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+"/data/stonks.json", "r") as file:
        allStonks = json.load(file)
    dailyReport = ''
    randomStonk = random.choice([0, 1, 2, 3])

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    today = datetime.datetime.now()
    date = str(months[int(today.month)- 1]) + " " + str(today.day) + ", " + str(today.year)
    
    for i in range(len(allStonks)):
        if (i == randomStonk):
            randomEvent = random.choice([-2,-1, 1, 2]) # (Really bad, bad, neutral, good, really good)
        else:
            randomEvent = 0 #neutral day [0.01, 0.03]
        allStonks[i]['dailyVolatility'] = [random.choice([0.005, 0.01, 0.015, 0.02, 0.025]), random.choice([0.025,0.03,0.035,0.04])]
        if (randomEvent == -2):
            dailyReport += "**UH OH!**\n\n**" + allStonks[i]['stonk'] + "'s** CEO *accidentally* stuck his dick into a microwave.\n"
            allStonks[i]['influence'] = -0.01
        elif(randomEvent == -1):
            dailyReport += "**oooof.**\n\nThe CEO of **" + allStonks[i]['stonk'] + "** was too busy GRINDIN for diamond last night and went on a MASSIVE loss streak...\n\n..__he is now Bronze 3.__\n"
            allStonks[i]['influence'] = -0.005
        elif(randomEvent == 0):
            allStonks[i]['influence'] = 0
        elif(randomEvent == 1):
            dailyReport += "**:eyes::eyes:**\n\n**" + allStonks[i]['stonk'] + "'s** CEO was caught at the park giving every good boy BEEG pets.\n"
            allStonks[i]['influence'] = 0.005
        elif(randomEvent == 2):
            dailyReport += "**OKAY QUEEN POP OFF**\n\nRumors has it that, **" + allStonks[i]['stonk'] + "'s** CEO, has hit CHALLENGER.\n"
            allStonks[i]['influence'] = 0.01
    
    with open(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+"/data/stonks.json", "w") as file:
        json.dump(allStonks, file)
        
    with open(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+"/data/accounts.json", "r") as file:
        allAccounts = json.load(file)

    dailyReport += '\n'

    for account in allAccounts:
        ALL_BITCH_TRAITS = ['keep_job', 'best_job', 'card_count', 'finese_the_dealer', 'slight_of_hand']
        if ('keep_job' not in account['bitch']['traits']):
            account['job']['date'] = -1
            account['job']['jobTitle'] = "Jobless"
            account['job']['rate'] = 0
        if (account['bitch']['name'] != 'Nobody' and account['bitch']['balance'] > 0):
            excuses = [
                ', bc you were too cheap... come on man.', 
                ', bc you did not treat her like a QUEEN', 
                ', bc you did not spend enough time with her.', 
                ', bc she met another man.',
                ', bc you just got TOO much money. SIKE.',
                ', bc you kept talkin that good game and fell short my guy.',
                ', bc she thought you were too broke for her.',
                ', bc she low key kinda a man and dealing with shit.',
                ', bc she be shiddn, fartn, and cummn.',
                ', bc she did not like yo ass.'
            ]
            dailyReport += '\n- **' + account['name'] + '** lost your bitch, ' + account['bitch']['name'] + excuses[random.randint(0,5)]
            account['bitch'] = {'name': 'Nobody', 'value': 0, 'date': -1, 'traits': [], 'balance': 0}
        else:
            assetValue = 0
            for _stonk in account['stonks'].keys():
                for liveStonk in allStonks:
                   if liveStonk['stonk'] == _stonk:
                        haveStonk = liveStonk

                for _share in account['stonks'][_stonk]:
                    assetValue +=  account['stonks'][_stonk][_share] * float(haveStonk['value'])


            netWorth = float(assetValue) + float(account['value'])
            account['bitch']['value'] += 5
            account['bitch']['balance'] = netWorth * (account['bitch']['value']/100) * 0.2
            if account['bitch']['value'] - 60 < 5 or account['bitch']['value'] - 100 < 5 or account['bitch']['value'] - 125 < 5 or account['bitch']['value'] - 150 < 5:
                for trait in account['bitch']['traits']:
                    ALL_BITCH_TRAITS.remove(trait)
                    
                if len(ALL_BITCH_TRAITS) != 0:
                    randTrait = ALL_BITCH_TRAITS[random.randint(0,len(ALL_BITCH_TRAITS) - 1)]
                    account['bitch']['traits'].append(randTrait)
                    dailyReport += '\n- **' + account['name'] + ', your bitch gained the **' + randTrait + '** trait!' 

            

    dailyReport += "\n\n...... Aaaandddd you lost your job."

    with open(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+"/data/accounts.json", "w") as file:
        json.dump(allAccounts, file)
    
    
    embedVar = discord.Embed(
            title='Daily Reports: '+ date, description=dailyReport, color=0x00ff00)
    await channel.send(embed=embedVar)
    exit()
    
client.run(token)
