import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator)
import json

with open("stonks.json", "r") as file:
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

ax.xaxis.set_major_locator(MultipleLocator(6))
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

var = 'test'
plt.xlim([graphLen - 6*4, graphLen + 10])
plt.savefig('demo.png', transparent=True)
plt.show()
