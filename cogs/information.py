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
import json

# le cog of le other
class Information(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command(name='serversetup',description='Run this if you want to setup server information channels.')
    @has_permissions(manage_channels=True)
    async def _serversetup(self, ctx):
        guild = ctx.message.guild
        totalMemberCount = 0
        botMemberCount = 0
        memberCount = 0

        with open('json/data.json','r') as f:
            jsonStats = json.load(f)

        jsonStats[f'{guild.id} stats'] = True

        for member in guild.members:
            totalMemberCount += 1
            if member.bot == True:
                botMemberCount += 1
            else:
                memberCount += 1

        overwrites={
            guild.default_role: discord.PermissionOverwrite(connect=False)
        }
        category = await guild.create_category(name="Server Stats",overwrites=overwrites,reason="Server Stats",position=0)
        totalChannel = await guild.create_voice_channel(f"Total Members: {totalMemberCount}",category=category)
        memberChannel = await guild.create_voice_channel(f"Members: {memberCount}",category=category)
        botChannel = await guild.create_voice_channel(f"Bots: {botMemberCount}",category=category)

        jsonStats[f'{guild.id} stats total'] = totalChannel.id
        jsonStats[f'{guild.id} stats member'] = memberChannel.id
        jsonStats[f'{guild.id} stats bot'] = botChannel.id    

        with open('json/data.json','w') as f:
            json.dump(jsonStats,f,indent=4)

        await ctx.reply("Setup Complete!")

    @commands.command(aliases=['bcoin','bitc'],name='bitcoin',description='Gets the current price of Bitcoin.')
    async def bitcoin(self, ctx,amount=1):
        await ctx.trigger_typing()
        response_API = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
        data = response_API.text
        parse_json = json.loads(data)
        bitcoinGBP = parse_json['bpi']['GBP']['rate_float']
        bitcoinUSD = parse_json['bpi']['USD']['rate_float']
        bitcoinEUR = parse_json['bpi']['EUR']['rate_float']


        bitcoinEmbed = discord.Embed(title=f'Price of {amount} bitcoin',color=discord.Colour.gold())
        bitcoinEmbed.add_field(name='(€)EUR',value=round(bitcoinEUR * amount),inline=True)
        bitcoinEmbed.add_field(name='(£)GBP',value=round(bitcoinGBP*amount),inline=True)
        bitcoinEmbed.add_field(name='($)USD',value=round(bitcoinUSD*amount),inline=True)
        bitcoinEmbed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Bitcoin.svg/64px-Bitcoin.svg.png")
        bitcoinEmbed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
        await ctx.reply(embed=bitcoinEmbed)

    @commands.command(name='uptime',description='Tells you how long the bot has been online.')
    async def uptime(self,ctx):
        
        delta_uptime = datetime.utcnow() - self.client.start_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        uptimeEmbed = discord.Embed(title='Uptime',description=f"{days}d, {hours}h, {minutes}m, {seconds}s",color=discord.Color.random())
        uptimeEmbed.set_thumbnail(url=self.client.user.avatar_url)
        uptimeEmbed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
        await ctx.reply(embed=uptimeEmbed)


    @commands.command(aliases=['test'],name='ping',description='Tells you the bots ping.')
    async def ping(self, ctx):
        

        pingEmbed = discord.Embed(title=f'Ping of {self.client.user.name}',description=f':stopwatch:  {round(self.client.latency * 1000)}ms',color=discord.Colour.random())
        pingEmbed.set_thumbnail(url=self.client.user.avatar_url)
        pingEmbed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
        await ctx.reply(embed=pingEmbed)

    @commands.command(name='avatar', description='Gets you the avatar of someone.')
    async def avatar(self, ctx, user: commands.MemberConverter=None):
        user = user or ctx.message.author
        
        avatar = user.avatar_url

        avatarembed = discord.Embed(description=f'Avatar of {user.mention}',color=discord.Colour.random(),type='image')
        avatarembed.set_image(url=avatar)
        avatarembed.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url
        )
        await ctx.reply(embed=avatarembed)

    @commands.command(aliases=['channelinfo','cinfo'],name='channel_info',description='Gives info on a channel.')
    async def channel_info(self, ctx, channel: commands.TextChannelConverter=None):
        channel = channel or ctx.channel
        
        date_format = "%a, %d %b %Y %I:%M %p"


        cinfoEmbed = discord.Embed(title=f'Info on {channel.name}',description=f'**Topic:**\n```{channel.topic}```\n**ID:**\n```{channel.id}```\n**Type:**\n```{channel.type}```\n**Category:**\n```{channel.category}```\n**Channel Created On:**\n```{channel.created_at.strftime(date_format)}```',color=discord.Colour.random())
        cinfoEmbed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
        await ctx.reply(embed=cinfoEmbed)

    @commands.command(aliases=['roleinfo','rinfo'],name='role_info',description='Gives info on a role.')
    async def role_info(self, ctx, role: commands.RoleConverter):
        date_format = "%a, %d %b %Y %I:%M %p"
        memberList = ", ".join([str(m.name) for m in role.members])
        permissionList = ', '.join([perm[0] for perm in role.permissions if perm[1]])

        rinfoEmbed = discord.Embed(title=f'Info on {role.name}',description=f'**ID:**\n```{role.id}```\n**Can be Mentioned:**\n```{role.mentionable}```\n**Position:**\n```{role.position}```\n**Role Created On:**\n```{role.created_at.strftime(date_format)}```\n**Colour:**\n```{role.colour}```\n**Permissions:**\n```{permissionList}```\n**Members:**\n```{memberList}```',color=role.colour)
        rinfoEmbed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
        await ctx.reply(embed=rinfoEmbed)

    @commands.command(aliases=['guildinfo','ginfo','serverinfo','server_info','sinfo'],name='guild_info',description='Gives info on the guild.')
    async def guild_info(self, ctx):
        
        guild = ctx.guild
        date_format = "%a, %d %b %Y %I:%M %p"

        roleList = ", ".join([str(r.name) for r in guild.roles])

        ginfoEmbed = discord.Embed(title=f'Info on {guild.name}',description=f'**Description:**\n```{guild.description}```\n**Member Count:**\n```{guild.member_count}```\n**Owner:**\n```{guild.owner}```\n**Roles:**\n```{roleList}```\n**Boost Level:**\n```{guild.premium_tier}```\n**Boost Count:**\n```{guild.premium_subscription_count}```\n**ID:**\n```{guild.id}```\n**Guild Created On:**\n```{guild.created_at.strftime(date_format)}```\n**Region:**\n```{guild.region}```',color=discord.Colour.random())
        ginfoEmbed.set_thumbnail(url=guild.icon_url)
        ginfoEmbed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
        await ctx.reply(embed=ginfoEmbed)



    @commands.command(aliases=['userinfo','uinfo'],name='user_info',description='Gives info on a user.')
    async def user_info(self, ctx, member: commands.MemberConverter=None):
        member = member or ctx.message.author
        permissionList = ', '.join([perm[0] for perm in member.guild_permissions if perm[1]])
        rolelist = [r.name for r in member.roles if r != ctx.guild.default_role]
        roles = ", ".join(rolelist)
        if roles == "":
            roles=None
        date_format = "%a, %d %b %Y %I:%M %p"
        uinfoEmbed = discord.Embed(title=f'Info on {member.name}#{member.discriminator}', description=f'**ID:**\n`{member.id}`\n**Roles:**\n`{roles}`\n**Account Created On:**\n`{member.created_at.strftime(date_format)}`\n**Account Joined Guild On:**\n`{member.joined_at.strftime(date_format)}`\n**Nickname:**\n`{member.nick}`\n**Is Bot:**\n`{member.bot}`\n**Permissions:**\n`{permissionList}`',color=discord.Colour.random())
        uinfoEmbed.set_thumbnail(url=member.avatar_url)
        uinfoEmbed.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url
        )
        await ctx.reply(embed=uinfoEmbed)
            
    @commands.command(name='invite', description='Sends the bots invite link')
    async def invite(self, ctx):
        
        inviteEmbed = discord.Embed(title="Invite Link",description="[Bot Invite](https://discord.com/api/oauth2/authorize?client_id=865190020179296267&permissions=0&scope=bot%20applications.commands)",color=discord.Colour.random())
        inviteEmbed.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url
            )
        inviteEmbed.set_thumbnail(url=self.client.user.avatar_url)
        inviteEmbed.add_field(name='Support Server',value="[Server Invite](https://discord.gg/Raakw6367z)",inline=False)
        inviteEmbed.add_field(name='Get Dubot Slash!',value="[Dubot Slash Invite](https://discord.com/api/oauth2/authorize?client_id=900481597311172660&permissions=0&scope=bot%20applications.commands)",inline=False)
        await ctx.reply(embed=inviteEmbed)

    @commands.command(aliases=['information'],name='info', description='Tells you info on the bot')
    async def info(self, ctx):
        
        title="discord.py | Python"
        description="by <@!327807253052653569>\n[Github Page](https://github.com/Duzos/dubot)\n[Support Server](https://discord.gg/Raakw6367z)"

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
            
        await ctx.reply(embed=embed)

    @commands.command(name='prefixes',description='Gives you the prefixes.')
    async def prefixes(self,ctx):
        with open('json/data.json','r') as f:
            jsonPrefix = json.load(f)

        guildID = str(ctx.guild.id)
        currentPrefixes = jsonPrefix[f"{guildID} prefix"] 

        prefixEmbed = discord.Embed(title='Prefixes',description=currentPrefixes,color=discord.Colour.random())
        prefixEmbed.set_thumbnail(url=ctx.guild.icon_url)
        prefixEmbed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)                            
        await ctx.reply(embed=prefixEmbed)
        

def setup(client):
    client.add_cog(Information(client))