# le importing
from asyncio.windows_events import NULL
import discord
import json
import random
import os
import sys
from discord.ext import commands
from discord.ext.commands.core import has_permissions
from discord.message import Message
from discord.utils import get
from discord import Member
from discord.ext import tasks
from itertools import cycle
#le intents
intents = discord.Intents.default()
intents.presences = False
intents.members = True
# le client stuff

def get_prefix(client, message):
    with open('json/prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]


client = commands.Bot(command_prefix = get_prefix, intents=intents)
client.remove_command('help')
token = 'TOKENHERE'
statuses = cycle(["statuses","here"])
#le on le ready
@client.event
async def on_ready():
    changeStatus.start()
    print(f'{client.user.name} is ready')
    #await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(client.guilds)} servers!"))

#le error handling
@client.event
async def on_command_error(ctx, error):
    errorEmbed = discord.Embed(title='ERROR',description=error,color=0x992D22)
    errorEmbed.set_author(
        name=ctx.message.author.name,
        icon_url=ctx.message.author.avatar_url
    )
    errorEmbed.set_thumbnail(url=client.user.avatar_url)
    await ctx.send(embed=errorEmbed)

#le stuff that involves json
@client.event
async def on_guild_join(guild):
    with open('json/leave.json', 'r') as lf:
        leave = json.load(lf)
    with open('json/welcome.json', 'r') as wf:
        welcome = json.load(wf)
    with open('json/prefixes.json', 'r') as f:
        prefixes = json.load(f)

    idGuild = str(guild.id)

    leave[str(guild.id)] = False
    leave[f"{idGuild} Channel"] = False
    welcome[str(guild.id)] = False
    welcome[f"{idGuild} Channel"] = False
    prefixes[str(guild.id)] = ['d.','D.']

    with open('json/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    with open('json/welcome.json', 'w') as wf:
        json.dump(welcome, wf, indent=4)
    with open('json/leave.json', 'w') as lf:
        json.dump(leave, lf, indent=4   )

@client.event
async def on_guild_remove(guild):
    with open('json/leave.json', 'r') as lf:
        leave = json.load(lf)
    with open('json/welcome.json', 'r') as wf:
        welcome = json.load(wf)
    with open('json/prefixes.json', 'r') as f:
        prefixes = json.load(f)

    idGuild = str(guild.id)

    leave.pop(f"{idGuild} Channel")
    leave.pop(str(guild.id))
    welcome.pop(f"{idGuild} Channel")
    welcome.pop(str(guild.id))
    prefixes.pop(str(guild.id))

    with open('json/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    with open('json/welcome.json', 'w') as wf:
        json.dump(welcome, wf, indent=4)
    with open('json/leave.json', 'w') as lf:
        json.dump(leave, lf, indent=4)

 

#le colour list
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



# le comands

#changing the status
@tasks.loop(seconds=30)
async def changeStatus():
    await client.change_presence(activity=discord.Game(next(statuses),status=discord.Status.idle))

@client.event
async def on_member_join(member : discord.Member):
    color_list = [c for c in colors.values()]
    guild = member.guild

    with open('welcome.json', 'r') as wf:
        welcome = json.load(wf)    
    
    idGuild = str(guild.id)
    welcomeChoiceGuild = welcome[idGuild]


    if welcomeChoiceGuild == True:
        welcomeChannel = welcome[f"{idGuild} Channel"]
        welcomeEmbed = discord.Embed(title='New Member', description=f'{member.mention} joined!',color=random.choice(color_list))
        welcomeEmbed.set_thumbnail(url=member.avatar_url)
        welcomeEmbed.set_author(
            name=client.user.display_name,
            icon_url=client.user.avatar_url
            )
        await client.get_channel(welcomeChannel).send(embed=welcomeEmbed)
    else:
        return

@client.event
async def on_member_remove(member : discord.Member):
    color_list = [c for c in colors.values()]
    guild = member.guild

    with open('leave.json', 'r') as lf:
        leave = json.load(lf)    
    
    idGuild = str(guild.id)
    leaveChoiceGuild = leave[idGuild]


    if leaveChoiceGuild == True:
        leaveChannel = leave[f"{idGuild} Channel"]
        leaveEmbed = discord.Embed(title='Member Left', description=f'**{member.mention}** left.',color=random.choice(color_list))
        leaveEmbed.set_thumbnail(url=member.avatar_url)
        leaveEmbed.set_author(
            name=client.user.display_name,
            icon_url=client.user.avatar_url
            )
        await client.get_channel(leaveChannel).send(embed=leaveEmbed)
    else:
        return

@client.command()
@commands.is_owner()
async def idle(ctx, *, text):
    await client.change_presence(status=discord.Status.idle, activity=discord.Game(f"{text}"))
    await ctx.send(f"Changed status to **idle** with a description of **{text}**")

@client.command()
@commands.is_owner()
async def online(ctx, *, text):
    await client.change_presence(status=discord.Status.online, activity=discord.Game(f"{text}"))
    await ctx.send(f"Changed status to **online** with a description of **{text}**")

@client.command()
@commands.is_owner()
async def offline(ctx, *, text):
    await client.change_presence(status=discord.Status.offline, activity=discord.Game(f"{text}"))
    await ctx.send(f"Changed status to **offline** with a description of **{text}**")

@client.command()
@commands.is_owner()
async def dnd(ctx, *, text):
    await client.change_presence(status=discord.Status.dnd, activity=discord.Game(f"{text}"))
    await ctx.send(f"Changed status to **dnd** with a description of **{text}**")


@client.command()
@commands.is_owner()
async def pausebot(ctx):
    await ctx.send("Pausing")
    input("Bot Paused")
    await ctx.send("Unpaused")
    print("Unpaused")

@client.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("Goodbye.")
    await client.change_presence(status=discord.Status.invisible)
    await client.close()
    await ctx.send("Unable to shutdown.")

def restart_bot():
    os.execv(sys.executable, ['python'] + sys.argv)

@client.command()
@commands.is_owner()
async def restart(ctx):
    await ctx.send("Restarting.")
    restart_bot()

@client.command()
async def realping(ctx):
    await ctx.send(f'im so speedy my latency is only {round(client.latency * 1000)}ms')

@client.command()
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send("Successfully loaded")

@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send("Successfully unloaded")

@client.command()
@commands.is_owner()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send("Reload complete.")

#@client.command()
#async def status(ctx, user: discord.Member):
#    color_list = [c for c in colors.values()]
#    status = discord.Embed (
#    color=random.choice(color_list)
#    )
#    
#    stat = user.status
#
#
#    status.add_field(name=f"Status for {user.display_name}", value=f"currently: {stat}")
#
#    await ctx.send(embed=status)


@client.command()
async def test(ctx):
    title="test"
    desc="test"
    color_list = [c for c in colors.values()]
    msg = await ctx.send("one seccc")
    embed=discord.Embed(
    title=title,
        desc=desc,
        color=random.choice(color_list)
    )
    embed.set_thumbnail(url=client.user.avatar_url)
    embed.set_author(
        name=ctx.message.author.name,
        icon_url=ctx.message.author.avatar_url
    )
    await msg.edit(
        embed=embed,
        content=None
    )

@client.command()
async def rawavatar(ctx, user: discord.Member):
    await ctx.send(user.avatar_url)

#@client.event
#async def on_message(message):
    # No infinite bot loops
#    if message.author == client.user or message.author.bot:
#        return
#
#    mention = message.author.mention
#    response = f"hey {mention}, you suck"
#    await message.channel.send(response)


# le cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

# run le bot
client.run(token)
 