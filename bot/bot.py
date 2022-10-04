from abc import ABC

import discord
import os
import dotenv
from discord.ext import tasks
from itertools import cycle
import logging

dotenv.load_dotenv()


class Client(discord.Bot, ABC):
    """
    The base class for the bot. This inherits from discord.Bot, it allows us to
    extend the client object to our needs and liking.
    """

    def __init__(self):
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        self.logger = logging.getLogger("bot")
        if os.getenv("DEV"):
            super().__init__(
                intents=discord.Intents.all(),
                debug_guilds=[int(os.getenv("DEV_GUILD"))],
            )
            self.logger.info("Running in dev mode.")
        else:
            super().__init__(
                intents=discord.Intents.all()
            )
            self.logger.info("Running in prod mode.")
        self.statuses = cycle([
            "My Ping! {latency} ms",
            "Some Servers, {guild_count}",
            "Klassick | https://dsc.gg/klassick"
        ])  # Create a cycle, so we can simply use next() to get the next status.

    def load_exts(self):
        for ext in os.listdir("cogs"):
            if ext.endswith(".py"):
                self.load_extension(f"cogs.{ext[:-3]}")
                self.logger.info(f"Loaded {ext[:-3]}")

    async def on_ready(self):
        """
        Instead of having to use @client.event decorators, we can simply add/overwrite
        methods on the client object. This is a lot cleaner and easier to read.
        """
        self.load_exts()
        self.logger.info(f"Logged in as {self.user.name}")
        self.update_presence.start()

    @tasks.loop(seconds=60)
    async def update_presence(self):
        status = next(self.statuses).format(guild_count=len(self.guilds), latency=round(self.latency * 1000))
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=status
            )
        )
        self.logger.debug(f"Updated presence to \"{status}\"")

    def run(self):
        super().run(os.getenv("TOKEN"))

