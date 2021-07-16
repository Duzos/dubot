import discord
from discord.ext import commands
from discord.ext.commands.core import has_permissions

class Moderation(commands.Cog):

    @commands.command(aliases=['comeback', 'revive', 'oops'], permissions=["ban_members"], name='unban', description='Unbans a banned user')
    @has_permissions(ban_members=True)    
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user  

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'**{user.name}#{user.discriminator}** has been unbanned.')
                return
    
    @commands.command(aliases=['goawayforever'], name='ban', description='Bans a user')
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'**{member.name}** has been banned.')

    @commands.command(name='slowmode', description='Adds slowmode to a channel')
    @has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int):
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f'Slowmode is now on **{seconds}** seconds.')

    @commands.command(aliases=['goaway'], name='kick', description='Kicks a user')
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'**{member.name}** has been kicked.')

    @commands.command(name='clear', description='Clears the amount of messages you want')
    @has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=2):
        await ctx.channel.purge(limit=amount)

def setup(client):
    client.add_cog(Moderation(client))