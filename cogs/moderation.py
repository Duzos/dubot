import discord
import random
from discord.ext import commands
from discord.ext.commands.core import has_permissions

class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client




    @commands.command(aliases=['comeback', 'revive', 'oops', 'pardon'], permissions=["ban_members"], name='unban', description='Unbans a banned user')
    @has_permissions(ban_members=True)    
    async def unban(self, ctx, *, user=None):
        

        try:
            user = await commands.converter.UserConverter().convert(ctx, user)
        except:
            await ctx.send("User not found!")
            return

        try:
            bans = tuple(ban_entry.user for ban_entry in await ctx.guild.bans())
            if user in bans:
                await ctx.guild.unban(user)
            else:
                await ctx.send("User not banned!")
                return
        except discord.Forbidden:
            await ctx.send("I do not have permission to unban!")
            return

        except:
            await ctx.send("Unbanning failed!")
            return
    
        await ctx.message.delete()
        unbanEmbed = discord.Embed(title='Unban',description=f'{user.mention} has been unbanned.',color=discord.Colour.random())
        unbanEmbed.set_thumbnail(url=self.client.user.avatar_url)
        unbanEmbed.set_author(
                name=ctx.message.author.name,
                icon_url=ctx.message.author.avatar_url
            )
        await ctx.send(embed=unbanEmbed)


    
    @commands.command(aliases=['goawayforever'], name='ban', description='Bans a user')
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member : commands.MemberConverter, *, reason=None):
        await ctx.message.delete()
        
        if member.id == 509436097835827210:
            await ctx.send(f"Unable to ban **{member.name}**: Person too epic")
            return
        if member.id == 327807253052653569:
            await ctx.send(f"Unable to ban **{member.name}**: Person too epic")
            return
        if member.id == 578844127878184961:
            await ctx.send(f"Unable to ban **{member.name}**: Person too epic")
            return
        await member.ban(reason=reason)
        banEmbed = discord.Embed(title='Ban',description=f'**{member.display_name}** has been banned for **{reason}**', color=discord.Colour.random())
        banEmbed.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url
        )
        banEmbed.set_thumbnail(url=self.client.user.avatar_url)
        await ctx.send(embed=banEmbed)

    @commands.command(name='slowmode', description='Adds slowmode to a channel, limit is 21600')
    @has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int):
        await ctx.message.delete()
        
        await ctx.channel.edit(slowmode_delay=seconds)
        slowEmbed = discord.Embed(title='Slowmode',description=f'Slowmode is now on **{seconds}** seconds.',color=discord.Colour.random())
        slowEmbed.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url
        )
        slowEmbed.set_thumbnail(url=self.client.user.avatar_url)
        await ctx.send(embed=slowEmbed)

    @commands.command(aliases=['goaway'], name='kick', description='Kicks a user')
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member : commands.MemberConverter, *, reason=None):
        
        await ctx.message.delete()
        if member.id == 509436097835827210:
            await ctx.send(f"Unable to ban **{member.name}**: Person too epic")
            return
        if member.id == 327807253052653569:
            await ctx.send(f"Unable to ban **{member.name}**: Person too epic")
            return
        if member.id == 578844127878184961:
            await ctx.send(f"Unable to ban **{member.name}**: Person too epic")
            return
        await member.kick(reason=reason)
        kickEmbed = discord.Embed(title='Kick',description=f'**{member.name}** has been kicked for **{reason}**',color=discord.Colour.random())
        kickEmbed.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url
        )
        kickEmbed.set_thumbnail(url=self.client.user.avatar_url)
        await ctx.send(embed=kickEmbed)

    @commands.command(name='clear', description='Clears the amount of messages you want')
    @has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=2):
        await ctx.channel.purge(limit=amount)

def setup(client):
    client.add_cog(Moderation(client))