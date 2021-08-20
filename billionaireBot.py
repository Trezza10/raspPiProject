import discord
from discord.ext import commands
import json
from datetime import datetime
import re

today = datetime.today()
print("Today's date:", today)


file = open('token.txt')
token = file.read()
print(token)
file.close()

file2 = open('birthdays.json')
birthdays = json.load(file2)
print(birthdays)
file2.close()

"""
for user in birthdays:
    birthday = datetime.strptime(user['date'], '%Y-%m-%d')
    if (birthday.day == today.day and birthday.month == today.month) :
        print('it is your birthday today, ' + user['name'])
        print(today.day, today.month)
    else:
        print('it is not your birthday' + user['name'])
"""
channelId = 864619752991096833


# CREATES A NEW BOT OBJECT WITH A SPECIFIED PREFIX. IT CAN BE WHATEVER YOU WANT IT TO BE.
bot = commands.Bot(command_prefix="!")

@bot.command(
	addBirthday="Add a birthday in the format: YYYY-MM-DD",
	brief="Add your birthday"
)
async def addBirthday(ctx, arg):
    if (re.match('^[0-9]{4}-[0-9]{2}-[0-9]{2}$', arg)):
        mention = ctx.message.author.mention
        response = f"Writing {mention}'s birthday to the db"

        with open("birthdays.json", "r+") as file:
            data = json.load(file)
            newEntry = {}
            newEntry['name'] = str(ctx.message.author)
            newEntry['date'] = str(arg)
            data.append(newEntry)
            json.dump(data, file)

        await ctx.channel.send(response)
    else:
        await ctx.channel.send('not valid birthday')

# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.
bot.run(token)