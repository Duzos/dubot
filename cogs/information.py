from operator import truediv
import discord
from discord import guild
from discord.ext import commands
import random
import json
from discord.ext.commands.converter import MessageConverter
from discord.ext.commands.core import has_permissions
import requests
from datetime import datetime

# le cog of le other
class Information(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['bcoin','bitc'],name='bitcoin',description='Gets the current price of Bitcoin.')
    async def bitcoin(self, ctx):
        

        await ctx.message.delete()

        response_API = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
        data = response_API.text
        parse_json = json.loads(data)
        bitcoinGBP = parse_json['bpi']['GBP']['rate_float']
        bitcoinUSD = parse_json['bpi']['USD']['rate_float']
        bitcoinEUR = parse_json['bpi']['EUR']['rate_float']


        bitcoinEmbed = discord.Embed(title='Current price of bitcoin',color=discord.Colour.random())
        bitcoinEmbed.add_field(name='(€)EUR',value=round(bitcoinEUR),inline=True)
        bitcoinEmbed.add_field(name='(£)GBP',value=round(bitcoinGBP),inline=True)
        bitcoinEmbed.add_field(name='($)USD',value=round(bitcoinUSD),inline=True)
        bitcoinEmbed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Bitcoin.svg/64px-Bitcoin.svg.png")
        bitcoinEmbed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=bitcoinEmbed)

    @commands.command(name='uptime',description='Tells you how long the bot has been online.')
    async def uptime(self,ctx):
        await ctx.message.delete()

        delta_uptime = datetime.utcnow() - self.client.start_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        uptimeEmbed = discord.Embed(title='Uptime',description=f"{days}d, {hours}h, {minutes}m, {seconds}s",color=discord.Color.random())
        uptimeEmbed.set_thumbnail(url=self.client.user.avatar_url)
        uptimeEmbed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=uptimeEmbed)

    @commands.command(name='ping',description='Tells you the bots ping.')
    async def ping(self, ctx):
        await ctx.message.delete()
        

        pingEmbed = discord.Embed(title=f'Ping of {self.client.user.name}',description=f':stopwatch:  {round(self.client.latency * 1000)}ms',color=discord.Colour.random())
        pingEmbed.set_thumbnail(url=self.client.user.avatar_url)
        pingEmbed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=pingEmbed)
       
    @commands.command(name='avatar', description='Gets you the avatar of someone.')
    async def avatar(self, ctx, user: commands.MemberConverter):
        await ctx.message.delete()
        avatar = user.avatar_url
        
        avatarembed = discord.Embed(description=f'Avatar of {user.mention}',color=discord.Colour.random(),type='image')
        avatarembed.set_image(url=avatar)
        avatarembed.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url
        )
        await ctx.send(embed=avatarembed)

    @commands.command(aliases=['channelinfo','cinfo'],name='channel_info',description='Gives info on a channel.')
    async def channel_info(self, ctx, channel: commands.TextChannelConverter):
        await ctx.message.delete()
        date_format = "%a, %d %b %Y %I:%M %p"
        

        cinfoEmbed = discord.Embed(title=f'Info on {channel.name}',description=f'**Topic:**\n```{channel.topic}```\n**ID:**\n```{channel.id}```\n**Type:**\n```{channel.type}```\n**Category:**\n```{channel.category}```\n**Channel Created On:**\n```{channel.created_at.strftime(date_format)}```',color=discord.Colour.random())
        cinfoEmbed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=cinfoEmbed)

    @commands.command(aliases=['roleinfo','rinfo'],name='role_info',description='Gives info on a role.')
    async def role_info(self, ctx, role: commands.RoleConverter):
        await ctx.message.delete()
        date_format = "%a, %d %b %Y %I:%M %p"
        memberList = ", ".join([str(m.name) for m in role.members])

        rinfoEmbed = discord.Embed(title=f'Info on {role.name}',description=f'**ID:**\n```{role.id}```\n**Can be Mentioned:**\n```{role.mentionable}```\n**Position:**\n```{role.position}```\n**Role Created On:**\n```{role.created_at.strftime(date_format)}```\n**Colour:**\n```{role.colour}```\n**Members:**\n```{memberList}```',color=role.colour)
        rinfoEmbed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=rinfoEmbed)

    @commands.command(aliases=['guildinfo','ginfo','serverinfo','server_info','sinfo'],name='guild_info',description='Gives info on the guild.')
    async def guild_info(self, ctx):
        await ctx.message.delete()
        guild = ctx.guild
        date_format = "%a, %d %b %Y %I:%M %p"
        
        roleList = ", ".join([str(r.name) for r in guild.roles])

        ginfoEmbed = discord.Embed(title=f'Info on {guild.name}',description=f'**Description:**\n```{guild.description}```\n**Member Count:**\n```{guild.member_count}```\n**Owner:**\n```{guild.owner}```\n**Roles:**\n```{roleList}```\n**Boost Level:**\n```{guild.premium_tier}```\n**Boost Count:**\n```{guild.premium_subscription_count}```\n**ID:**\n```{guild.id}```\n**Guild Created On:**\n```{guild.created_at.strftime(date_format)}```\n**Region:**\n```{guild.region}```',color=discord.Colour.random())
        ginfoEmbed.set_thumbnail(url=guild.icon_url)
        ginfoEmbed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=ginfoEmbed)

    @commands.command(aliases=['userinfo','uinfo'],name='user_info',description='Gives info on a user.')
    async def user_info(self, ctx, member: commands.MemberConverter):
        await ctx.message.delete()
        rolelist = [r.name for r in member.roles if r != ctx.guild.default_role]
        roles = ", ".join(rolelist)
        date_format = "%a, %d %b %Y %I:%M %p"
        
        uinfoEmbed = discord.Embed(title=f'Info on {member.name}#{member.discriminator}', description=f'**ID:**\n```{member.id}```\n**Roles:**\n```{roles}```\n**Account Created On:**\n```{member.created_at.strftime(date_format)}```\n**Account Joined Guild On:**\n```{member.joined_at.strftime(date_format)}```\n**Nickname:**\n```{member.nick}```\n**Is Bot:**\n```{member.bot}```',color=discord.Colour.random())
        uinfoEmbed.set_thumbnail(url=member.avatar_url)
        uinfoEmbed.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url
        )
        await ctx.send(embed=uinfoEmbed)
            
     
    @commands.command(aliases=['information'],name='info', description='Tells you info on the bot')
    async def info(self, ctx):
        await ctx.message.delete()
        title="discord.py | Python"
        description="by Duzo#0001\n<@!327807253052653569>\n[Github Page](https://github.com/Duzos/dubot)"
        
        msg = await ctx.send("one seccc")
        embed=discord.Embed(
            title=title,
            description=description,
            color=discord.Colour.random()
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
    client.add_cog(Information(client))
