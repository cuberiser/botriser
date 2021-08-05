import os
import discord
from discord.ext import commands
import randomstuff
import keep_alive
client = commands.Bot(command_prefix=commands.when_mentioned_or('>'), intents = discord.Intents().all())

apikey = os.environ['api']
ai = randomstuff.AsyncClient(api_key = apikey )


@client.event
async def on_ready():
  print('bot ready')
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='new support server\'s commands'))

@client.event
async def on_member_join(member):
  if member.guild.id == 871789537616089108:
    joinemb = discord.Embed(title = f'{member.name} joined the {member.guild.name}', description=f'Hello {member.mention}, welcome to {member.guild.name}')
    joinemb.set_image(url=member.avatar_url)
    await client.get_channel(872069641323827250).send(f'{member.mention} joined the {member.guild.name}', embed=joinemb)

@client.event
async def on_member_leave(member):
  if member.guild.id == 871789537616089108:
    await client.get_channel(872071696138518538).send(f'{member.mention} left the {member.guild.name} sad')

@client.event
async def on_message(message):
  if client.user == message.author:
    return
  if message.channel.id == 867109320281423882 or message.channel.id == 871790105738772590:
    response = await ai.get_ai_response(message.content)
    await message.reply(response.message)

  await client.process_commands(message)

@client.command(name = 'serverlist')
@commands.has_permissions(administrator=True)
async def sn(ctx):
  async for guild in client.fetch_guilds(limit=15):
    await ctx.send(guild.name)

@client.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.MissingPermissions):
    await ctx.send('You do not have the Permissions to use the command')
  elif isinstance(error, commands.MissingRequiredArgument):
    await ctx.send('A required argument is missing please fill it in')
  elif isinstance(error, commands.NotOwner):
    await ctx.send('You do not own the bot!')
    raise error
  elif isinstance(error, commands.CommandOnCooldown):
    msg = 'You are on cooldown please try the command after {:.2f}s'.format(error.retry_after)
    await ctx.send(msg)
  elif isinstance(error, commands.CommandNotFound):
    await ctx.message.reply('That command does not exist')
  elif isinstance(error, commands.ArgumentParsingError):
    await ctx.send('Failed to process the arguments, please put proper arguments for the command in correct order.')
  else:
    await ctx.send('Some unknown error occured')
    raise error

@client.command()
async def load(ctx, cog):
  await client.load_extension(f'cogs.{cog}')
  await ctx.send(f'I have loaded the {cog}')

@client.command()
async def unload(ctx, cog):
  await client.unload_extension(f'cogs.{cog}')
  await ctx.send(f'I have loaded {cog}')

@client.command()
async def reload(ctx, cog):
  await client.unload_extension(f'cogs.{cog}')
  await client.load_extension(f'cogs.{cog}')
  await ctx.send(f'I have reloaded {cog}')

for cog in os.listdir('cogs'):
  if cog.endswith('.py') and not cog.startswith('_'):
    client.load_extension(f'cogs.{cog[:-3]}')

my_secret = os.environ['token']

keep_alive.keep_alive()
client.run(my_secret)
