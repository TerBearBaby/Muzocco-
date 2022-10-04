from abc import ABC

import discord
import os
import dotenv
from discord.ext import tasks
import random
from itertools import cycle

dotenv.load_dotenv()


class Client(discord.Bot, ABC):
    """
    The base class for the bot. This inherits from discord.Bot, it allows us to
    extend the client object to our needs and liking.
    """

    def __init__(self):
        super().__init__(
            intents=discord.Intents.all(),
        )
        self.statuses = cycle([
            "My Ping! {latency} ms",
            "Some Servers, {guild_count}",
            "Klassick | https://dsc.gg/klassick"
        ])  # Create a cycle, so we can simply use next() to get the next status.

    def load_exts(self):
        for ext in os.listdir("cogs"):
            if ext.endswith(".py"):
                self.load_extension(f"cogs.{ext[:-3]}")
                print(f"Loaded {ext[:-3]}")

    async def on_ready(self):
        """
        Instead of having to use @client.event decorators, we can simply add/overwrite
        methods on the client object. This is a lot cleaner and easier to read.
        """
        self.load_exts()
        print(f"Logged in as {self.user.name}")
        self.update_presence.start()

    @tasks.loop(seconds=60)
    async def update_presence(self):
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=next(self.statuses).format(guild_count=len(self.guilds), latency=round(self.latency * 1000))
            )
        )

    def run(self):
        super().run(os.getenv("TOKEN"))

