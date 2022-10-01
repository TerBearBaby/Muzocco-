import discord, json, os, random, asyncio, string, time, requests
from Cog import staff
from Cog import music
from discord.ext import commands, tasks
from datetime import datetime
from discord.ui import Button, View
from requests import get
import dotenv

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


@client.slash_command(name="suggest", description="DM's Owner(s) (content) for your suggestion(s)")
async def suggest(ctx, *, content):
  await client.get_user(800886153783279658).send(f"{ctx.author} suggests {content}")
  await client.get_user(977998058031833188).send(f"{ctx.author} suggests {content}")
  await ctx.respond("Suggestion sent!", ephemeral=True)


@client.slash_command(name="help", description="Help page with commands for Muzocco!")
async def help(ctx):
  link = Button(label='Dashboard', url='https://terbearbaby.github.io/Muzocco-')
  view = View()
  view.add_item(link)
  embed=discord.Embed(title="Hey There!\nMuzocco! doesnt have too many commands yet!", description="Commands that are available for beta update are listed below (bigger desc coming soon!)", color=0x2F3136)
  embed.add_field(name="/help", value="Shows help page for Muzocco!", inline=True)
  embed.add_field(name="/bi or /botinfo", value="Shows bot info for Muzocco!", inline=True)
  embed.add_field(name="/ui or /userinfo", value="Shows user info for pinged user", inline=True)
  embed.add_field(name="/si or /serverinfo", value="Shows info for a server Muzocco! is in", inline=True)
  embed.add_field(name="/meme", value="Run this command to see an epic meme", inline=True)
  embed.add_field(name="/av or /avatar", value="Shows avatar (pfp) for pinged user", inline=True)
  embed.add_field(name="/mute", value="Mutes specified user")
  embed.add_field(name="/unmute", value="Unmutes specified user")
  embed.add_field(name="/kick", value="Kicks specified user")
  embed.add_field(name="/ban", value="Bans specified user")
  embed.add_field(name="/unban", value="Unbans specified user")
  embed.add_field(name="/echo", value="Repeats whatever you say")
  embed.set_footer(text=f"Copyright © Muzocco! 2022 All Rights Reserved")
  embed.timestamp = discord.utils.utcnow()
  await ctx.respond(embed=embed, view=view)


@client.slash_command(name="echo", description="Repeats whatever you say [ /echo (content) ]")
async def echo(ctx, *, content):
  embed=discord.Embed(title=f"{content}", description=f"Repeated {content}", color=0x2F3136)
  await ctx.respond(embed=embed)


@client.slash_command(name="bot_info", description="Bot info for Muzocco!")
async def botinfo(ctx):
  link = Button(label='Dashboard', url='https://terbearbaby.github.io/Muzocco-')
  view = View()
  view.add_item(link)
  embed = discord.Embed(title="Bot Information", description=f"**Head Info:**\nHost: Muzocco-Test.pianoidol.repl.co\nDate Created: August 8th, 2022 8/8/2022\n\n**Statistics:**\nPing: {round (client.latency * 1000)} ms\nUptime: {time.time() - starttime} seconds\n\n**Other Info:**\nPartners: None", color=0x2F3136)
  embed.set_footer(text="DM Terbearbaby#6960 if you have any complaints")
  await ctx.respond(embed=embed, view=view)


@client.slash_command(name="user_info", description="User info for specified user")
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


@client.slash_command(name="avatar", description="Shows profile picture for specified user")
async def avatar(ctx, member: discord.Member = None):
  if not ctx.author.bot:
      if member == None:
          member = ctx.author
  embed = discord.Embed(title=f"", color=0x2F3136)
  embed.set_author(name=f"{member}'s Avatar", icon_url=f"{member.avatar.url}")
  embed.set_image(url=f"{member.avatar.url}")
  await ctx.respond(embed=embed)


@client.slash_command(name="meme", description="Funny memes")
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


@client.slash_command(name="server_info", description="Info for a server that command is ran in")
async def serverinfo(ctx):
  embed = discord.Embed(title=f"{ctx.guild.name} Info", description="Information of this Server", color=0x2F3136)
  embed.add_field(name='🆔Server ID', value=f"{ctx.guild.id}", inline=True)
  embed.add_field(name='📆Created On', value=ctx.guild.created_at.strftime("%b %d %Y"), inline=True)
  embed.add_field(name='👑Owner', value=f"{ctx.guild.owner.mention}", inline=True)
  embed.add_field(name='👥Members', value=f'{ctx.guild.member_count} Members', inline=True)
  embed.add_field(name='💬Channels', value=f'{len(ctx.guild.text_channels)} Text | {len(ctx.guild.voice_channels)} Voice', inline=True)
  await ctx.respond(embed=embed)

  
@client.slash_command(name="links", description="Links for Muzocco!")
async def links(ctx):
  link = Button(label='Dashboard', url='https://terbearbaby.github.io/Muzocco-')
  view = View()
  view.add_item(link)
  supportem=discord.Embed(title="Muzocco! Support Server", url="https://dsc.gg/muzocco-support", description="Hey there, Muzocco! Support Server has all of Musocco's updates & GitHub's and more!\n\nJoin now!\nhttps://discord.gg/s9NtJADv\nhttps://dsc.gg/muzocco-support", color=0x2F3136)
  inviteem=discord.Embed(title="Muzocco!", url="https://dsc.gg/muzocco", description="This is Muzocco! The coolest bot ever, invite this bot to your server to listen to music in a VC or use my fun commands!\n\nhttps://dsc.gg/muzocco", color=0x2F3136)
  await ctx.respond(embed=inviteem)
  await ctx.respond(embed=supportem, view=view)




for file in os.listdir('Cog'): 
    if file.endswith('.py'):
      client.load_extension(f'Cog.' + file[:-3]) 


starttime = time.time()
client.run(os.getenv("TOKEN"))