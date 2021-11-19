import os
import nextcord as discord
from nextcord.ext import commands
import randomstuff
import keep_alive
import contextlib
from traceback import format_exception
import io, textwrap

client = commands.Bot(command_prefix=commands.when_mentioned_or('>'),
                      intents=discord.Intents().all())

apikey = os.environ['api']
ai = randomstuff.AsyncClient(api_key=apikey)

client.version = '1.0.1'


@client.event
async def on_ready():
    print('bot ready')
    await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.listening,
                                  name='new support server\'s commands'))


@client.event
async def on_member_join(member):
    if member.guild.id == 752028116809023548:
        emb = discord.Embed(
            title=f'{member.name} joined the {member.guild.name}',
            description=
            f'Welcome {member.mention} to {member.guild.name}, get roles from <#841581457662935060> and <#851346687952027659>'
        )
        await member.guild.get_channel(840465352864956416).send(
            f"{member.mention} welcome to {member.guild.name}", embed=emb)
    else:
        return


@client.event
async def on_member_leave(member):
    if member.guild.id == 871789537616089108:
        await client.get_channel(872071696138518538).send(
            f'{member.mention} left the {member.guild.name} sad')


@client.event
async def on_message(message):
    if client.user == message.author:
        return
    if ("@" in message.content and 
    ("everyone" in message.content.lower()
    or "here" in message.content.lower() or
    ("<@&" in message.content and ">" in message.content))) and message.author.id != 752020937335111801:
        return
    if message.channel.id == 867109320281423882 or message.channel.id == 871790105738772590 or message.channel.id == 852441082855424000:
        response = await ai.get_ai_response(message.content)
        await message.reply(response.message)
    if message.content.startswith(f"<@!{client.user.id}>") and (
            "prefix" in message.content
            or len(message.content) == len(f'<@!{client.user.id}>')):
        await message.reply("My prefix is >")
    await client.process_commands(message)


@client.command(name='serverlist')
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
        msg = 'You are on cooldown please try the command after {:.2f}s'.format(
            error.retry_after)
        await ctx.send(msg)
    elif isinstance(error, commands.CommandNotFound):
        await ctx.message.reply('That command does not exist')
    elif isinstance(error, commands.ArgumentParsingError):
        await ctx.send(
            'Failed to process the arguments, please put proper arguments for the command in correct order.'
        )
    else:
        await ctx.send('Some unknown error occured')
        raise error


@client.command()
@commands.is_owner()
async def load(ctx, cog):
    client.load_extension(f'cogs.{cog}')
    await ctx.send(f'I have loaded the {cog}')


@client.command()
@commands.is_owner()
async def unload(ctx, cog):
    client.unload_extension(f'cogs.{cog}')
    await ctx.send(f'I have loaded {cog}')


@client.command()
@commands.is_owner()
async def reload(ctx, cog):
    client.reload_extension(f'cogs.{cog}')
    await ctx.send(f'I have reloaded {cog}')


@client.command(name='eval')
@commands.is_owner()
async def _eval(ctx, *, code):
    if code.startswith("```") and code.endswith("```"):
        code = "\n".join(code.split("\n")[1:])[:-3]
    lv = {
        "discord": discord,
        "nextcord": discord,
        "commands": commands,
        "client": client,
        "bot": client,
        "ctx": ctx,
        "message": ctx.message,
        "channel": ctx.channel,
        "guild": ctx.guild,
    }
    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout):
        try:
            exec(f"async def func():\n{textwrap.indent(code, '    ')}", lv)
            rv = await lv['func']()
            result = f"{stdout.getvalue()}\n-- {rv}"
        except Exception as e:
            result = "\n".join(format_exception(type(e), e, e.__traceback__))
    
    await ctx.send(f"```py\n{result[0:1900]}\n```")


for cog in os.listdir('cogs'):
    if cog.endswith('.py') and not cog.startswith('_'):
        client.load_extension(f'cogs.{cog[:-3]}')


token = os.environ['token']

keep_alive.keep_alive()
client.run(token)
