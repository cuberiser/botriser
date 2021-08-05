import discord
from discord.ext import commands
from main import client as bot

class mod(commands.Cog):
  def __init__(self, client):
    self.client = client
  
  @commands.Cog.listener()
  async def on_ready(self):
    print('Moderation loaded')
  
  @commands.command(name='purge', aliases=('clear', 'c'))
  @commands.has_permissions(manage_messages=True)
  @commands.guild_only()
  async def clear(self, ctx, amount=5):
    await ctx.channel.purge(limit=amount+1)
  
  @commands.command(case_insensitive=True)
  @commands.has_permissions(kick_members=True)
  @commands.guild_only()
  async def kick(self, ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} has been kicked from {ctx.guild}")
  
  @commands.command(case_insensitive=True)
  @commands.has_permissions(ban_members=True)
  @commands.guild_only()
  async def ban(self, ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} has been banned from {ctx.guild}")
  
  @commands.command(case_insensitive=True,
   description='Locks the current or mentioned channel')
  @commands.has_permissions(manage_channels=True)
  @commands.guild_only()
  async def lock(self, ctx, channel: discord.TextChannel=None):
    if channel is None:
      channel = ctx.channel
    await channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send(f"Sucessfully locked {channel}")
  
  @commands.command(case_insensitive=True,
   description='Locks the current or mentioned channel')
  @commands.has_permissions(manage_channels=True)
  @commands.guild_only()
  async def unlock(self, ctx, channel: discord.TextChannel=None):
    if channel is None:
      channel = ctx.channel
    await channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send(f"Sucessfully unlocked {channel}")

def setup(client):
  client.add_cog(mod(client))