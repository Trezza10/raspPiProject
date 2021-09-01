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

channelId = 864619752991096833
BOT_IMAGE = 'https://www.media3.hw-static.com/wp-content/uploads/xx_55026731-638x425-638x425.jpeg'

file = open('./../token.txt')
token = file.read()
file.close()


with open("bitches.json", "r") as file:
    allBitches = json.load(file)


with open("jobs.json", "r") as file:
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

    with open("accounts.json", "r") as file:
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

    with open("accounts.json", "r") as file:
        accounts = json.load(file)

    name = ctx.message.author.name
    index = -1
    for account in accounts:
        if (account['name'] == name):
            index = accounts.index(account)

    if (index == -1):
        account = {}
        account['name'] = ctx.message.author.name
        account['job'] = {'jobTitle': 'Jobless', 'rate': 0}
        account['value'] = 0.00
        account['debt'] = 0.00
        account['bitch'] = {'name': 'Nobody', 'value': 0, 'date': -1}
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
async def bitch(ctx, arg1 = 'show'):
    if (arg1 == 'get'):
        today = int(datetime.datetime.now().day)
        accounts = readAccountsFromDb()
        for _account in accounts:
            if _account['name'] == ctx.message.author.name:
                account = _account
                break
        if (account['bitch']['date'] < today):
            randomBitch = allBitches[random.randint(0, len(allBitches)-1)]
            randomBitchValue = random.randint(0, 100)
            account['bitch']['name'] = randomBitch
            account['bitch']['value'] = randomBitchValue
            account['bitch']['date'] = today
            currentNetWorth = account['value']
            account['value'] = await bitchesValue(randomBitchValue, currentNetWorth, ctx)
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
        embedVar = discord.Embed(
                title=account['bitch']['name'], description=str(account['bitch']['name']) + ' is yo bitch for now.\n\nYour anniversary is September ' + str(account['bitch']['date']) +'.\n\nShe is ' + str(account['bitch']['value']) + ' value.', color=0x00ff00)
        await ctx.channel.send(embed=embedVar)
    else:
        embedVar = discord.Embed(title='Incorrect bitches command',
                             description='Use the following:\n\n!bitch show\n\n!bitch get', color=0x00ff00)
        await ctx.channel.send(embed=embedVar)
        

# The stonks boi
@bot.command(
    profile="stonks",
    brief="stonks"
)
async def stonks(ctx, arg1 = 'show', arg2 = '-1', arg3 = '-1'):
    if (arg1 == 'show' and arg2 == '-1' and arg3 == '-1'):
        embedVar = discord.Embed(title='BillionaireBot',
                                description='Stonks on the market', color=0x00ff00)
        embedVar.set_thumbnail(url=BOT_IMAGE)

        allStonks = readStonksFromDb()

        i = 1
        for stonk in allStonks:
            stonkName = stonk['stonk']
            stonkValue = stonk['value']
            embedVar.add_field(name="[" + str(i) + "] " + stonkName,
                            value="$" + str(stonkValue) + " ", inline=False)
            i += 1

        await ctx.channel.send(embed=embedVar)
        
        file = discord.File("demo.png")
        e = discord.Embed()
        e.set_image(url="attachment://demo.png")
        await ctx.send(file = file, embed=e)
    elif (arg1 == 'buy'):
        if (arg2.isnumeric() and arg3.isnumeric()):
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
async def jobs(ctx, arg1 = 'show', arg2 = '-1'):
    if (arg1 == 'show' and arg2 == '-1'):
        embedVar = discord.Embed(title='BillionaireBot',
                                description='Jobs on the market', color=0x00ff00)
        embedVar.set_thumbnail(url=BOT_IMAGE)

        i = 1
        for job in allJobs:
            jobName = job['name']
            jobRate = job['rate']
            embedVar.add_field(name="[" + str(i) + "] " + jobName,
                            value="$" + str(jobRate) + " per hour", inline=False)
            i += 1

        await ctx.channel.send(embed=embedVar)
    elif (arg1 == 'get' and arg2.isnumeric()):
        await getAJob(ctx, arg2)
    else:
        embedVar = discord.Embed(title='Incorrect jobs command',
                             description='Use the following:\n\n!jobs\n\n!jobs get x(job #)', color=0x00ff00)
        await ctx.channel.send(embed=embedVar)


# get a job
async def getAJob(ctx, args):
    if (args.isnumeric()):
        job = int(args) - 1
        if not(0 <= job < len(allJobs)):
            return

    accounts = readAccountsFromDb()
    for _account in accounts:
        if _account['name'] == ctx.message.author.name:
            account = _account
            break

    account['job']['jobTitle'] = allJobs[job]['name']
    account['job']['rate'] = allJobs[job]['rate']

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

    with open("stonks.json", "r") as file:
        allStonks = json.load(file)

    if (arg1.isnumeric() and arg2.isnumeric()):
        _stonk = int(arg1) - 1
        if not(0 <= _stonk < len(allStonks)):
            return

    accounts = readAccountsFromDb()
    for _account in accounts:
        if _account['name'] == ctx.message.author.name:
            account = _account
            break
    # enough money?
    if (account['value'] >= allStonks[int(arg1)]['value'] * int(arg2)):
        # Loop through all your stonks
        haveStonk = False
        for _stonk in account['stonks']:
            # check to see if you already have stonk of it
            if allStonks[int(arg1)]['stonk'] == _stonk['stonk']:
                haveStonk = True
                # append x stonks to list of that
                _stonk['own'].append(
                    {
                        'priceBoughtAt': allStonks[int(arg1)]['value'],
                        'quantity': int(arg2)
                    }
                )
                print(_stonk)

        if not(haveStonk):
            account['stonks'].append(
                {
                    'stonk': allStonks[int(arg1)]['stonk'],
                    'own': [
                        {
                            'priceBoughtAt': allStonks[int(arg1)]['value'],
                            'quantity': int(arg2)
                        }
                    ]
                }
            )
        # Deduct moneys
        account['value'] -= allStonks[int(arg1)]['value'] * int(arg2)
        embedVar = displayProfile(account, ctx.message.author.avatar_url)
        writeToAccountDb(account)

        await ctx.channel.send(embed=embedVar)




# sell stonks
async def sellStonks(ctx, arg1):
    print(arg1)

    with open("stonks.json", "r") as file:
        allStonks = json.load(file)

    if (arg1.isnumeric()):
        _stonk = int(arg1) - 1
        if not(0 <= _stonk < len(allStonks)):
            return

    accounts = readAccountsFromDb()
    for _account in accounts:
        if _account['name'] == ctx.message.author.name:
            account = _account
            break
    
    # Loop through all your stonks
    for _stonk in account['stonks']:
        # check to see if you already have stonk of it
        if allStonks[int(arg1)]['stonk'] == _stonk['stonk']:
            for own in _stonk['own']:
                account['value'] += ((own['priceBoughtAt'] - allStonks[int(arg1)]['value']) * -1 * own['quantity'])
                embedVar = displayProfile(account, ctx.message.author.avatar_url)

            account['stonks'].remove(_stonk) 
        
    writeToAccountDb(account)
    await ctx.channel.send(embed=embedVar)



# sell stonks
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
            title='Not enough funds', description="You can do a maximum of " + str(account['value']) + ' dollars', color=0x00ff00)
        await ctx.channel.send(embed=embedVar)
        return
    
    _coinFlip = random.randint(0,1)
    
    if (_coinFlip == 1):
        account['value'] += int(arg1)
        embedVar = discord.Embed(
            title='Coin flip', description="You won " + str(arg1) + " dollars!", color=0x00ff00)
    else:
        account['value'] -= int(arg1)
        embedVar = discord.Embed(
            title='Coin flip', description="You lost " + str(arg1) + " dollars!", color=0x00ff00)
     
    writeToAccountDb(account)

    await ctx.channel.send(embed=embedVar)

    embedVar = displayProfile(account, ctx.message.author.avatar_url)

    await ctx.channel.send(embed=embedVar)
        
    



# Display Profile
def displayProfile(account, author_avatar_url):
    embedVar = discord.Embed(title=account['name'], description=account['job']['jobTitle'] +
                             " ( $" + str(account['job']['rate']) + " per/hour)", color=0x00ff00)
    embedVar.set_thumbnail(url=author_avatar_url)
    embedVar.add_field(name="Value", value="$" +
                       str(account['value']), inline=False)
    #embedVar.add_field(name="Debt", value="$" + str(account['debt']), inline=False)
    embedVar.add_field(name="Bitch of the day", value=account['bitch']['name'] + " (" + str(
        account['bitch']['value']) + ")", inline=False)
    
    
    myStonks = ""
    for _stonk in account['stonks']:
        for _own in _stonk['own']:
            myStonks += "  " + str(_own['quantity']) + " " + _stonk['stonk'] + " shares at $" + str(
                str(_own['priceBoughtAt'])) + "\n"

    embedVar.add_field(name="Stonks", value=myStonks, inline=False)
    return embedVar


# Read Accounts
def readAccountsFromDb():
    with open("accounts.json", "r") as file:
        accounts = json.load(file)
    return accounts

# Read Stonks
def readStonksFromDb():
    with open("stonks.json", "r") as file:
        allStonks = json.load(file)
    return allStonks


# Write to Account Database
def writeToAccountDb(accountToWrite):
    with open("accounts.json", "r") as file:
        accounts = json.load(file)

    name = accountToWrite['name']
    index = -1
    for account in accounts:
        if (account['name'] == name):
            index = accounts.index(account)

    with open("accounts.json", "w") as file:

        if (index != -1):
            accounts[index] = accountToWrite
        else:
            accounts.append(accountToWrite)

        json.dump(accounts, file)


# Caculating the bitches value
async def bitchesValue(value, currentNetWorth, ctx):
    if (value == 0):
        embedVar = discord.Embed(
            title='STINKY BITCH', description="UH OH YOU GOT STINKY BITCH. SHE IS ONLY DATING YOU FOR YOUR MONEY. SHE WANTS A DIVORCE ALREADY.\n\n**1/2X NET WORTH**", color=0x00ff00)
        await ctx.channel.send(embed=embedVar)
        return currentNetWorth * 0.5
    elif (value < 10):
        embedVar = discord.Embed(
            title='GOLD DIGGER', description="Sheeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeesh. Bitch maxed out all your credit cards.\n\n**-20% NET WORTH**", color=0x00ff00)
        await ctx.channel.send(embed=embedVar)
        return currentNetWorth * 0.8
    elif (value < 30):
        embedVar = discord.Embed(
            title='F', description="She likes yo ass... but you were caught looking at her mom. She steals the car, the kids, and your collection of The Bee Movies you have in the living room.\n\n**-10% NET WORTH**", color=0x00ff00)
        await ctx.channel.send(embed=embedVar)
        return currentNetWorth * 0.9
    elif (value < 70):
        embedVar = discord.Embed(
            title='Baddie', description="You find a nice baddie. She is a 6th grade teachers but provides no monetary gain to your life.\n\n**+0% NET WORTH**", color=0x00ff00)
        await ctx.channel.send(embed=embedVar)
        return currentNetWorth
    elif (value < 90):
        embedVar = discord.Embed(
            title='She do be kinda smart', description="She got KNOWLEDGE. And she BAD? She posts regular instagram posts quoted \"Live, Laugh, Love.\" under a picture of her butt cheeks.\n\n**+10% NET WORTH**", color=0x00ff00)
        await ctx.channel.send(embed=embedVar)
        return currentNetWorth * 1.1
    elif (value < 99):
        embedVar = discord.Embed(
            title='Baddest bitch in da club', description="She's an only fans model. Making millions herself. All the homies want her, and all the girls want to be her.\n\n**+20% NET WORTH**", color=0x00ff00)
        await ctx.channel.send(embed=embedVar)
        return currentNetWorth * 1.2
    elif (value == 100):
        embedVar = discord.Embed(
            title='MEGA BAD BITCH', description="You've found the one. She a billionaire herself. She is yo sugar mama.\n\n**2X NET WORTH**", color=0x00ff00)
        await ctx.channel.send(embed=embedVar)
        return currentNetWorth * 2
    else:
        return currentNetWorth


# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.
bot.run(token)
