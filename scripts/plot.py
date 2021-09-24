import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator)
import json
import os
with open(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+"/data/stonks.json", "r") as file:
    allStonks = json.load(file)


def plotSetup():
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

    ax.xaxis.set_major_locator(MultipleLocator(5))
    ax.xaxis.set_major_formatter('{x:.0f}')

    # For the minor ticks, use no labels; default NullFormatter.
    ax.xaxis.set_minor_locator(MultipleLocator(1))

    plt.gca().axes.xaxis.set_ticklabels([])


graphColors = ['blue', 'orange', 'green', 'red']
i = 0
for stonk in allStonks:
    plotSetup()
    names = []
    graphLen = len(allStonks[0]['history'])
    graph = stonk['history'][graphLen - 6*10:] # stonk['history']
    name = stonk['stonk']
    names.append(name)
    plt.plot(graph, color=graphColors[i])
    i += 1

    # Function add a legend  
    plt.legend(names, loc ="lower right")

    plt.xlim([0, 100]) # ([graphLen - 6*4, graphLen + 10])
    plt.savefig(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+'/stonksCharts' + name.upper() + '.png', transparent=True)


plotSetup()
names = []
graphLen = len(allStonks[0]['history'])
i = 0
for stonk in allStonks:
    graph = stonk['history'][graphLen - 6*10:] # stonk['history']
    name = stonk['stonk']
    names.append(name)
    plt.plot(graph, color=graphColors[i])
    i += 1


# Function add a legend  
plt.legend(names, loc ="lower right")

plt.xlim([0, 100]) # ([graphLen - 6*4, graphLen + 10])
plt.savefig(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+'/stonksCharts.png', transparent=True)
