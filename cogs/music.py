import logging
import typing

import discord
import wavelink
from discord.ext.commands import Cog, slash_command
from discord.ext import commands


class Queue(wavelink.Queue):
    def __init__(self):
        self.queue = []
        self.position = 0


class Music(Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        client.loop.create_task(self.create_nodes())

    async def create_nodes(self) -> None:
        await self.client.wait_until_ready()
        await wavelink.NodePool.create_node(bot=self.client,
                                            host="127.0.0.1",
                                            port="2333",
                                            password="youshallnotpass",
                                            region="us-central")

    def get_player(self, ctx: discord.ApplicationContext) -> wavelink.Player:
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)
        return player

    def display_track(self, track: wavelink.Track) -> str:
        return f"{track.title} by {track.author}"

    @Cog.listener()
    async def on_ready(self):
        if not self.client.is_ready:
            self.client.cogs_ready.ready_up('Commands')

    @Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        logging.info(f"Node <{node.identifier}> is ready!")

    @Cog.listener()
    async def on_wavelink_track_end(self, player: wavelink.Player,
                                    track: wavelink.Track, reason):
        if player.queue.is_empty:
            return

        track = await player.queue.get_wait()

        await player.play(track)

    @slash_command(name="join")
    async def join_command(self,
                           ctx: discord.ApplicationContext,
                           channel: typing.Optional[
                               discord.VoiceChannel] = None):
        """

        Bring the music player to your voice channel.

        """

        if channel is None:
            channel = ctx.author.voice.channel

        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if player is not None:
            if player.is_connected():
                return await ctx.send(
                    "client is already connected to a voice channel!")

        await channel.connect(cls=wavelink.Player)

        embed = discord.Embed(
            title=f"Connected to {channel.name}", color=ctx.author.color)

        await ctx.respond(embed=embed)

    @slash_command(name="leave")
    async def leave_command(self, ctx: discord.ApplicationContext):
        """

        Disconnect the bot from the current channel

        """

        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if player is None:
            return await ctx.send("The client is not connected to a voice channel!")

        await player.disconnect()

        embed = discord.Embed(
            title=f"Disconnected from {player.channel.name}", color=ctx.author.color)

        await ctx.respond(embed=embed)

    @slash_command(name="play")
    async def play_command(self, ctx: discord.ApplicationContext, search: str):
        """

        Play a song



        Parameters

        ----------

        search: song to search for

        """

        search = await wavelink.YouTubeTrack.search(query=search, return_first=True)

        if not ctx.guild.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(
                cls=wavelink.Player)

        else:
            vc: wavelink.Player = ctx.guild.voice_client

        if not vc.is_playing():
            await vc.play(search)
            embed = discord.Embed(
                title=f"Now playing {self.display_track(search)}", color=ctx.author.color)

            return await ctx.send(embed=embed)

        await vc.queue.put_wait(search)

        embed = discord.Embed(
            title=f"Added {search.title} to the queue", color=ctx.author.color)

        await ctx.respond(embed=embed)

    @slash_command(name="stop")
    async def stop_command(self, ctx: discord.ApplicationContext):
        """

        Stop the current song from playing

        """

        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if player is None:
            return await ctx.send("The client is not connected to a voice channel!")

        if player.is_playing():
            track = player.track
            await player.stop()

            embed = discord.Embed(
                title=f"Stopped playing {self.display_track(track)}", color=ctx.author.color)

            return await ctx.respond(embed=embed)

        else:
            return await ctx.respond("The client is not playing anything!")

    @slash_command(name="pause")
    async def pause_command(self, ctx: discord.ApplicationContext):
        """

        Pause the current song

        """

        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if player is None:
            return await ctx.send("The client is not connected to a voice channel!")

        if not player.is_paused():
            if player.is_playing():
                await player.pause()

                embed = discord.Embed(
                    title=f"Paused {self.display_track(player.track)}", color=ctx.author.color)

                return await ctx.respond(embed=embed)

            else:
                return await ctx.respond("The client is not playing anything!")

        else:
            return await ctx.respond("The client is already paused!")

    @slash_command(name="resume")
    async def resume_command(self, ctx: discord.ApplicationContext):
        """

        Resume the current song

        """

        node = wavelink.NodePool.get_node()

        player = node.get_player(ctx.guild)

        if player is None:
            return await ctx.respond(
                "The client is not connected to a voice channel!")

        if player.is_paused():
            await player.resume()
            embed = discord.Embed(
                title=f"Resumed {self.display_track(player.track)}", color=ctx.author.color)

            return await ctx.respond(embed=embed)

        else:
            return await ctx.respond("The client is not paused!")

    @slash_command(name="skip")
    async def skip_command(self, ctx: discord.ApplicationContext):
        """

        Skip the current song playing

        """

        node = wavelink.NodePool.get_node()

        player = node.get_player(ctx.guild)

        if player is None:
            return await ctx.respond("The client is not connected to a voice channel!")

        if player.is_playing():
            if player.queue.is_empty:
                return await ctx.send("The queue is empty!")

            track = player.queue.get()

            await player.play(track)

            embed = discord.Embed(
                title=f"Now playing {self.display_track(track)}", color=ctx.author.color)

            return await ctx.respond(embed=embed)

        else:
            return await ctx.respond("The client is not playing anything!")

    @slash_command(name="queue")
    async def queue_command(self, ctx: discord.ApplicationContext):
        """

        Check what current songs are in the queue

        """

        node = wavelink.NodePool.get_node()

        player = node.get_player(ctx.guild)

        if player is None:
            return await ctx.respond("The client is not connected to a voice channel!")

        if player.queue.is_empty:
            return await ctx.respond("The queue is empty!")

        embed = discord.Embed(title=f"Queue", color=ctx.author.color)
        embed.set_author(
            name=f"Currently Playing: {self.display_track(track)}", icon_url=ctx.author.avatar.url)
        embed.set_thumbnail(url=ctx.guild.icon.url)

        num = 0

        for track in player.queue:
            num += 1
            embed.add_field(name=f"{num}. {self.display_track(track)}",
                            value="\u200B", inline=True)

        await ctx.respond(embed=embed)


def setup(client):
    client.add_cog(Music(client))
