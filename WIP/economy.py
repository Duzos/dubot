import json
from typing import Tuple
import discord
from discord.ext import commands
import datetime
import random

class Economy(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['econsetup'],name='economysetup',description='Redos the setup of your bank.')
    async def economysetup(self, ctx):
        with open('wip/econ.json', 'r') as ef:
            econ = json.load(ef)

        askMessage = await ctx.send("What's your messaage?")
        OtherMessage = await self.client.wait_for('message', check=check)
        

        econ[str(ctx.message.author.id)] = 0
        econ[f"{ctx.message.author.id} say"] = False
        #econ[f"{ctx.message.author.id} Daily"] = str(datetime.date(2000,1,1))

        with open('wip/econ.json', 'w') as ef:
            json.dump(econ, ef, indent=4)

        await ctx.message.delete()
        setupEmbed = discord.Embed(title='Setup Complete',description=f'Completed economy setup for: {ctx.message.author.mention}',color=discord.Colour.random())
        setupEmbed.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url
            )
        setupEmbed.set_thumbnail(url=self.client.user.avatar_url)
        await ctx.send(embed=setupEmbed)

    @commands.command(name='daily',description='Gives you your daily D10')
    async def daily(self, ctx):
        with open('wip/econ.json', 'r') as ef:
            econ = json.load(ef)
        
        #econ[f"{ctx.message.author.id} Daily"] = str(datetime.datetime.today)
        currentBal = econ[str(ctx.message.author.id)]
        newBal = currentBal + 10
        econ[str(ctx.message.author.id)] = newBal
        with open('wip/econ.json', 'w') as ef:
            json.dump(econ, ef, indent=4)
        dailyEmbed=discord.Embed(title="Daily",description=f'Your new balance is: D${newBal}',color=discord.Colour.random())
        dailyEmbed.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url
            )
        dailyEmbed.set_thumbnail(url=self.client.user.avatar_url)
        await ctx.send(embed=dailyEmbed)

    @commands.command(name='buy',description='lets you buy a command')
    async def buy(self,ctx, command=None):
        with open('wip/econ.json', 'r') as ef:
            econ = json.load(ef)
        bal=econ[str(ctx.message.author.id)]
        

        if command == None:
            storeEmbed=discord.Embed(title='Selections:',description='Say - D$10',color=discord.Colour.random())
            await ctx.send(embed=storeEmbed)
            return
        if command == "say":
            if econ[f"{ctx.message.author.id} say"] == True:
                ownedEmbed=discord.Embed(title='Already Owned!',description='You already own this command!')
                await ctx.send(embed=ownedEmbed)
                return
            if bal >= 10:
                econ[f"{ctx.message.author.id} say"] = True
                newBal=bal-10
                econ[str(ctx.message.author.id)] = newBal
                await ctx.send("Successfully bought the say command")
                with open('wip/econ.json', 'w') as ef:
                    json.dump(econ, ef, indent=4)
                return
            else:
                await ctx.send("Invalid funds!")
                return

    @commands.command(aliases=['bal'],name='balance',description='Tells you your balance.')
    async def balance(self, ctx):
        with open('wip/econ.json', 'r') as ef:
            econ = json.load(ef)
        
        bal=econ[str(ctx.message.author.id)]
        await ctx.send(f"Your balance is: D{bal}.")
        
def setup(client):
    client.add_cog(Economy(client))