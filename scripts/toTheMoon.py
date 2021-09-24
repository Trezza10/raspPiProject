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


with open(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+"/data/stonks.json", "r") as file:
    stonks = json.load(file)



@client.event
async def on_ready():
    channel = client.get_channel(882939847998861362) #879488994960883723  #882939847998861362
    j = 0
    SLEEP = 60*6
    timeRn = datetime.datetime.now()
    stonksName = ['OWO', 'HUH', 'YEP', 'DOG']
    randomStonk = random.choice([0,1,2,3])
    print(stonksName[randomStonk] + ' TO THE MOOON!!!!!!!!!!!!!!!!!! ')

    embedVar = discord.Embed(
            title='TO THE MOOOOOOOON!!!!!!!!', description= '**' + stonksName[randomStonk] + '** HAS LIFT OFF!\n\nFOR THE NEXT HOUR ( ends at ' + str((timeRn.hour + 1) % 24) + ":" + "{0:0=2d}".format((timeRn.minute)) + ')**' + stonksName[randomStonk] + '** WILL SKY ROCKET IN PRICE!\n\n@here', color=0x00ff00)
    await channel.send(embed=embedVar)
    

    while j < 10:
        print(j)
        for i in range(len(stonks)):
            if (i != randomStonk):
                daily_vol = random.uniform(stonks[i]['dailyVolatility'][0], stonks[i]['dailyVolatility'][1])
                lastVal = stonks[i]['value']
                stonks[i]['beforeTheMoon'] = -1
                newVal = round(lastVal * (1 + np.random.normal(stonks[i]['influence'], daily_vol)), 2)
                stonks[i]['value'] = newVal
                stonks[i]['history'].append(newVal)
                print("${:.2f}".format(stonks[i]['value']))
                if stonks[i]['value'] <= 0:
                    stonks[i]['value'] = 10
            else:
                daily_vol = random.uniform(stonks[i]['dailyVolatility'][0]*2.5, stonks[i]['dailyVolatility'][1]*2.5)
                lastVal = stonks[i]['value']
                newVal = round(lastVal * (1 + np.random.normal(stonks[i]['influence'] + random.choice([-0.15, -0.1, -0.05, 0, 0.05, 0.1, 0.15]), daily_vol)), 2)
                if j == 0:
                    stonks[i]['beforeTheMoon'] = lastVal
                stonks[i]['value'] = newVal
                stonks[i]['history'].append(newVal)
                print(stonksName[randomStonk] + ' went up ' + str(newVal - lastVal) + '. And now is at ' + str(newVal) )
                print("${:.2f}".format(stonks[i]['value']))
                if stonks[i]['value'] <= 0:
                    stonks[i]['value'] = 10

        with open(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+"/data/stonks.json", "w") as file:
            json.dump(stonks, file)

        plotGraph()
        if (j == 9):
            embedVar = discord.Embed(
                title='Returning from the moon!', description= '**' + stonksName[randomStonk] + '** IS ON ITS WAY HOME!\n\nEvent will end at ' + str((timeRn.hour + 1) % 24) + ":" + "{0:0=2d}".format(timeRn.minute) + ' EST!**\n\n ' + stonksName[randomStonk] + '**. SELL! SELL! SELL!\n\n@here', color=0x00ff00)
            await channel.send(embed=embedVar)
        print('going to sleep')
        time.sleep(SLEEP)
        print('awake')
        j += 1
        
    for stonk in stonks:
        if (stonk['beforeTheMoon'] != -1):
            embedVar = discord.Embed(
                    title='MISSION COMPLETE', description= '**' + stonksName[randomStonk] + '** LANDED BACK TO EARTH!\n\nAND HAS RESUMED REGULAR DAY TO DAY ACTIVITIES\n\n@here', color=0x00ff00)
            await channel.send(embed=embedVar)

            newVal = int((stonk['value'] - stonk['beforeTheMoon']) * random.choice([.25, .3, .35, .4, .45, .5])) + stonk['beforeTheMoon']
            stonk['beforeTheMoon'] = -1
            stonk['value'] = newVal
            stonk['history'].append(newVal)
        else:
            daily_vol = random.uniform(stonk['dailyVolatility'][0], stonk['dailyVolatility'][1])
            lastVal = stonk['value']
            stonk['beforeTheMoon'] = -1
            newVal = round(lastVal * (1 + np.random.normal(stonk['influence'], daily_vol)), 2)
            stonk['value'] = newVal
            stonk['history'].append(newVal)
    
    with open(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+"/data/stonks.json", "w") as file:
        json.dump(stonks, file)
    
    plotGraph()

    exit()
    

def plotGraph():
    
    with open(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+"/data/stonks.json", "r") as file:
        allStonks = json.load(file)

    fig = plt.figure()

    ax = fig.add_subplot()

    ax.set_xlabel('Time')
    ax.set_ylabel('Price')

    ax.xaxis.label.set_color('white')        #setting up X-axis label color to yellow
    ax.yaxis.label.set_color('white')          #setting up Y-axis label color to blue

    ax.tick_params(axis='x', colors='white')    #setting up X-axis tick color to red
    ax.tick_params(axis='y', colors='white')  #setting up Y-axis tick color to black

    ax.spines['left'].set_color('white')        # setting up Y-axis tick color to red
    ax.spines['bottom'].set_color('white')         #setting up above X-axis tick color to red
    ax.spines['right'].set_color('white')        # setting up Y-axis tick color to red
    ax.spines['top'].set_color('white')         #setting up above X-axis tick color to red

    ax.xaxis.set_major_locator(MultipleLocator(3))
    ax.xaxis.set_major_formatter('{x:.0f}')

    # For the minor ticks, use no labels; default NullFormatter.
    ax.xaxis.set_minor_locator(MultipleLocator(1))

    names = []
    graphLen = len(allStonks[0]['history'])
    for stonk in allStonks:
        graph = stonk['history']
        name = stonk['stonk']
        names.append(name)
        plt.plot(graph)


    # Function add a legend  
    plt.legend(names, loc ="lower right")

    plt.xlim([graphLen - 6*4, graphLen + 10])
    plt.savefig(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+'/stonksCharts.png', transparent=True)


client.run(token)