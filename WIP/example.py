import discord
from discord.ext import commands

class example(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='exampleCommand',description='Example')
    async def exampleCommand(ctx):
        await ctx.send("Example Response")

def setup(client):
    client.add_cog(example(client))