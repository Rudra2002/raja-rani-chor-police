import discord
import random
import asyncio

TOKEN = "discord-token "
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
        await message.channel.send(
            "Welcome to Chor Dakat! Please remove your \U0001f45e outside and enter by opening \U0001f6aa.")
        eemojichannel = message.channel
        async for msge in eemojichannel.history(limit=1):
            if msge != message:
                await msge.add_reaction("\U0001f6aa")

        def check(reaction, user):

            return user != client.user and str(reaction.emoji) == "\U0001f6aa" and len(players) < 6

        while len(players) < 6:
            try:
                reaction, user = await client.wait_for('reaction_add', timeout=10.0, check=check)
            except asyncio.TimeoutError:
                break
            else:
                if user.name in players:
                    await message.remove_reaction("\U0001f6aa", user)
                    continue
                playersnum += 1
                players.append(user.name)
        await message.channel.send(f"Got {playersnum} players: {', '.join(players)}")

        await message.channel.send("Starting in 5 seconds...")
        await asyncio.sleep(1)
        for i in range(4, 0, -1):
            await message.channel.send(f"{i}...")
            await asyncio.sleep(1)
        await message.channel.send("Pick your card!")
        emojis = random.sample(
            [u"\U0001f409", u"\U0001f31a", u"\U0001f52b", u"\U0001f341", u"\U0001f433", u"\U0001f34e"], playersnum)
        emojichannel = message.channel
        async for msg in emojichannel.history(limit=1):
            if msg != message:
                for emoji in emojis:
                    await msg.add_reaction(emoji)

        card_values = random.sample(["Babu", "Fake babu", "Dalal", "Police", "chor", "Dakat"], playersnum)

        assigned_cards = []
        for i in range(playersnum):

            def check(reaction, user):
                return user != client.user and str(
                    reaction.emoji) in emojis and user.name not in assigned_cards and user.name in players and reaction.count != 0

            reaction, user = await client.wait_for('reaction_add', check=check)
            player_index = emojis.index(str(reaction.emoji))

            assigned_cards.append(user.name)
            card_value = card_values[player_index]

            embed = discord.Embed(title=f"Your card: {card_value}")
            gif_url = ""
            if card_value == "Babu":
                gif_url = "https://media.tenor.com/i09hWnL0i0gAAAAC/rich-money.gif"
            elif card_value == "Fake babu":
                gif_url = "https://media.tenor.com/AjCT-xzbhwsAAAAC/fake-seinfeld.gif"
            elif card_value == "Dalal":
                gif_url = "https://media3.giphy.com/media/aZcwYGaPOGJsLeLFfC/giphy.gif?cid=6c09b952xzmov1jnn0e17y6xot14yrowfkco3qgyi47j7ymx&ep=v1_gifs_search&rid=giphy.gif&ct=g"
            elif card_value == "Police":
                gif_url = "https://media.tenor.com/k6kuG5YqLrQAAAAM/police-dance.gif"
            elif card_value == "police":
                gif_url = "https://media.giphy.com/media/Hg3q8zEi9sqvuzRzCO/giphy.gif"
            elif card_value == "chor":
                gif_url = "https://media.tenor.com/VC30cOLxNcwAAAAM/family-guy.gif"
            elif card_value == "Dakat":
                gif_url = "https://media.tenor.com/IknEM_m7vEAAAAAd/sigma-male-breaking-bad.gif"
            embed.set_image(url=gif_url)

            await user.send(embed=embed)
            await reaction.remove(client.user)

            await reaction.remove(user)
            await message.remove_reaction(reaction, client.user)

            del emojis[player_index]
            del card_values[player_index]
        await message.channel.send("Game Ended\U0001F480")


client.run(TOKEN)
