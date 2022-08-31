import discord, datetime
from discord.ext import commands

channel = 1014425666990657576
intents = discord.Intents.default()
intents.presences = True
intents.members = True
intents.message_content = True

class staff(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(name='mute', description='Mutes <user> for <duration> minutes because of <reason> using discords new timeouts')
    @commands.has_guild_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member, duration, reason):
      try:
        minutes = datetime.timedelta(minutes=int(duration))
        await member.timeout_for(minutes, reason=reason)
        muteem=discord.embed(title=f"{member.mention} was muted for {minutes} for {reason}", color=0x2F3136)
        await ctx.respond(embed=muteem)
        await self.client.get_channel(channel).send(f'{member.name} was muted in {ctx.guild}')
      except discord.Forbidden:
        await ctx.respond('No Perms')

    @commands.slash_command(name='unmute', description='unmuting <user> with <reason> using new discord timeouts')
    @commands.has_guild_permissions(moderate_members=True)
    async def unmute(self, ctx, member: discord.Member, reason):
      try:
        unmuteem=discord.Embed(title=f"Unmuted {member.mention}", color=0x2F3136)
        await member.remove_timeout(reason=reason)
        await ctx.respond(embed=unmuteem)
        await self.client.get_channel(channel).send(f'{member.name} was unmuted in {ctx.guild}')
      except discord.Forbidden:
        await ctx.respond('No Perms')


    @commands.slash_command(name="purge", description="Deletes certain amount of messages **ADMIN**")
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx, amount=10):
      try:
        print('Purge enabled')
        await ctx.channel.purge(limit=int(amount) + 1)
        await self.client.get_channel(channel).send(f'{ctx.channel} was purged by {ctx.author.name} \n User Id: {ctx.author.id} \n \n \n **CTX** \n {ctx} \n -----------------------------------')
      except discord.Forbidden:
        await ctx.respond('No Perms')


    @commands.slash_command(name="ban", description="Bans specified user | /ban <user> <reason>")
    @commands.has_permissions(moderate_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
      try:
        banem=discord.Embed(title=f"Banned {member.mention} for {reason}", color=0x2F3136)
        await member.ban(reason=reason)
        await ctx.respond(embed=banem)
        await self.client.get_channel(channel).send(f'{member} was banned by {ctx.author.name} \n User Id: {ctx.author.id} in {ctx.guild} \n \n \n **CTX** \n {ctx} \n -----------------------------------')
      except discord.Forbidden:
        await ctx.respond('No Perms')
    
    @commands.slash_command(name="kick", description="Kicks specified user | /kick <user> <reason>")
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
      try:
        kickem=discord.Embed(title=f"Kicked {member.mention} for {reason}", color=0x2F3136)
        await member.kick(reason=reason)
        await ctx.send(embed=kickem)
        await self.client.get_channel(channel).send(f'{member} was kicked by {ctx.author.name} \n User Id: {ctx.author.id} in {ctx.guild} \n \n \n **CTX** \n {ctx} \n -----------------------------------')
      except discord.Forbidden:
        await ctx.respond('No Perms')

def setup(client):
    client.add_cog(staff(client))
