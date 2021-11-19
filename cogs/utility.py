import nextcord as discord
from nextcord.ext import commands
from main import client as bot

class utility(commands.Cog):
  def __init__(self, client):
    self.client = client
  
  @commands.Cog.listener()
  async def on_ready(self):
    print('The utility commands have been loaded')
  
  @commands.command(name='userinfo', aliases=['whois'], description = "gets a user's info")
  async def userinfo(self, ctx, *, member: discord.Member=None):
    if member is None:
      member = ctx.author
    roles = [role for role in member.roles]
    user_embed = discord.Embed(colour=member.colour)
    user_embed.set_footer(icon_url=ctx.author.avatar_url, text=f'Requested by {ctx.author.name}')
    user_embed.add_field(name="Member's name: ", value=member.name, inline=False)
    user_embed.add_field(name="Member's ID: ", value = member.id, inline=False)
    user_embed.add_field(name=f'Roles({len(roles)}):', value="".join([role.mention for role in roles]), inline=False)
    user_embed.set_image(url = member.avatar_url)
    await ctx.send(embed=user_embed)
  
  @commands.command(case_insensitive=True)
  async def ping(self, ctx):
    await ctx.send(f'Ping is {round(bot.latency * 1000)} ms')

  @commands.command(case_insensitive=True)
  @commands.cooldown(1, 10, commands.BucketType.user)
  async def say(self, ctx, *, saymsg=None):
    if saymsg==None:
      return await ctx.send("No message type in something")
    
    sayEmbed = discord.Embed(title=f"{ctx.author.name} said ", color = discord.Color.red(), description=f"{saymsg}")
    
    await ctx.send(embed = sayEmbed)

def setup(client):
  client.add_cog(utility(client))
