import os
import random

import discord
import dotenv
from discord.ext import commands, tasks

dotenv.load_dotenv()

# imports things needed for bot (modules needed)

member = discord.Member

Game = discord.Game

Streaming = discord.Streaming

idle = discord.Status.idle

dnd = discord.Status.dnd

randomc = random.choice

intents = discord.Intents.default()
intents.presences = True
intents.members = True
intents.message_content = True

client = commands.Bot(command_prefix=[
                      'm?', 'M?'], intents=intents, help_command=None, case_insensitive=True)


@client.event
async def on_ready():
    print(f"logged into {client.user.name}")


statuses = ""


@tasks.loop(seconds=120)
async def update_presence():
    statuses = [f"My Ping! {round (client.latency * 1000)} ms",
                f"Some Servers, {len(client.guilds)}", "Klassick | https://dsc.gg/klassick"]
    await client.change_presence(status=dnd, activity=discord.Activity(type=discord.ActivityType.watching, name=randomc(statuses)))


@update_presence.before_loop
async def before_update_presence():
    await client.wait_until_ready()

update_presence.start()


for file in os.listdir('cogs'):
    if file.endswith('.py'):
        client.load_extension(f'cogs.' + file[:-3])


client.run(os.getenv("TOKEN"))
