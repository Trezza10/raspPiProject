import discord
from discord.ext import commands
import json
import random
import datetime 

'''
Billionaire Bot. Who has what it takes to be a billionaire by the end of the month. 

Things to do to become a billionaire
1. Get a job. (!jobs)
    - Child labor slave (!job get int)
        - $1 dollar an hour (24 dollars per day bc you're a slave)
    - McDonald's Employee
        - $8 dollars an hour (64 dollars per day)

3. PASSIVE INCOME
    - Real estate
    - Invest in 

5. Stocks
    - Have a selection of multiple 5 stocks
    - Buy and sell x amount of each stock
    - Randomly go up and down per day.

6. Find a bad bitch
    - Every day you have to find a new bad bitch, like all billionaires do.
        - 0 <= bitch < 10  takes 20% of your net worth immediately for the day
        - 10 <= bitch < 20 takes 10 % of your net worth immediately for the day
        - 20 <= bitch < 80 just a nice side piece
        - 80 <= bitch < 90 adds 10% net worth immediately for the day
        - 90 <= bitch < 99 add 20% net worth immediately for the day
        - 100% BAD BITCH = 2x net worth.

7. Gamble (!gamble)
    - Coin flip (!coinflip x)
        - 50/50 chance to double your money put in
    - Black jack (!blackjack)
        - !hit, !stay
'''

channelId = 633465922786689024 #864619752991096833
BOT_IMAGE = 'https://www.media3.hw-static.com/wp-content/uploads/xx_55026731-638x425-638x425.jpeg'
JOB_AVAILABILITY = 10
TICKET_PRICE = 100

file = open('./../token.txt')
token = file.read()
file.close()


with open("data/bitches.json", "r") as file:
    allBitches = json.load(file)


with open("data/jobs.json", "r") as file:
    allJobs = json.load(file)

# Creates bot with the prefix of !
bot = commands.Bot(command_prefix="!")

# Introduction
@bot.command(
    profile="introduction",
    brief="introduction"
)
async def intro(ctx):
    
    embedVar = discord.Embed(
            title='Welcome', description="\"\"Everybody here has the ability absolutely to do anything I do and much beyond, and some of you will and some of you won't.\"- Warren Buffet\"\n- BillionaireBot", color=0x00ff00)
    await ctx.channel.send(embed=embedVar)
    
    embedVar = discord.Embed(
            title='The Journey', description="One can speak about making BILLIONS... but do you have what it takes to actually EARN BILLIONS?\n\nWell now you can... for the next 30 days. I want to see who will become the first Discord **BILLIONAIRE**. \n\n\n\nYour journey starts now.", color=0x00ff00)
    await ctx.channel.send(embed=embedVar)
    
    embedVar = discord.Embed(
            title='Get Started', description="Each command is prefixed with !\n\nTo see all commands type \"!help\"", color=0x00ff00)
    await ctx.channel.send(embed=embedVar)



# Creates account
'''@bot.command(
    profile="cheat",
    brief="cheat"
)
async def cheat(ctx):

    with open("data/accounts.json", "r") as file:
        accounts = json.load(file)

    for account in accounts:
        account['value'] = 5000.00
        writeToAccountDb(account)
    
    embedVar = discord.Embed(
            title='cheatin', description="We cheatin", color=0x00ff00)
    await ctx.channel.send(embed=embedVar)
'''
    
# Creates account
@bot.command(
    profile="createAccount",
    brief="createAccount"
)
async def createAccount(ctx):

    with open("data/accounts.json", "r") as file:
        accounts = json.load(file)

    name = ctx.message.author.name
    index = -1
    for account in accounts:
        if (account['name'] == name):
            index = accounts.index(account)

    if (index == -1):
        account = {}
        account['name'] = ctx.message.author.name
        account['job'] = {'jobTitle': 'Jobless', 'rate': 0, 'date': -1}
        account['value'] = 500.00
        account['debt'] = 0.00
        account['bitch'] = {'name': 'Nobody', 'value': 0, 'date': -1, 'trait': [], 'balance': 0}
        account['stonks'] = []

        # Create embed message display
        embedVar = displayProfile(account, ctx.message.author.avatar_url)

        writeToAccountDb(account)

        await ctx.channel.send(embed=embedVar)
    else:
        embedVar = discord.Embed(
            title=name, description="Already has an account", color=0x00ff00)
        await ctx.channel.send(embed=embedVar)


# Random bitch of the day
@bot.command(
    profile="Find your bad bitch TODAY",
    brief="Find your bad bitch TODAY"
)
async def bitch(ctx, arg1 = 'show', arg2 = -1):
    if (arg1 == 'get'):
        today = int(datetime.datetime.now().day)
        accounts = readAccountsFromDb()
        for _account in accounts:
            if _account['name'] == ctx.message.author.name:
                account = _account
                break
        if (account['bitch']['date'] < today):
            assetValue = 0

            with open("data/stonks.json", "r") as file:
                liveStonks = json.load(file)

            for _stonk in _account['stonks']:
                for liveStonk in liveStonks:
                    if liveStonk['stonk'] == _stonk['stonk']:
                        haveStonk = liveStonk

                for _own in _stonk['own']:
                    assetValue += float(_own['quantity']) * float(haveStonk['value'])
                
            netWorth = float(assetValue) + float(_account['value'])

            randomBitch = allBitches[random.randint(0, len(allBitches)-1)]
            randomBitchValue = random.randint(0, 100)
            account['bitch']['name'] = randomBitch
            account['bitch']['value'] = randomBitchValue
            account['bitch']['date'] = today
            account['bitch']['traits'] = [] #, 'OWO', 'HUH', 'YEP', 'DOG'])
            account['bitch']['balance'] = netWorth * (randomBitchValue/100) * 0.2 # NETWORTH * BITCHES VALUE/100 * .2 PER DAY
            currentNetWorth = account['value']
            account['value'] = await bitchesValue(randomBitchValue, currentNetWorth, account['bitch'], ctx)
            embedVar = displayProfile(account, ctx.message.author.avatar_url)
            writeToAccountDb(account)

            await ctx.channel.send(embed=embedVar)
        else:
            embedVar = discord.Embed(
                title='You kinda unloyal', description="You must keep yo bitch for at least one day before finding a new side piece.", color=0x00ff00)
            await ctx.channel.send(embed=embedVar)
    elif (arg1 == 'show'):
        accounts = readAccountsFromDb()

        for _account in accounts:
            if _account['name'] == ctx.message.author.name:
                account = _account
                break
        
        bitchTraits = ''
        for _traits in account['bitch']['traits']:
            bitchTraits += '\n - ' + _traits + ''
        embedVar = discord.Embed(
                title=account['bitch']['name'], description='', color=0x00ff00)
        
        embedVar.add_field(name="Value", value=str(account['bitch']['value']), inline=False)
        embedVar.add_field(name="Anniversary", value='September '+ str(account['bitch']['date']), inline=False)
        embedVar.add_field(name="Traits", value=bitchTraits, inline=False)
        embedVar.add_field(name="Balance", value='Needs $' + "{:,.2f}".format(account['bitch']['balance']) + ' or she will leave you', inline=False)
        
        await ctx.channel.send(embed=embedVar)
    elif (arg1 == 'give'):
        accounts = readAccountsFromDb()

        for _account in accounts:
            if _account['name'] == ctx.message.author.name:
                account = _account
                break
        
        if ((str(arg2).isnumeric() and account['value'] < int(arg2)) or (arg2 == 'all' and account['value'] < account['bitch']['balance'])):
            embedVar = discord.Embed(
                title='Not enough funds', description="You can pay her a maximum of " + "{:,.2f}".format(account['value']) + ' dollars', color=0x00ff00)
            await ctx.channel.send(embed=embedVar)
            return
        if (account['bitch']['name'] == 'Nobody'):
            embedVar = discord.Embed(
                title='You aint got bitches', description="You aint got bitches to give nothing to my guy. Either go get a bitch or go listen to Drake on spotify.", color=0x00ff00)
            await ctx.channel.send(embed=embedVar)
            return

        if (account['bitch']['balance'] <= 0):
            embedVar = discord.Embed(
                title='Boiiii whatchu doing', description="You aint supposed to OVER pay yo bitch.\n\n\n\nThe hell is wrong with you.....", color=0x00ff00)
            await ctx.channel.send(embed=embedVar)
            return
        
        if (arg2 == 'all'):
            account['value'] -= account['bitch']['balance']
            account['bitch']['balance'] -= 0
            account['bitch']['value'] += 5
            embedVar = discord.Embed(
                    title='Payment Accepted', description=str(account['bitch']['name']) + ' is quite happy now. She now might reconsider leaving your broke ass for someone else.', color=0x00ff00)
            await ctx.channel.send(embed=embedVar)
        else:
            account['value'] -= int(arg2)
            account['bitch']['balance'] -= int(arg2)
            if (account['bitch']['balance'] <= 0):
                account['bitch']['value'] += 5
                embedVar = discord.Embed(
                    title='Payment Accepted', description=str(account['bitch']['name']) + ' is quite happy now. She now might reconsider leaving your broke ass for someone else.', color=0x00ff00)
                await ctx.channel.send(embed=embedVar)
            else:
                embedVar = discord.Embed(
                    title='Payment Accepted', description=str(account['bitch']['name']) + ' accepts the jesture... but still wants $' + "{:,.2f}".format(account['bitch']['balance']) + ' dollars', color=0x00ff00)
                await ctx.channel.send(embed=embedVar)
        
        writeToAccountDb(account)
    else:
        embedVar = discord.Embed(title='Incorrect bitches command',
            description='Use the following:\n\n!bitch show\n\n!bitch get\n\n!bitch give \{money\}', color=0x00ff00)
        await ctx.channel.send(embed=embedVar)
    
        

# The stonks boi
@bot.command(
    profile="stonks",
    brief="stonks"
)
async def stonks(ctx, arg1 = 'show', arg2 = '-1', arg3 = '-1'):
    if (arg1 == 'show' and arg2 == '-1' and arg3 == '-1'):
        embedVar = discord.Embed(title='BillionaireBot',
                                description='Stonks on the market. (Updated every 15 minutes)', color=0x00ff00)

        allStonks = readStonksFromDb()

        i = 1
        for stonk in allStonks:
            stonkName = stonk['stonk']
            stonkValue = stonk['value']
            embedVar.add_field(name="[" + str(i) + "] " + stonkName,
                            value="$" + "{:,.2f}".format(stonkValue) + " ", inline=False)
            i += 1
        
        file = discord.File("stonksCharts.png")
        embedVar.set_image(url="attachment://stonksCharts.png")
        await ctx.send(file = file, embed=embedVar)
    elif (arg1 == 'buy'):
        if (arg2.isnumeric() and (arg3.isnumeric() or arg3 == 'max')):
            await buyStonks(ctx, arg2, arg3)
    elif (arg1 == 'sell'):
        if (arg2.isnumeric()):
            await sellStonks(ctx, arg2)
    else:
        embedVar = discord.Embed(title='Incorrect stonks command',
                             description='Use the following:\n\n!stonks\n\n!stonks buy x(stonk #), y(quantity)\n\n!stonks sell x(stonk #)', color=0x00ff00)
        await ctx.channel.send(embed=embedVar)

# Jobs
@bot.command(
    profile="Jobs",
    brief="Jobs"
)
async def jobs(ctx, arg1 = 'show'):
    if (arg1 == 'show'):
        embedVar = discord.Embed(title='BillionaireBot',
                                description='Jobs on the market(More jobs coming)', color=0x00ff00)
        embedVar.set_thumbnail(url=BOT_IMAGE)

        i = 1
        for job in allJobs:
            if (i >= JOB_AVAILABILITY + 1):
                break
            jobName = job['name']
            jobRate = job['rate']
            embedVar.add_field(name="[" + str(i) + "] " + jobName,
                            value="$" + "{:,.2f}".format(jobRate) + " per hour", inline=False)
            i += 1

        await ctx.channel.send(embed=embedVar)
    elif (arg1 == 'get'):
        await getAJob(ctx, str(random.randint(0,JOB_AVAILABILITY)))
    else:
        embedVar = discord.Embed(title='Incorrect jobs command',
                             description='Use the following:\n\n!jobs\n\n!jobs get', color=0x00ff00)
        await ctx.channel.send(embed=embedVar)


# get a job
async def getAJob(ctx, args):
    if (args.isnumeric()):
        job = int(args) - 1
        if not(0 <= job < len(allJobs) - 1):
            return

    accounts = readAccountsFromDb()
    for _account in accounts:
        if _account['name'] == ctx.message.author.name:
            account = _account
            break

    today = int(datetime.datetime.now().day)
    
    if (account['job']['date'] < today):
        if ('best_job' in account['bitch']['traits']):
            account['job']['jobTitle'] = allJobs[JOB_AVAILABILITY - 1]['name']
            account['job']['rate'] = allJobs[JOB_AVAILABILITY - 1]['rate']
            account['job']['date'] = today
        else:
            account['job']['jobTitle'] = allJobs[job]['name']
            account['job']['rate'] = allJobs[job]['rate']
            account['job']['date'] = today
    else:
        embedVar = discord.Embed(
                title='Lazy ass bum', description="You gonna have to **WORK** for your job before you get a new one.\n\nYou must wait till tomorrow to get a new job.", color=0x00ff00)
        await ctx.channel.send(embed=embedVar)
        return

    embedVar = displayProfile(account, ctx.message.author.avatar_url)
    writeToAccountDb(account)

    await ctx.channel.send(embed=embedVar)


# What's your profile
@bot.command(
    profile="profile",
    brief="profile"
)
async def profile(ctx):
    accounts = readAccountsFromDb()
    for _account in accounts:
        if _account['name'] == ctx.message.author.name:
            account = _account
            break

    embedVar = displayProfile(account, ctx.message.author.avatar_url)

    await ctx.channel.send(embed=embedVar)



# Buy/sell stonks
async def buyStonks(ctx, arg1, arg2):
    print(arg1, arg2)

    with open("data/stonks.json", "r") as file:
        allStonks = json.load(file)

    if (arg1.isnumeric()):
        _stonkBuying = int(arg1) - 1
        if not(0 <= _stonkBuying < len(allStonks)):
            return

    accounts = readAccountsFromDb()
    for _account in accounts:
        if _account['name'] == ctx.message.author.name:
            account = _account
            break

    # enough money?
    if (arg2 == 'max' and account['value'] >= allStonks[int(_stonkBuying)]['value']):
        # Loop through all your stonks
        haveStonk = False
        for _stonk in account['stonks']:
            # check to see if you already have stonk of it
            if allStonks[int(_stonkBuying)]['stonk'] == _stonk['stonk']:
                haveStonk = True
                # append x stonks to list of that
                _stonk['own'].append(
                    {
                        'priceBoughtAt': allStonks[int(_stonkBuying)]['value'],
                        'quantity': int(account['value']/allStonks[int(_stonkBuying)]['value'])
                    }
                )
                print(_stonk)

        if not(haveStonk):
            account['stonks'].append(
                {
                    'stonk': allStonks[int(_stonkBuying)]['stonk'],
                    'own': [
                        {
                            'priceBoughtAt': allStonks[int(_stonkBuying)]['value'],
                            'quantity': int(account['value']/allStonks[int(_stonkBuying)]['value'])
                        }
                    ]
                }
            )
        # Deduct moneys
        account['value'] -= int(account['value'] / allStonks[int(_stonkBuying)]['value']) * allStonks[int(_stonkBuying)]['value']
        embedVar = displayProfile(account, ctx.message.author.avatar_url)
        writeToAccountDb(account)

        await ctx.channel.send(embed=embedVar)
    elif (arg2 != 'max' and account['value'] >= allStonks[int(_stonkBuying)]['value'] * int(arg2)):
        # Loop through all your stonks
        haveStonk = False
        for _stonk in account['stonks']:
            # check to see if you already have stonk of it
            if allStonks[int(_stonkBuying)]['stonk'] == _stonk['stonk']:
                haveStonk = True
                # append x stonks to list of that
                _stonk['own'].append(
                    {
                        'priceBoughtAt': allStonks[int(_stonkBuying)]['value'],
                        'quantity': int(arg2)
                    }
                )
                print(_stonk)

        if not(haveStonk):
            account['stonks'].append(
                {
                    'stonk': allStonks[int(_stonkBuying)]['stonk'],
                    'own': [
                        {
                            'priceBoughtAt': allStonks[int(_stonkBuying)]['value'],
                            'quantity': int(arg2)
                        }
                    ]
                }
            )
        # Deduct moneys
        account['value'] -= allStonks[int(_stonkBuying)]['value'] * int(arg2)
        embedVar = displayProfile(account, ctx.message.author.avatar_url)
        writeToAccountDb(account)

        await ctx.channel.send(embed=embedVar)
    else:
        embedVar = discord.Embed(
            title='Not enough funds', description="You can do a maximum of " + str(int(account['value']/allStonks[int(_stonkBuying)]['value'])) + ' shares of ' + allStonks[int(_stonkBuying)]['stonk'] + ' for $' + "{:,.2f}".format(int(account['value'] / allStonks[int(_stonkBuying)]['value']) * allStonks[int(_stonkBuying)]['value']), color=0x00ff00)
        await ctx.channel.send(embed=embedVar)
        return



# sell stonks
async def sellStonks(ctx, arg1):
    print(arg1)

    with open("data/stonks.json", "r") as file:
        allStonks = json.load(file)

    if (arg1.isnumeric()):
        _stonkSell = int(arg1) - 1
        if not(0 <= _stonkSell < len(allStonks)):
            return

    accounts = readAccountsFromDb()
    for _account in accounts:
        if _account['name'] == ctx.message.author.name:
            account = _account
            break
    
    # Loop through all your stonks
    for _stonk in account['stonks']:
        # check to see if you already have stonk of it
        if allStonks[_stonkSell]['stonk'] == _stonk['stonk']:
            for own in _stonk['own']:
                account['value'] += (allStonks[int(_stonkSell)]['value'] * own['quantity'])
            account['stonks'].remove(_stonk) 
        
    writeToAccountDb(account)
    embedVar = displayProfile(account, ctx.message.author.avatar_url)
    await ctx.channel.send(embed=embedVar)



# gamble
@bot.command(
    profile="gamble",
    brief="gamble"
)
async def gamble(ctx, arg1):
    accounts = readAccountsFromDb()
    for _account in accounts:
        if _account['name'] == ctx.message.author.name:
            account = _account
            break
    if (account['value'] < int(arg1)):
        embedVar = discord.Embed(
            title='Not enough funds', description="You can do a maximum of " + "{:,.2f}".format(account['value']) + ' dollars', color=0x00ff00)
        await ctx.channel.send(embed=embedVar)
        return
    if (int(arg1) < 0):
        embedVar = discord.Embed(
            title='Invalid bet', description="You must bet a minimum of $1.00 dollar", color=0x00ff00)
        await ctx.channel.send(embed=embedVar)
        return

    bonusChance = 0
    
    if 'card_count' in account['bitch']['traits']:
        bonusChance = int(account['bitch']['value'] / 5)

    _coinFlip = random.randint(0,100) + bonusChance
    
    if (_coinFlip > 50):
        bonusValue = 0
        bonusDescription = ''
        if 'slight_of_hand' in account['bitch']['traits']:
            print('SLIGHT OF HAND, GET MORE MONEY')
            bonusValue = account['bitch']['value']
            bonusDescription = '\n\n:eyes::eyes: And **' + account['bitch']['name'] + '** won you ' + "{:,.2f}".format(int(bonusValue)) + ' dollars!'
        account['value'] += int(arg1) + bonusValue
        embedVar = discord.Embed(
            title='Coin flip', description="You won " + "{:,.2f}".format(int(arg1)) + " dollars!" + bonusDescription, color=0x00ff00)
    else:
        if 'finesse_the_dealer' in account['bitch']['traits']:
            print('FINESSED, DO NOT LOSE MONEY')
            finessed = random.randint(0,100)
            if finessed >= 51:
                embedVar = discord.Embed(
                    title='Coin flip', description=":eyes::eyes:\nYou almost lost! But your bitch **" + account['bitch']['name'] + "** saved your ass :o", color=0x00ff00)
            else:
                account['value'] -= int(arg1)
                embedVar = discord.Embed(
                    title='Coin flip', description="You lost " + "{:,.2f}".format(int(arg1)) + " dollars!", color=0x00ff00)
        else:
            account['value'] -= int(arg1)
            embedVar = discord.Embed(
                title='Coin flip', description="You lost " + "{:,.2f}".format(int(arg1)) + " dollars!", color=0x00ff00)
     
    writeToAccountDb(account)

    await ctx.channel.send(embed=embedVar)
    embedVar = displaySimpleProfile(account, ctx.message.author.avatar_url)

    await ctx.channel.send(embed=embedVar)

# Lottery
@bot.command(
    profile="lottery",
    brief="lottery"
)
async def lottery(ctx, arg1 = 'info', arg2 = '-1'):
    accounts = readAccountsFromDb()
    for _account in accounts:
        if _account['name'] == ctx.message.author.name:
            account = _account
            break
    
    if (arg1 == 'info'):
        embedVar = discord.Embed(
            title='Lottery', description="The Billionaire Bot lottery takes place once a week and the big winner is announced Sunday Night at 7 pm EST.\n\nTo buy a ticket use the command !lottery buy x.\n\n*Tickets are on sale for " + str(TICKET_PRICE) +". Each user is limited to 100 tickets*", color=0x00ff00)
        await ctx.channel.send(embed=embedVar)   
        return
    if (arg1 == 'buy'):
        if (arg2.isnumeric()):
            if (int(arg2) > 100):
                embedVar = discord.Embed(
                    title='Lottery', description="You can only buy a maximum of 100 tickets!", color=0x00ff00)
                await ctx.channel.send(embed=embedVar)   
                return

            if (account['value'] > int(arg2) * TICKET_PRICE):
                with open("data/lottery.json", "r") as file:
                    allLottery = json.load(file)
                
                if (not(account['name'] in allLottery)):
                    allLottery[account['name']] = int(arg2)
                    account['value'] -= int(arg2) * TICKET_PRICE
                    with open("data/accounts.json", "w") as file:
                            json.dump(accounts, file)

                    with open("data/lottery.json", "w") as file:
                        json.dump(allLottery, file)

                    embedVar = discord.Embed(
                        title='Lottery', description="Congratulations you have bought yourself a ticket to the upcoming lottery!", color=0x00ff00)
                    await ctx.channel.send(embed=embedVar)   
                    return
                else:
                    if (allLottery[account['name']] + int(arg2) < 100):
                        allLottery[account['name']] += int(arg2)
                        account['value'] -= int(arg2) * TICKET_PRICE
                        
                        with open("data/accounts.json", "w") as file:
                            json.dump(accounts, file)

                        with open("data/lottery.json", "w") as file:
                            json.dump(allLottery, file)

                        embedVar = discord.Embed(
                            title='Lottery', description="Congratulations you have bought yourself a ticket to the upcoming lottery!", color=0x00ff00)
                        await ctx.channel.send(embed=embedVar)   
                        return
                    else:
                        embedVar = discord.Embed(
                            title='Lottery', description="You can afford these tickets but you can only buy " + str(100 - allLottery[account['name']]) + ' tickets!', color=0x00ff00)
                        await ctx.channel.send(embed=embedVar)   
                        return
            else:
                embedVar = discord.Embed(
                    title='Lottery', description="You don't have enough funds to buy " + arg2 + " tickets.\n\nYou can purchase up to" + str(int(account['value']/TICKET_PRICE)) + " tickets.", color=0x00ff00)
                await ctx.channel.send(embed=embedVar)   
                return
    
# leaderboard
@bot.command(
    profile="leaderboard",
    brief="leaderboard"
)
async def leaderboard(ctx):
    leaderboard = []
    
    with open("data/stonks.json", "r") as file:
        liveStonks = json.load(file)

    accounts = readAccountsFromDb()
    for _account in accounts:

        assetValue = 0

        myStonks = ""

        for _stonk in _account['stonks']:
            for liveStonk in liveStonks:
                if liveStonk['stonk'] == _stonk['stonk']:
                    haveStonk = liveStonk

            for _own in _stonk['own']:
                myStonks += "  " + str(_own['quantity']) + " " + _stonk['stonk'] + " shares at $" + "{:,.2f}".format(_own['priceBoughtAt']) + "\n"
                assetValue += float(_own['quantity']) * float(haveStonk['value'])
        netWorth = float(assetValue) + float(_account['value'])
        leaderboard.append((_account['name'], netWorth ))
    
    leaderboard.sort(key = sortSecond, reverse = True)
    
    showLeaderBoard = ''
    
    for leader in leaderboard:
        showLeaderBoard += str(leader[0]) + " : ${:,.2f}".format(leader[1])+'\n'
    
    embedVar = discord.Embed(
            title='Leaderboard', description="**Net Worth**\n\n" +str(showLeaderBoard), color=0x00ff00)       
    await ctx.channel.send(embed=embedVar)


def sortSecond(val):
    return val[1]


# sell stonks
'''
@bot.command(
    profile="leaderboard",
    brief="leaderboard"
)
async def blackjack(ctx, arg1 = 'setup', arg2 = '-1'):
    with open("data/blackJack.json", "r") as file:
        blackJackSession = json.load(file)
    if (arg1 == 'setup'):
        if (blackJackSession[0]['status'] == 'inProgress'):
            embedVar = discord.Embed(
                title='Blackjack', description='There is a game already in progress\n\nYou must wait till the game is over', color=0x00ff00)
            await ctx.channel.send(embed=embedVar)
            return
        elif (blackJackSession[0]['status'] == 'lobby'):
            embedVar = discord.Embed(
                    title='Blackjack', description='There is already a lobby created.\n\n**To join use !blackjack join {wager}**', color=0x00ff00)
            await ctx.channel.send(embed=embedVar)
            return
        elif (blackJackSession[0]['status'] == 'null'):
            blackJackSession[0]['status'] = 'lobby' 
            embedVar = discord.Embed(
                    title='Blackjack', description='You just created a black jack lobby.\n\n**You and others may join using !blackjack join {wager}**\n\nTo start the game do !blackjack start', color=0x00ff00)
            await ctx.channel.send(embed=embedVar)
    elif (arg1 == 'join' and arg2.isnumeric() and int(arg2) > 0):
        if (blackJackSession[0]['status'] == 'inProgress'):
            embedVar = discord.Embed(
                title='Blackjack', description='You cannot join a game in progress.\n\nYou must wait till the game is over', color=0x00ff00)
            await ctx.channel.send(embed=embedVar)
            return
        elif (blackJackSession[0]['status'] == 'lobby'):
            ## ADD MY NAME AND WAGER TO BLACKJACK.JSON
            embedVar = discord.Embed(
                    title='Blackjack', description='You have joined the lobby!', color=0x00ff00)
            await ctx.channel.send(embed=embedVar)
            return
        elif (blackJackSession[0]['status'] == 'null'):
            embedVar = discord.Embed(
                    title='Blackjack', description='There is no black jack lobby\n\n**To create a lobby do !blackjack setup**', color=0x00ff00)
            await ctx.channel.send(embed=embedVar)
    elif (arg1 == 'start'):
        if (blackJackSession[0]['status'] == 'inProgress'):
            embedVar = discord.Embed(
                title='Blackjack', description='You cannot start a game in progress.\n\nYou must wait till the game is over', color=0x00ff00)
            await ctx.channel.send(embed=embedVar)
            return
        elif (blackJackSession[0]['status'] == 'lobby'):
            ## PRINT WHO IS IN THE GAME
            blackJackSession[0]['status'] = 'inProgress'
            embedVar = discord.Embed(
                    title='Blackjack', description='You have started the game!', color=0x00ff00)
            await ctx.channel.send(embed=embedVar)
            return
        elif (blackJackSession[0]['status'] == 'null'):
            embedVar = discord.Embed(
                    title='Blackjack', description='You cannot start a game without a lobby\n\n**To create a lobby do !blackjack setup**', color=0x00ff00)
            await ctx.channel.send(embed=embedVar)
    elif (arg1 == 'hit'):
        if (blackJackSession[0]['status'] == 'inProgress'):
            ## CHECK TO SEE IF IM IN GAME
            ## CHECK TO SEE MY STATUS ('alive', 'busted')
            ## GRAB MY ACCOUNTS HAND
            ## ADD RANDOM CARD
            ## CHECK TO SEE IF > 21 BUST
            ## ELSE ADD CARD TO HAND
            ## CHECK TO SEE 
            embedVar = discord.Embed(
                title='Blackjack', description='You cannot start a game in progress.\n\nYou must wait till the game is over', color=0x00ff00)
            await ctx.channel.send(embed=embedVar)
            return
        elif (blackJackSession[0]['status'] == 'lobby'):
            embedVar = discord.Embed(
                    title='Blackjack', description='The game is not yet started.', color=0x00ff00)
            await ctx.channel.send(embed=embedVar)
            return
        elif (blackJackSession[0]['status'] == 'null'):
            embedVar = discord.Embed(
                    title='Blackjack', description='There is not a game created.', color=0x00ff00)
            await ctx.channel.send(embed=embedVar)
    elif (arg1 == 'stay'):
        if (blackJackSession[0]['status'] == 'inProgress'):
            ## CHECK TO SEE IF IM IN GAME
            ## CHECK TO SEE MY STATUS ('alive', 'busted')
            ## GRAB MY ACCOUNTS HAND
            ## ADD RANDOM CARD
            ## CHECK TO SEE IF > 21 BUST
            ## ELSE ADD CARD TO HAND
            embedVar = discord.Embed(
                title='Blackjack', description='You cannot start a game in progress.\n\nYou must wait till the game is over', color=0x00ff00)
            await ctx.channel.send(embed=embedVar)
            return
        elif (blackJackSession[0]['status'] == 'lobby'):
            embedVar = discord.Embed(
                    title='Blackjack', description='The game is not yet started.', color=0x00ff00)
            await ctx.channel.send(embed=embedVar)
            return
        elif (blackJackSession[0]['status'] == 'null'):
            embedVar = discord.Embed(
                    title='Blackjack', description='There is not a game created.', color=0x00ff00)
            await ctx.channel.send(embed=embedVar)
        
 '''   

# Display Profile
def displayProfile(account, author_avatar_url):
    
    with open("data/stonks.json", "r") as file:
        liveStonks = json.load(file)

    embedVar = discord.Embed(title=account['name'], description=account['job']['jobTitle'] +
                             " ( $" + "{:,.2f}".format(account['job']['rate']) + " per/hour)", color=0x00ff00)
    embedVar.set_thumbnail(url=author_avatar_url)
    embedVar.add_field(name="Bank", value="$" +
                       "{:,.2f}".format(account['value']), inline=False)
    embedVar.add_field(name="Bitch of the day", value=account['bitch']['name'] + " (" + str(
        account['bitch']['value']) + ")", inline=False)
    
    assetValue = 0

    myStonks = ""

    for _stonk in account['stonks']:
        for liveStonk in liveStonks:
            if liveStonk['stonk'] == _stonk['stonk']:
                haveStonk = liveStonk

        for _own in _stonk['own']:
            myStonks += "  " + str(_own['quantity']) + " " + _stonk['stonk'] + " shares at $" + "{:,.2f}".format(_own['priceBoughtAt']) + "\n"
            assetValue += float(_own['quantity']) * float(haveStonk['value'])

    if (myStonks != ""):
        embedVar.add_field(name="Asset Value", value="${:,.2f}".format(assetValue), inline=False)
        embedVar.add_field(name="Stonks", value=myStonks, inline=False)
    else:
        embedVar.add_field(name="Stonks", value='You have no stonks.', inline=False)
    return embedVar


# Display Simple Profile
def displaySimpleProfile(account, author_avatar_url):
    
    embedVar = discord.Embed(title=account['name'], description='', color=0x00ff00)
    embedVar.set_thumbnail(url=author_avatar_url)
    embedVar.add_field(name="Bank", value="$" +
                       "{:,.2f}".format(account['value']), inline=False)
    return embedVar


# Read Accounts
def readAccountsFromDb():
    with open("data/accounts.json", "r") as file:
        accounts = json.load(file)
    return accounts

# Read Stonks
def readStonksFromDb():
    with open("data/stonks.json", "r") as file:
        allStonks = json.load(file)
    return allStonks


# Write to Account Database
def writeToAccountDb(accountToWrite):
    with open("data/accounts.json", "r") as file:
        accounts = json.load(file)

    name = accountToWrite['name']
    index = -1
    for account in accounts:
        if (account['name'] == name):
            index = accounts.index(account)

    if (index != -1):
        accounts[index] = accountToWrite
    else:
        accounts.append(accountToWrite)

    with open("data/accounts.json", "w") as file:
        json.dump(accounts, file)


# Caculating the bitches value
async def bitchesValue(value, currentNetWorth, bitch, ctx):
    ALL_BITCH_TRAITS = ['keep_job', 'best_job', 'card_count', 'finese_the_dealer', 'slight_of_hand']
    randomTrait = random.choice(ALL_BITCH_TRAITS)
    if (value == 0):
        embedVar = discord.Embed(
            title='STINKY BITCH', description="UH OH YOU GOT STINKY BITCH. SHE IS ONLY DATING YOU FOR YOUR MONEY. SHE WANTS A DIVORCE ALREADY.\n\n**1/2X NET WORTH**", color=0x00ff00)
        await ctx.channel.send(embed=embedVar)
        return currentNetWorth * 0.5
    elif (value < 20):
        embedVar = discord.Embed(
            title='GOLD DIGGER', description="Sheeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeesh. Bitch maxed out all your credit cards.\n\n**-20% NET WORTH**", color=0x00ff00)
        await ctx.channel.send(embed=embedVar)
        return currentNetWorth * 0.8
    elif (value < 40):
        bitch['traits'].append(randomTrait)
        embedVar = discord.Embed(
            title='F', description="She likes yo ass... but you were caught looking at her mom. She steals the car, the kids, and your collection of The Bee Movies you have in the living room.\n\n**-10% NET WORTH**\n\nTraits: " + bitch['traits'][0], color=0x00ff00)
        await ctx.channel.send(embed=embedVar)
        return currentNetWorth * 0.9
    elif (value < 60):
        bitch['traits'].append(randomTrait)
        embedVar = discord.Embed(
            title='Baddie', description="You find a nice baddie. She is a 6th grade teachers but provides no monetary gain to your life.\n\n**+0% NET WORTH**\n\nTraits: " + bitch['traits'][0], color=0x00ff00)
        await ctx.channel.send(embed=embedVar)
        return currentNetWorth
    elif (value < 80):
        bitch['traits'].append(randomTrait)
        ALL_BITCH_TRAITS.remove(randomTrait)
        secondTrait = random.choice(ALL_BITCH_TRAITS)
        bitch['traits'].append(secondTrait)
        embedVar = discord.Embed(
            title='She do be kinda smart', description="She got KNOWLEDGE. And she BAD? She posts regular instagram posts quoted \"Live, Laugh, Love.\" under a picture of her butt cheeks.\n\n**+10% NET WORTH**\n\nTraits: " + bitch['traits'][0] + " , " + bitch['traits'][1], color=0x00ff00)
        await ctx.channel.send(embed=embedVar)
        return currentNetWorth * 1.1
    elif (value < 99):
        bitch['traits'].append(randomTrait)
        ALL_BITCH_TRAITS.remove(randomTrait)
        secondTrait = random.choice(ALL_BITCH_TRAITS)
        bitch['traits'].append(secondTrait)
        embedVar = discord.Embed(
            title='Baddest bitch in da club', description="She's an only fans model. Making millions herself. All the homies want her, and all the girls want to be her.\n\n**+20% NET WORTH**\n\nTraits: " + bitch['traits'][0] + " , " + bitch['traits'][1], color=0x00ff00)
        await ctx.channel.send(embed=embedVar)
        return currentNetWorth * 1.2
    elif (value == 100):
        bitch['traits'].append(randomTrait)
        ALL_BITCH_TRAITS.remove(randomTrait)
        secondTrait = random.choice(ALL_BITCH_TRAITS)
        bitch['traits'].append(secondTrait)
        
        ALL_BITCH_TRAITS.remove(secondTrait)
        thirdTrait = random.choice(ALL_BITCH_TRAITS)
        bitch['traits'].append(thirdTrait)
        embedVar = discord.Embed(
            title='MEGA BAD BITCH', description="You've found the one. She a billionaire herself. She is yo sugar mama.\n\n**2X NET WORTH**\n\nTraits: " + bitch['traits'][0] + " , " + bitch['traits'][1] + " , " + bitch['traits'][2], color=0x00ff00)
        await ctx.channel.send(embed=embedVar)
        return currentNetWorth * 2
    else:
        return currentNetWorth


# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.
bot.run(token)
