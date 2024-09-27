import asyncio

from ebaysdk.finding import Connection as Finding
import pymysql.cursors
from datetime import datetime

import discord
from discord.ext import commands

key = open("key.txt", "r").read()

def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


token = read_token()
bot = commands.Bot(command_prefix='.', intents=discord.Intents().all())


@bot.event
async def on_connect():
    print('Bot connected')


@bot.event
async def on_disconnect():
    print('Bot disconnected')


@bot.event
async def on_ready():
    # When bot is ready, send ready message
    print(f'Logged in as {bot.user.name} ({bot.user.id})\n\nLogged in Guilds:')
    for guild in bot.guilds:
        print(f'{guild} ({guild.id})')

    on_ready_channels = [
        864566842076561458
    ]

    for on_ready_channels in on_ready_channels:
        ch = bot.get_channel(on_ready_channels)
        embed = discord.Embed(title='Bot Connected', color=0x3498db, timestamp=datetime.utcnow())
        await ch.send(embed=embed)


@bot.command(name='search')
async def saerchebay(ctx, entries, *, query):
    await ctx.send(f'Loading search results for `{query}`')

    api = Finding(domain='svcs.sandbox.ebay.com', appid=key, config_file=None)
    response = api.execute('findItemsAdvanced', {'keywords': query})

    d = response.dict()

    for index in range(0, int(entries)):
        embed = discord.Embed(title=f'Item {index+1} Properties 📥', color=0x3498db, timestam=datetime.utcnow())

        item_properties = [
            ('Title', d['searchResult']['item'][index]['title']),  # item title
            ('Item ID', d['searchResult']['item'][index]['itemId']),  # item ID
            ('Price', f"${d['searchResult']['item'][index]['sellingStatus']['currentPrice']['value']}"),  # item price
        ]
        # Cycle through different product properties and add to embeded message
        for name, value in item_properties:
            embed.add_field(name=f'{name}', value=f"```{value}```", inline=False)

        embed.add_field(name=f'Product Listing Link',
                        value=f"[Click here]({d['searchResult']['item'][index]['viewItemURL']})")  # URL to view item

        await ctx.send(embed=embed)


# Runs bot with token
bot.run(token)
