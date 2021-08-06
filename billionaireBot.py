import discord
from datetime import date

today = date.today()
print("Today's date:", today)

token = "ODcyMjM2NzI2NTUzMjgwNTQy.YQm7wA.m8MqpJz37_XF1Y8bvlwUyz7FKCw"
channelId = 864619752991096833

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)
        await self.scheduled_message()

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send(today)

    async def scheduled_message(self):
        channel = client.get_channel(channelId)
        channel.send("Message")

client = MyClient()
client.run(token)