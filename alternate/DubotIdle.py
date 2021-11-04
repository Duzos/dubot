import discord
from discord.ext import commands

client = commands.Bot(command_prefix='botoverride.')
client.remove_command('help')
token = 'ODY1MTkwMDIwMTc5Mjk2MjY3.YPAY_w.sqazc0J3MavapwVtOPFGomtlmuA'

@client.event
async def on_ready():
    print(f'{client.user.name} is now in maintenance mode.')
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("in Maintenance Mode."))

@client.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("Goodbye.")
    await client.change_presence(status=discord.Status.offline)
    await client.close()
    await ctx.send("Unable to shutdown.")

client.run(token)