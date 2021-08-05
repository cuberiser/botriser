import discord
from discord.ext import commands
from main import client as bot

class misc(commands.Cog):
  def __init__(self, client):
    self.client = client
  
  @commands.Cog.listener()
  async def on_ready(self):
    print('Loaded the miscallaneous commands')
  
  @commands.command()
  @commands.is_owner()
  async def playing(self, ctx, *, playmessage):
    await bot.change_presence(activity = discord.Activity(type = discord.ActivityType.playing, name  = f'{playmessage}'))

    await ctx.send(f'status changed to playing {playmessage}')

  @commands.command()
  @commands.is_owner()
  async def comp(self, ctx, *, compmessage):
    await bot.change_presence(activity = discord.Activity(type = discord.ActivityType.competing, name  = f'{compmessage}'))

    await ctx.send(f'status changed to competing in {compmessage}')

  @commands.command()
  @commands.is_owner()
  async def listening(self, ctx, *, listmessage):
    await bot.change_presence(activity = discord.Activity(type = discord.ActivityType.listening, name  = f'{listmessage}'))

    await ctx.send(f'status changed to listening to {listmessage}')

  @commands.command()
  @commands.is_owner()
  async def watching(self, ctx, *, watchmessage):
    await bot.change_presence(activity = discord.Activity(type = discord.ActivityType.watching, name  = f'{watchmessage}'))

    await ctx.send(f'status changed to watching {watchmessage}')
  
  
def setup(client):
  client.add_cog(misc(client))