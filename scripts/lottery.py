#!/usr/bin/python3
import json
import random
import numpy as np
import os
import time
import os
import discord
from discord.ext import tasks
import json
import random
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator)
import json
import os
import datetime

intents = discord.Intents.default()
intents.members = True
intents.reactions = True
intents.guilds = True

client = discord.Client()

file = open(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))+"/token.txt")
token = file.read()
file.close()


with open(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+"/data/lottery.json", "r") as file:
    tickets = json.load(file)

with open(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+"/data/accounts.json", "r") as file:
    accounts = json.load(file)

## CRONJOB : 45 18 * * SUN
LOTTERY_PRIZE = 100000 #100k 

@client.event
async def on_ready():
    channel = client.get_channel(882939847998861362) #879488994960883723  #882939847998861362

    SLEEP = 60 * 15

    embedVar = discord.Embed(
            title='Weekly Lottery!', description= 'Welcome to our weekly lottery! A winner will be announced in 15 minutes at 8:00 PM EST!\n\nGood luck!\n\n@here', color=0x00ff00)
    await channel.send(embed=embedVar)
    
    time.sleep(SLEEP)

    allTickets = []

    for ticket in tickets.keys():
        for i in range(tickets[ticket]):
            allTickets.append(ticket)
            print(i)

    winner = allTickets[random.randint(0, len(allTickets) - 1)]

    for account in accounts:
        if account['name'] == winner:
            account['value'] += LOTTERY_PRIZE
    embedVar = discord.Embed(
            title='Weekly Lottery!', description= 'Congratulations to:\n\n**' + winner + '**\n\nYou have won ' + "${:,.2f}".format(LOTTERY_PRIZE) + ' dollars!!\n\n@here', color=0x00ff00)
    exit()
    


client.run(token)