import main
from discord.ext import commands
import dotenv
import os
from discord import app_commands
import discord
import asyncio
import time
from tabulate import tabulate

dotenv.load_dotenv()
KEY = os.environ.get("DISCORD_TOKEN")



bot = discord.Client(intents=discord.Intents.default(), command_prefix='!')


@bot.event
async def on_ready():
    await bot.wait_until_ready()
    await tree.sync()
    asyncio.create_task(update())

    print("{0.user} is online!".format(bot))


tree = app_commands.CommandTree(bot)

async def update():
    while True:
        global df
        df = ""
        df = main.main()
        table = tabulate(df, headers='keys', tablefmt='psql')
        open('table.txt', 'w').write(f'```{table}```')

        await asyncio.sleep(10)


@tree.command(name='get_versions', description='prints all versions')
async def get_versions(interaction: discord.Interaction):
    global df
    print(df + '\n')
    table = tabulate(df, headers='keys', tablefmt='psql')

    await interaction.response.send_message(f'```{table}```')




bot.run(KEY)
