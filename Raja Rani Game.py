import discord
import random
import asyncio
TOKEN = "Enter Your Disocrd token"
intents = discord.Intents.all()  # this will enable all the intents

client = discord.Client(intents=intents)
@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.content.startswith('!start'):
        playersnum = 0
        players = []
        await message.channel.send("Welcome to Chor Dakat! Please remove your \U0001f45e outside and enter by opening \U0001f6aa.")
        eemojichannel = message.channel
        async for msge in eemojichannel.history(limit=1):
            if msge != message:
                    await msge.add_reaction("\U0001f6aa")

        def check(reaction, user):
            return user != client.user and str(reaction.emoji) != '' and len(players) < 6
        while len(players) < 6:
            try:
                reaction, user = await client.wait_for('reaction_add', timeout=10.0, check=check)
            except asyncio.TimeoutError:
                break
            else:
                playersnum += 1
                players.append(user.name)
        await message.channel.send(f"Got {playersnum} players: {', '.join(players)}")
        
        await message.channel.send("Starting in 5 seconds...")
        await asyncio.sleep(1)
        for i in range(4, 0, -1):
            await message.channel.send(f"{i}...")
            await asyncio.sleep(1)
        await message.channel.send("Pick your card!")
        emojis = random.sample([u"\U0001f409", u"\U0001f31a", u"\U0001f52b", u"\U0001f341", u"\U0001f433", u"\U0001f34e"], playersnum)
        emojichannel = message.channel
        async for msg in emojichannel.history(limit=1):
            if msg != message:
                for emoji in emojis:
                    await msg.add_reaction(emoji)

        card_values = random.sample(["Babu", "Fake babu", "Dalal", "Police", "chor", "Dakat"], playersnum)
        
        def check(reaction, user):
            return user != client.user and str(reaction.emoji) in emojis and user.name in players and reaction.count == 2
        
        for i in range(playersnum):
            reaction, user = await client.wait_for('reaction_add', check=check)
            player_index = emojis.index(str(reaction.emoji))
            await user.send(f"You got {card_values[player_index]}!")
            del emojis[player_index]
            del card_values[player_index]
            
client.run(TOKEN)