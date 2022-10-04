import datetime

import discord

channel = 1014425666990657576
intents = discord.Intents.default()
intents.presences = True
intents.members = True
intents.message_content = True


class staff(discord.Cog):
    def __init__(self, client):
        self.client = client

    @discord.command(name='mute', description='Mutes <user> for <duration> minutes because of <reason> using discords new timeouts')
    @discord.default_permissions(moderate_members=True)
    async def mute(self, ctx: discord.ApplicationContext, member: discord.Member, duration, reason):
        try:
            minutes = datetime.timedelta(minutes=int(duration))
            await member.timeout_for(minutes, reason=reason)
            muteem = discord.embed(
                title=f"{member.mention} was muted for {minutes} for {reason}", color=0x2F3136)
            await ctx.respond(embed=muteem)
            await self.client.get_channel(channel).send(f'{member.name} was muted in {ctx.guild}')
        except discord.Forbidden:
            await ctx.respond('No Perms')

    @discord.command(name='unmute', description='unmuting <user> with <reason> using new discord timeouts')
    @discord.default_permissions(moderate_members=True)
    async def unmute(self, ctx: discord.ApplicationContext, member: discord.Member, reason):
        try:
            unmuteem = discord.Embed(
                title=f"Unmuted {member.mention}", color=0x2F3136)
            await member.remove_timeout(reason=reason)
            await ctx.respond(embed=unmuteem)
            await self.client.get_channel(channel).send(f'{member.name} was unmuted in {ctx.guild}')
        except discord.Forbidden:
            await ctx.respond('No Perms')

    @discord.command(name='unban', description='unban <user> with <reason>')
    @discord.default_permissions(administrator=True)
    async def unban(self, ctx: discord.ApplicationContext, member: discord.Member, reason):
        try:
            unmuteem = discord.Embed(
                title=f"Unban{member.mention}", color=0x2F3136)
            await member.unban(reason=reason)
            await ctx.respond(embed=unmuteem)
            await self.client.get_channel(channel).send(f'{member.name} was unbanned in {ctx.guild}')
        except discord.Forbidden:
            await ctx.respond('No Perms')

    @discord.command(name="purge", description="Deletes certain amount of messages **ADMIN**")
    @discord.default_permissions(administrator=True)
    async def purge(self, ctx: discord.ApplicationContext, amount=10):
        try:
            print('Purge enabled')
            await ctx.channel.purge(limit=int(amount) + 1)
            await ctx.respond("Purged channel", ephemeral=True)
            await self.client.get_channel(channel).send(f'{ctx.channel} was purged by {ctx.author.name} \n User Id: {ctx.author.id} \n \n \n **CTX** \n {ctx} \n -----------------------------------')
        except discord.Forbidden:
            await ctx.respond('No Perms')

    @discord.command(name="ban", description="Bans specified user | /ban <user> <reason>")
    @discord.default_permissions(moderate_members=True)
    async def ban(self, ctx: discord.ApplicationContext, member: discord.Member, *, reason=None):
        try:
            banem = discord.Embed(
                title=f"Banned {member.mention} for {reason}", color=0x2F3136)
            await member.ban(reason=reason)
            await ctx.respond(embed=banem)
            await self.client.get_channel(channel).send(f'{member} was banned by {ctx.author.name} \n User Id: {ctx.author.id} in {ctx.guild} \n \n \n **CTX** \n {ctx} \n -----------------------------------')
        except discord.Forbidden:
            await ctx.respond('No Perms')

    @discord.command(name="kick", description="Kicks specified user | /kick <user> <reason>")
    @discord.default_permissions(administrator=True)
    async def kick(self, ctx: discord.ApplicationContext, member: discord.Member, *, reason=None):
        try:
            kickem = discord.Embed(
                title=f"Kicked {member.mention} for {reason}", color=0x2F3136)
            await member.kick(reason=reason)
            await ctx.send(embed=kickem)
            await self.client.get_channel(channel).send(f'{member} was kicked by {ctx.author.name} \n User Id: {ctx.author.id} in {ctx.guild} \n \n \n **CTX** \n {ctx} \n -----------------------------------')
        except discord.Forbidden:
            await ctx.respond('No Perms')


def setup(client):
    client.add_cog(staff(client))
