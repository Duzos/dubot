from operator import truediv
import discord
from discord import guild
from discord.ext import commands
import random
import json
from discord.ext.commands.converter import MessageConverter

from discord.ext.commands.core import has_permissions

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
class Information(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='avatar', description='Gets you the avatar of someone.')
    async def avatar(self, ctx, user: commands.MemberConverter):
        await ctx.message.delete()
        avatar = user.avatar_url
        color_list = [c for c in colors.values()]
        avatarembed = discord.Embed(description=f'Avatar of {user.mention}',color=random.choice(color_list),type='image')
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
        color_list = [c for c in colors.values()]

        cinfoEmbed = discord.Embed(title=f'Info on {channel.name}',description=f'**Topic:**\n```{channel.topic}```\n**ID:**\n```{channel.id}```\n**Type:**\n```{channel.type}```\n**Category:**\n```{channel.category}```\n**Channel Created On:**\n```{channel.created_at.strftime(date_format)}```',color=random.choice(color_list))
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
        color_list = [c for c in colors.values()]
        roleList = ", ".join([str(r.name) for r in guild.roles])

        ginfoEmbed = discord.Embed(title=f'Info on {guild.name}',description=f'**Description:**\n```{guild.description}```\n**Member Count:**\n```{guild.member_count}```\n**Owner:**\n```{guild.owner}```\n**Roles:**\n```{roleList}```\n**Boost Level:**\n```{guild.premium_tier}```\n**Boost Count:**\n```{guild.premium_subscription_count}```\n**ID:**\n```{guild.id}```\n**Guild Created On:**\n```{guild.created_at.strftime(date_format)}```\n**Region:**\n```{guild.region}```',color=random.choice(color_list))
        ginfoEmbed.set_thumbnail(url=guild.icon_url)
        ginfoEmbed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=ginfoEmbed)

    @commands.command(aliases=['userinfo','uinfo'],name='user_info',description='Gives info on a user.')
    async def user_info(self, ctx, member: commands.MemberConverter):
        await ctx.message.delete()
        rolelist = [r.name for r in member.roles if r != ctx.guild.default_role]
        roles = ", ".join(rolelist)
        date_format = "%a, %d %b %Y %I:%M %p"
        color_list = [c for c in colors.values()]
        uinfoEmbed = discord.Embed(title=f'Info on {member.name}#{member.discriminator}', description=f'**ID:**\n```{member.id}```\n**Roles:**\n```{roles}```\n**Account Created On:**\n```{member.created_at.strftime(date_format)}```\n**Account Joined Guild On:**\n```{member.joined_at.strftime(date_format)}```\n**Nickname:**\n```{member.nick}```\n**Is Bot:**\n```{member.bot}```',color=random.choice(color_list))
        uinfoEmbed.set_thumbnail(url=member.avatar_url)
        uinfoEmbed.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url
        )
        await ctx.send(embed=uinfoEmbed)
            
     
    @commands.command(name='info', description='Tells you info on the bot')
    async def info(self, ctx):
        await ctx.message.delete()
        title="discord.py | Python"
        description="by Duzo#0001"
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
    client.add_cog(Information(client))