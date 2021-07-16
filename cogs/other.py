import discord
from discord.ext import commands
import random

colors = {
  'DEFAULT': 0x000000,
  'WHITE': 0xFFFFFF,
  'AQUA': 0x1ABC9C,
  'GREEN': 0x2ECC71,
  'BLUE': 0x3498DB,
  'PURPLE': 0x9B59B6,
  'LUMINOUS_VIVID_PINK': 0xE91E63,
  'GOLD': 0xF1C40F,
  'ORANGE': 0xE67E22,
  'RED': 0xE74C3C,
  'GREY': 0x95A5A6,
  'NAVY': 0x34495E,
  'DARK_AQUA': 0x11806A,
  'DARK_GREEN': 0x1F8B4C,
  'DARK_BLUE': 0x206694,
  'DARK_PURPLE': 0x71368A,
  'DARK_VIVID_PINK': 0xAD1457,
  'DARK_GOLD': 0xC27C0E,
  'DARK_ORANGE': 0xA84300,
  'DARK_RED': 0x992D22,
  'DARK_GREY': 0x979C9F,
  'DARKER_GREY': 0x7F8C8D,
  'LIGHT_GREY': 0xBCC0C0,
  'DARK_NAVY': 0x2C3E50,
  'BLURPLE': 0x7289DA,
  'GREYPLE': 0x99AAB5,
  'DARK_BUT_NOT_BLACK': 0x2C2F33,
  'NOT_QUITE_BLACK': 0x23272A
}

# le cog of le other
class Other(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command(name='testcog', description='Tests if cogs are working')
    async def testcog(self, ctx):
        await ctx.send("it works")

    @commands.command(name='invite', description='Sends the bots invite link')
    async def invite(self, ctx):
        await ctx.send('this is my invite: INVITEHERE')
    
     
    @commands.command(name='info', description='Tells you info on the bot')
    async def info(self, ctx):
        title="Python"
        description="by Duzo"
        color_list = [c for c in colors.values()]
        msg = await ctx.send("one seccc")
        embed=discord.Embed(
            title=title,
            description=description,
            color=random.choice(color_list)
        )
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/768px-Python-logo-notext.svg.png")
        embed.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url
            )
            
        await msg.edit(
            embed=embed,
            content=None
        )
    


def setup(client):
    client.add_cog(Other(client))
