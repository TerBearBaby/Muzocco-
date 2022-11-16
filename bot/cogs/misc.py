import discord
from discord.ext import commands
from discord.ext.commands import Cog, slash_command
from discord.ui import View, Button
import time
import requests
import json


class Misc(Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.starttime = time.time()

    @slash_command(name="help", description="Help page with commands for Muzocco!")
    async def help(self, ctx: discord.ApplicationContext):
        link = Button(label='Dashboard',
                      url='https://muzocco.conchdev.com')
        view = View()
        view.add_item(link)
        embed = discord.Embed(title="Help page",
                              description="Muzocco! Help page listed with all commands",
                              color=0x2F3136)
        embed.add_field(name="</help:1006049204231229581>", value="Shows help page for Muzocco!", inline=True)
        embed.add_field(name="</botinfo:1006049204231229581>",
                        value="Shows bot info for Muzocco!", inline=True)
        embed.add_field(name="</userinfo:1006049204231229581>",
                        value="Shows user info for pinged user", inline=True)
        embed.add_field(name="</serverinfo:1006049204231229581>", value="Shows info for a server Muzocco! is in", inline=True)
        embed.add_field(name="</meme:1006049204231229581>", value="Run this command to see an epic meme", inline=True)
        embed.add_field(name="</avatar:1006049204231229581>",
                        value="Shows avatar (pfp) for pinged user", inline=True)
        embed.add_field(name="</echo:1028065104593436692>", value="Repeats whatever you say")
        embed.add_field(name="</play:1006049204231229581>", value="Play a song.")
        embed.add_field(name="</leave:1006049204231229581>", value="Removes the bot from a voice channel.")
        embed.add_field(name="</join:1006049204231229581>", value="Makes the bot join a voice channel.")
        embed.add_field(name="</skip:1006049204231229581>", value="Skips the current song.")
        embed.add_field(name="</pause:1006049204231229581>", value="Pause the player.")
        embed.add_field(name="</resume:1006049204231229581>", value="Resumes the player from pausing.")
        embed.add_field(name="</queue:1006049204231229581>", value="Check the player's queue.")
        embed.add_field(name="</stop:1006049204231229581>", value="Stop the player from playing music.")
        embed.set_footer(text=f"Copyright © Muzocco! 2022 All Rights Reserved")
        embed.timestamp = discord.utils.utcnow()
        await ctx.respond(embed=embed, view=view)

    @slash_command(name="echo", description="Repeats whatever you say [ /echo (content) ]")
    async def echo(self, ctx: discord.ApplicationContext, *, content):
        embed = discord.Embed(
            title=f"{content}", description=f"Repeated {content}", color=0x2F3136)
        embed.timestamp = discord.utils.utcnow()
        await ctx.respond(embed=embed)

    @slash_command(name="botinfo", description="Bot info for Muzocco!")
    async def botinfo(self, ctx: discord.ApplicationContext):
        link = Button(label='Dashboard',
                      url='https://muzocco.conchdev.com')
        view = View()
        view.add_item(link)
        embed = discord.Embed(title="Bot Information",
                              description=f"**Head Info:**\nHost: Raspberry Pi 4B 4gb\nDate Created: August 8th, 2022 8/8/2022\n\n**Statistics:**"
                              f"\nReputation (Servers): {len(self.client.guilds)}\nPing: {round(self.client.latency * 1000)} ms\nUptime: {time.time() - self.starttime} seconds\n\n**Other Info:**\nWebsite: Click the button!/nPartners: <@977998058031833188>'s Talking Ben Bot <@994213404371861544>! Check out more here: https://talking-ben-dbot.github.io/",
                              color=0x2F3136)
        embed.set_footer(text="DM Terbearbaby#6960 if you have any complaints")
        embed.timestamp = discord.utils.utcnow()
        await ctx.respond(embed=embed, view=view)

    @slash_command(name="userinfo", description="User info for specified user")
    async def userinfo(self, ctx: discord.ApplicationContext, user: discord.Member = None):
        if user == None:
            user = ctx.author

        rlist = []
        for role in user.roles:
            if role.name != "@everyone":
                rlist.append(role.mention)
            else:
                rlist.append("No roles")

        b = " | ".join(rlist)
        embed = discord.Embed(title=f"{user}", color=0x2F3136)
        embed.add_field(name=f"💬Users Display Name: {user.display_name}",
                        value="Displays A Users Nickname If They Have One", inline=False)
        embed.add_field(name=f"🆔User ID: {user.id}", value="User ID", inline=False)
        embed.add_field(
            name=f"🔊Playing Status Or Custom Status: {user.activity}", value="Displaying What User Is Playing",
            inline=False)
        embed.add_field(
            name=f"🚦User Status: {user.status}", value="Displaying User Status", inline=False)
        embed.add_field(name=f"👥User Roles:", value=''.join([b]), inline=False)
        embed.add_field(name=f"📆Joined Discord On: {user.created_at}",
                        value="Displaying When User Joined Discord", inline=False)
        embed.timestamp = discord.utils.utcnow()
        await ctx.respond(embed=embed)

    @slash_command(name="avatar", description="Shows profile picture for specified user")
    async def avatar(self, ctx: discord.ApplicationContext, member: discord.Member = None):
        if not ctx.author.bot:
            if member == None:
                member = ctx.author
        embed = discord.Embed(title=f"", color=0x2F3136)
        embed.set_author(name=f"{member}'s Avatar",
                         icon_url=f"{member.avatar.url}")
        embed.set_image(url=f"{member.avatar.url}")
        embed.timestamp = discord.utils.utcnow()
        await ctx.respond(embed=embed)

    @slash_command(name="meme", description="Funny memes")
    async def meme(self, ctx: discord.ApplicationContext):
        content = requests.get("https://meme-api.herokuapp.com/gimme").text
        data = json.loads(content)

        title = data["title"]
        link = data["postLink"]
        img = data["url"]
        likes = data["ups"]

        meme = discord.Embed(
            description=f"[{title}]({link})", color=0x2F3136).set_image(url=img)
        meme.set_footer(text=f"{likes}👍")
        await ctx.respond(embed=meme)

    @slash_command(name="advert", description="Advert for Muzocco!")
    async def advert(self, ctx):
        embed = discord.Embed(title=f"Advertisement", description="Advertise the bot in your servers!", color=0x2F3136)
        await ctx.respond(embed=embed)
        await ctx.respond("```\nThis is Muzocco! The coolest bot ever, invite this bot to your server to listen to music in a VC or use my fun commands! Muzocco! Support Server has all of Musocco's updates & GitHub's and more!\n\n**Join and add the bot now!**\nhttps://discord.gg/QBS6YBh6qS\n\n**Guide with website**\nTo add bot to server, click link below and press on invite image\nhttps://muzocco.conchdev.com\n\n**Top.gg vote**\nhttps://top.gg/bot/1006049204231229581\n\nCreated by TerBearBaby at https://TerBearBaby.github.io\nhttps://share.creavite.co/mralP2oW4Q46I312.gif\n```")
        await ctx.respond("__**RESULT**__\nThis is Muzocco! The coolest bot ever, invite this bot to your server to listen to music in a VC or use my fun commands! Muzocco! Support Server has all of Musocco's updates & GitHub's and more!\n\n**Join and add the bot now!**\nhttps://discord.gg/QBS6YBh6qS\n\n**Guide with website**\nTo add bot to server, click link below and press on invite image\nhttps://muzocco.conchdev.com\n\n**Top.gg vote**\nhttps://top.gg/bot/1006049204231229581\n\nCreated by TerBearBaby at https://TerBearBaby.github.io\nhttps://share.creavite.co/mralP2oW4Q46I312.gif")
def setup(client):
    client.add_cog(Misc(client))
