import discord
from discord.ui import View, Button
import time
import requests
import json


class Misc(discord.Cog):
    def __init__(self, client: discord.Bot):
        self.client = client
        self.starttime = time.time()

    @discord.command(name="suggest", description="DM's Owner(s) (content) for your suggestion(s)")
    async def suggest(self, ctx: discord.ApplicationContext, *, content):
        await self.client.get_user(800886153783279658).send(f"{ctx.author} suggests {content}")
        await self.client.get_user(977998058031833188).send(f"{ctx.author} suggests {content}")
        await ctx.respond("Suggestion sent!", ephemeral=True)

    @discord.command(name="help", description="Help page with commands for Muzocco!")
    async def help(self, ctx: discord.ApplicationContext):
        link = Button(label='Dashboard',
                      url='https://terbearbaby.github.io/Muzocco-')
        view = View()
        view.add_item(link)
        embed = discord.Embed(title="Hey There!\nMuzocco! doesnt have too many commands yet!",
                              description="Commands that are available for beta update are listed below (bigger desc coming soon!)",
                              color=0x2F3136)
        embed.add_field(
            name="/help", value="Shows help page for Muzocco!", inline=True)
        embed.add_field(name="/bi or /botinfo",
                        value="Shows bot info for Muzocco!", inline=True)
        embed.add_field(name="/ui or /userinfo",
                        value="Shows user info for pinged user", inline=True)
        embed.add_field(name="/si or /serverinfo",
                        value="Shows info for a server Muzocco! is in", inline=True)
        embed.add_field(
            name="/meme", value="Run this command to see an epic meme", inline=True)
        embed.add_field(name="/av or /avatar",
                        value="Shows avatar (pfp) for pinged user", inline=True)
        embed.add_field(name="/mute", value="Mutes specified user")
        embed.add_field(name="/unmute", value="Unmutes specified user")
        embed.add_field(name="/kick", value="Kicks specified user")
        embed.add_field(name="/ban", value="Bans specified user")
        embed.add_field(name="/unban", value="Unbans specified user")
        embed.add_field(name="/echo", value="Repeats whatever you say")
        embed.set_footer(text=f"Copyright © Muzocco! 2022 All Rights Reserved")
        embed.timestamp = discord.utils.utcnow()
        await ctx.respond(embed=embed, view=view)

    @discord.command(name="echo", description="Repeats whatever you say [ /echo (content) ]")
    async def echo(self, ctx: discord.ApplicationContext, *, content):
        embed = discord.Embed(
            title=f"{content}", description=f"Repeated {content}", color=0x2F3136)
        await ctx.respond(embed=embed)

    @discord.command(name="bot_info", description="Bot info for Muzocco!")
    async def botinfo(self, ctx: discord.ApplicationContext):
        link = Button(label='Dashboard',
                      url='https://terbearbaby.github.io/Muzocco-')
        view = View()
        view.add_item(link)
        embed = discord.Embed(title="Bot Information",
                              description=f"**Head Info:**\nHost: Muzocco-Test.pianoidol.repl.co\nDate Created: August 8th, 2022 8/8/2022\n\n**Statistics:**\nPing: {round(self.client.latency * 1000)} ms\nUptime: {time.time() - self.starttime} seconds\n\n**Other Info:**\nPartners: <@977998058031833188>'s Talking Ben Bot <@994213404371861544> https://talking-ben-dbot.github.io/",
                              color=0x2F3136)
        embed.set_footer(text="DM Terbearbaby#6960 if you have any complaints")
        await ctx.respond(embed=embed, view=view)

    @discord.command(name="user_info", description="User info for specified user")
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
        await ctx.respond(embed=embed)

    @discord.command(name="avatar", description="Shows profile picture for specified user")
    async def avatar(self, ctx: discord.ApplicationContext, member: discord.Member = None):
        if not ctx.author.bot:
            if member == None:
                member = ctx.author
        embed = discord.Embed(title=f"", color=0x2F3136)
        embed.set_author(name=f"{member}'s Avatar",
                         icon_url=f"{member.avatar.url}")
        embed.set_image(url=f"{member.avatar.url}")
        await ctx.respond(embed=embed)

    @discord.command(name="meme", description="Funny memes")
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

    @discord.command(name="server_info", description="Info for a server that command is ran in")
    async def serverinfo(self, ctx: discord.ApplicationContext):
        embed = discord.Embed(title=f"{ctx.guild.name} Info",
                              description="Information of this Server", color=0x2F3136)
        embed.add_field(name='🆔Server ID', value=f"{ctx.guild.id}", inline=True)
        embed.add_field(name='📆Created On', value=ctx.guild.created_at.strftime(
            "%b %d %Y"), inline=True)
        embed.add_field(
            name='👑Owner', value=f"{ctx.guild.owner.mention}", inline=True)
        embed.add_field(name='👥Members',
                        value=f'{ctx.guild.member_count} Members', inline=True)
        embed.add_field(
            name='💬Channels', value=f'{len(ctx.guild.text_channels)} Text | {len(ctx.guild.voice_channels)} Voice',
            inline=True)
        await ctx.respond(embed=embed)

    @discord.command(name="links", description="Links for Muzocco!")
    async def links(self, ctx: discord.ApplicationContext):
        link = Button(label='Dashboard',
                      url='https://terbearbaby.github.io/Muzocco-')
        view = View()
        view.add_item(link)
        supportem = discord.Embed(title="Muzocco! Support Server", url="https://dsc.gg/muzocco-support",
                                  description="Hey there, Muzocco! Support Server has all of Musocco's updates & GitHub's and more!\n\nJoin now!\nhttps://discord.gg/s9NtJADv\nhttps://dsc.gg/muzocco-support",
                                  color=0x2F3136)
        inviteem = discord.Embed(title="Muzocco!", url="https://dsc.gg/muzocco",
                                 description="This is Muzocco! The coolest bot ever, invite this bot to your server to listen to music in a VC or use my fun commands!\n\nhttps://dsc.gg/muzocco",
                                 color=0x2F3136)
        await ctx.respond(embed=inviteem)
        await ctx.respond(embed=supportem, view=view)


def setup(client):
    client.add_cog(Misc(client))
