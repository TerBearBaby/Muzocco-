import discord, json, os, random, asyncio, string, time, hostingserver, requests
from discord.ext import commands, tasks
from datetime import datetime
from hostingserver import keep_alive

from requests import get

# imports things needed for bot (modules needed)

# bot token to activate bot

member = discord.Member

#client = discord.Client()

Game = discord.Game

Streaming = discord.Streaming

idle = discord.Status.idle

dnd = discord.Status.dnd

randomc = random.choice

intents = discord.Intents.default()
intents.presences = True
intents.members = True
intents.message_content = True

client = commands.Bot(command_prefix=['m?', 'M?'], intents=intents, help_command=None, case_insensitive=True) 


@client.event
async def on_ready():
  print(f"logged into {client.user.name}")


statuses = ""

@tasks.loop(seconds=120)
async def update_presence():
  statuses = [f"My Ping! {round (client.latency * 1000)} ms", f"Some Servers, {len(client.guilds)}", "Klassick | https://dsc.gg/klassick"]
  await client.change_presence(status=dnd, activity=discord.Activity(type=discord.ActivityType.watching, name=randomc(statuses)))

@update_presence.before_loop
async def before_update_presence():
  await client.wait_until_ready()

update_presence.start()

@client.command()
async def help(ctx):
  embed=discord.Embed(title="Hey There!\nMuzocco! doesnt have too many commands yet!", description="Commands that are available for beta update are listed below (bigger desc coming soon!)", color=0x2F3136)
  embed.add_field(name="M?help", value="Shows help page for Muzocco!", inline=True)
  embed.add_field(name="M?bi/M?botinfo", value="Shows bot info for Muzocco!", inline=True)
  embed.add_field(name="M?ui/userinfo", value="Shows user info for pinged user", inline=True)
  embed.add_field(name="M?si/serverinfo", value="Shows info for a server Muzocco! is in", inline=True)
  embed.add_field(name="M?meme", value="Run this command to see an epic meme", inline=True)
  embed.add_field(name="M?av/avatar", value="Shows avatar (pfp) for pinged user", inline=True)
  embed.add_field(name="M?links", value="Links for invitation to support and to invite Muzocco!")
  embed.set_footer(text=f"Copyright © Muzocco! 2022 All Rights Reserved")
  embed.timestamp = discord.utils.utcnow()
  await ctx.reply(embed=embed)

@client.command(aliases=["bi"])
async def botinfo(ctx):
  embed = discord.Embed(color=0x2F3136)
  embed.add_field(name="Host:", value="```\nreplit.com\n```", inline=False)
  embed.add_field(name="Ping:", value=f"```\n{round (client.latency * 1000)} ms\n```", inline=False)
  embed.add_field(name="Uptime:", value=f"```\n{time.time() - starttime}\n```", inline=False)
  embed.add_field(name="Date Created:", value="```\nAugust 8th, 2022\n```", inline=False)
  await ctx.reply(embed=embed)


@client.command(aliases=["ui"])
async def userinfo(ctx, user: discord.Member = None):
  guild = ctx.guild
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
  embed.add_field(name=f"💬Users Display Name: {user.display_name}", value="Displays A Users Nickname If They Have One", inline=False)
  embed.add_field(name=f"🆔User ID: {user.id}", value="User ID", inline=False)
  embed.add_field(name=f"🔊Playing Status Or Custom Status: {user.activity}", value="Displaying What User Is Playing", inline=False)
  embed.add_field(name=f"🚦User Status: {user.status}", value="Displaying User Status", inline=False)
  embed.add_field(name=f"👥User Roles:", value=''.join([b]), inline=False)
  embed.add_field(name=f"📆Joined Discord On: {user.created_at}", value="Displaying When User Joined Discord", inline=False)
  await ctx.reply(embed=embed)


@client.command(aliases=["av"])
async def avatar(ctx, member: discord.Member = None):
  if not ctx.author.bot:
      if member == None:
          member = ctx.author
  embed = discord.Embed(title=f"", color=0x2F3136)
  embed.set_author(name=f"{member}'s Avatar", icon_url=f"{member.avatar.url}")
  embed.set_image(url=f"{member.avatar.url}")
  await ctx.reply(embed=embed)


@client.command()
async def meme(ctx):
    content = get("https://meme-api.herokuapp.com/gimme").text
    data = json.loads(content)

    title = data["title"]
    link = data["postLink"]
    img = data["url"]
    likes = data["ups"]

    meme = discord.Embed(description=f"[{title}]({link})", color=0x2F3136).set_image(url=img)
    meme.set_footer(text=f"{likes}👍")
    await ctx.reply(embed=meme)


@client.command(aliases=["si"])
async def serverinfo(ctx, member: discord.Member = None):
  if not ctx.author.bot:
    if member == None:
      member = ctx.author
  embed = discord.Embed(title=f"{ctx.guild.name} Info", description="Information of this Server", color=0x2F3136)
  embed.add_field(name='🆔Server ID', value=f"{ctx.guild.id}", inline=True)
  embed.add_field(name='📆Created On', value=ctx.guild.created_at.strftime("%b %d %Y"), inline=True)
  embed.add_field(name='👑Owner', value=f"{ctx.guild.owner.mention}", inline=True)
  embed.add_field(name='👥Members', value=f'{ctx.guild.member_count} Members', inline=True)
  embed.add_field(name='💬Channels', value=f'{len(ctx.guild.text_channels)} Text | {len(ctx.guild.voice_channels)} Voice', inline=True)
  await ctx.reply(embed=embed)


@client.command()
async def links(ctx):
  supportem=discord.Embed(title="Muzocco! Support Server", url="https://dsc.gg/muzocco-support", description="Hey there, Muzocco! Support Server has all of Musocco's updates & GitHub's and more!\n\nJoin now!\nhttps://discord.gg/s9NtJADv\nhttps://dsc.gg/muzocco-support", color=0x2F3136)
  inviteem=discord.Embed(title="Muzocco!", url="https://dsc.gg/muzocco", description="This is Muzocco! The coolest bot ever, invite this bot to your server to listen to music in a VC or use my fun commands!\n\nhttps://dsc.gg/muzocco", color=0x2F3136)
  await ctx.reply(embed=inviteem)
  await ctx.reply(embed=supportem)


@client.slash_command(name="help")
async def help(ctx):
  embed=discord.Embed(title="Hey There!\nMuzocco! doesnt have too many commands yet!", description="Commands that are available for beta update are listed below (bigger desc coming soon!)", color=0x2F3136)
  embed.add_field(name="/help", value="Shows help page for Muzocco!", inline=True)
  embed.add_field(name="/bi or /botinfo", value="Shows bot info for Muzocco!", inline=True)
  embed.add_field(name="/ui or /userinfo", value="Shows user info for pinged user", inline=True)
  embed.add_field(name="/si or /serverinfo", value="Shows info for a server Muzocco! is in", inline=True)
  embed.add_field(name="/meme", value="Run this command to see an epic meme", inline=True)
  embed.add_field(name="/av or /avatar", value="Shows avatar (pfp) for pinged user", inline=True)
  embed.add_field(name="/links", value="Links for invitation to support and to invite Muzocco!")
  embed.set_footer(text=f"Copyright © Muzocco! 2022 All Rights Reserved")
  embed.timestamp = discord.utils.utcnow()
  await ctx.respond(embed=embed)


@client.slash_command(name="botinfo",  aliases=["bi"])
async def botinfo(ctx):
  embed = discord.Embed(color=0x2F3136)
  embed.add_field(name="Host:", value="```\nreplit.com\n```", inline=False)
  embed.add_field(name="Ping:", value=f"```\n{round (client.latency * 1000)} ms\n```", inline=False)
  embed.add_field(name="Uptime:", value=f"```\n{time.time() - starttime}\n```", inline=False)
  embed.add_field(name="Date Created:", value="```\nAugust 8th, 2022\n```", inline=False)
  await ctx.respond(embed=embed)


@client.slash_command(name="userinfo", aliases=["ui"])
async def userinfo(ctx, user: discord.Member = None):
  guild = ctx.guild
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
  embed.add_field(name=f"💬Users Display Name: {user.display_name}", value="Displays A Users Nickname If They Have One", inline=False)
  embed.add_field(name=f"🆔User ID: {user.id}", value="User ID", inline=False)
  embed.add_field(name=f"🔊Playing Status Or Custom Status: {user.activity}", value="Displaying What User Is Playing", inline=False)
  embed.add_field(name=f"🚦User Status: {user.status}", value="Displaying User Status", inline=False)
  embed.add_field(name=f"👥User Roles:", value=''.join([b]), inline=False)
  embed.add_field(name=f"📆Joined Discord On: {user.created_at}", value="Displaying When User Joined Discord", inline=False)
  await ctx.respond(embed=embed)


@client.slash_command(name="avatar", aliases=["av", "pfp"])
async def avatar(ctx, member: discord.Member = None):
  if not ctx.author.bot:
      if member == None:
          member = ctx.author
  embed = discord.Embed(title=f"", color=0x2F3136)
  embed.set_author(name=f"{member}'s Avatar", icon_url=f"{member.avatar.url}")
  embed.set_image(url=f"{member.avatar.url}")
  await ctx.respond(embed=embed)


@client.slash_command(name="meme")
async def meme(ctx):
    content = get("https://meme-api.herokuapp.com/gimme").text
    data = json.loads(content)

    title = data["title"]
    link = data["postLink"]
    img = data["url"]
    likes = data["ups"]

    meme = discord.Embed(description=f"[{title}]({link})", color=0x2F3136).set_image(url=img)
    meme.set_footer(text=f"{likes}👍")
    await ctx.respond(embed=meme)


@client.slash_command(name="serverinfo", aliases=["si"])
async def serverinfo(ctx, member: discord.Member = None):
  if not ctx.author.bot:
    if member == None:
      member = ctx.author
  embed = discord.Embed(title=f"{ctx.guild.name} Info", description="Information of this Server", color=0x2F3136)
  embed.add_field(name='🆔Server ID', value=f"{ctx.guild.id}", inline=True)
  embed.add_field(name='📆Created On', value=ctx.guild.created_at.strftime("%b %d %Y"), inline=True)
  embed.add_field(name='👑Owner', value=f"{ctx.guild.owner.mention}", inline=True)
  embed.add_field(name='👥Members', value=f'{ctx.guild.member_count} Members', inline=True)
  embed.add_field(name='💬Channels', value=f'{len(ctx.guild.text_channels)} Text | {len(ctx.guild.voice_channels)} Voice', inline=True)
  await ctx.respond(embed=embed)

  
@client.slash_command()
async def links(ctx):
  supportem=discord.Embed(title="Muzocco! Support Server", url="https://dsc.gg/muzocco-support", description="Hey there, Muzocco! Support Server has all of Musocco's updates & GitHub's and more!\n\nJoin now!\nhttps://discord.gg/s9NtJADv\nhttps://dsc.gg/muzocco-support", color=0x2F3136)
  inviteem=discord.Embed(title="Muzocco!", url="https://dsc.gg/muzocco", description="This is Muzocco! The coolest bot ever, invite this bot to your server to listen to music in a VC or use my fun commands!\n\nhttps://dsc.gg/muzocco", color=0x2F3136)
  await ctx.respond(embed=inviteem)
  await ctx.respond(embed=supportem)

keep_alive()
starttime = time.time()
client.run(os.getenv("TOKEN"))
