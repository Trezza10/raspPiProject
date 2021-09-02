#!/bin/python3
import os
import discord
from discord.ext import tasks
import json
import random

intents = discord.Intents.default()
intents.members = True
intents.reactions = True
intents.guilds = True

client = discord.Client()

"""file = open('./../token.txt')
token = file.read()
file.close()"""

token = os.getenv('BOT_TOKEN')

@client.event
async def on_ready():
    channel = client.get_channel(864619752991096836)

    print(channel)
    with open("stonks.json", "r") as file:
        allStonks = json.load(file)
    dailyReport = ''

    for _stonk in allStonks:
        randomEvent = random.randint(-2, 2) # (Really bad, bad, neutral, good, really good)
        if (randomEvent == -2):
            dailyReport += _stonk['stonk'] + "'s CEO did an oopsy\n"
            _stonk['influence'] = -0.01
        elif(randomEvent == -1):
            dailyReport += _stonk['stonk'] + "'s CEO did a lil bit less of an oopsy\n"
            _stonk['influence'] = -0.005
        elif(randomEvent == 0):
            dailyReport += _stonk['stonk'] + "'s is gucci\n"
            _stonk['influence'] = 0
        elif(randomEvent == 1):
            dailyReport += _stonk['stonk'] + "'s CEO did a lil bit of a yuppers\n"
            _stonk['influence'] = 0.005
        elif(randomEvent == 2):
            dailyReport += _stonk['stonk'] + "'s CEO did a big yuppers\n"
            _stonk['influence'] = 0.01
    
    with open("stonks.json", "w") as file:
        json.dump(allStonks, file)

    embedVar = discord.Embed(
            title='Daily Reports', description=dailyReport, color=0x00ff00)
    await channel.send(embed=embedVar)
    exit()
    

client.run(token)