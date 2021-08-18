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
    with open('json/data.json', 'r') as f:
        prefixes = json.load(f)

    guildID = str(message.guild.id)
    return prefixes[f"{guildID} prefix"]


client = commands.Bot(command_prefix = get_prefix, intents=intents, case_insensitive=True)
client.remove_command('help')
prefix = ["PREFIXES","HERE"]
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
    with open('json/data.json', 'r') as lf:
        leave = json.load(lf)
    with open('json/data.json', 'r') as wf:
        welcome = json.load(wf)
    with open('json/data.json', 'r') as f:
        prefixes = json.load(f)

    idGuild = str(guild.id)

    leave[f"{idGuild} leave"] = False
    leave[f"{idGuild} leaveChannel"] = False
    welcome[f"{idGuild} welcome"] = False
    welcome[f"{idGuild} welcomeChannel"] = False
    prefixes[f"{idGuild} prefix"] = prefix

    with open('json/data.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    with open('json/data.json', 'w') as wf:
        json.dump(welcome, wf, indent=4)
    with open('json/data.json', 'w') as lf:
        json.dump(leave, lf, indent=4)

@client.event
async def on_guild_remove(guild):
    with open('json/data.json', 'r') as lf:
        leave = json.load(lf)
    with open('json/data.json', 'r') as wf:
        welcome = json.load(wf)
    with open('json/data.json', 'r') as f:
        prefixes = json.load(f)

    idGuild = str(guild.id)

    leave.pop(f"{idGuild} leaveChannel")
    leave.pop(f"{idGuild} leave")
    welcome.pop(f"{idGuild} welcomeChannel")
    welcome.pop(f"{idGuild} welcome")
    prefixes.pop(f"{idGuild} prefix")

    with open('json/data.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    with open('json/data.json', 'w') as wf:
        json.dump(welcome, wf, indent=4)
    with open('json/data.json', 'w') as lf:
        json.dump(leave, lf, indent=4)

 
# le comands

#changing the status
@tasks.loop(seconds=30)
async def changeStatus():
    await client.change_presence(activity=discord.Game(next(statuses),status=discord.Status.idle))

@client.event
async def on_message(message):
    if message.author.id == client.user.id:
        return
    
    await client.process_commands(message)

    with open('json/data.json', 'r') as f:
        sayCheck = json.load(f)

    senderID = f'{message.author.id} say'

    if senderID not in sayCheck:
        with open('json/data.json', 'r') as nf:
            sNew = json.load(nf)

        sNew[f'{message.author.id} say'] = False

        with open('json/data.json', 'w') as nf:
            json.dump(sNew, nf, indent=4)
        return

    sayContent = sayCheck[f'{message.author.id} say']

    if sayContent == True:
        message_components = message.content.split()
        if "@everyone" in message_components or "@here" in message_components:
            await message.channel.send("You cannot have everyone or here in your message!")
            return
        await message.delete()
        await message.channel.send(message.content)
        return
    if sayContent == False:
        return

@client.event
async def on_member_join(member : discord.Member):
    #welcome messages stuff
    guild = member.guild

    with open('json/data.json', 'r') as wf:
        welcome = json.load(wf)    
    
    idGuild = str(guild.id)
    welcomeChoiceGuild = welcome[f"{idGuild} welcome"]


    if welcomeChoiceGuild == True:
        welcomeChannel = welcome[f"{idGuild} welcomeChannel"]
        welcomeEmbed = discord.Embed(title='New Member', description=f'{member.mention} joined!',color=discord.Colour.random())
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
    guild = member.guild

    with open('json/data.json', 'r') as lf:
        leave = json.load(lf)    
    
    idGuild = str(guild.id)
    leaveChoiceGuild = leave[f"{idGuild} leave"]


    if leaveChoiceGuild == True:
        leaveChannel = leave[f"{idGuild} leaveChannel"]
        leaveEmbed = discord.Embed(title='Member Left', description=f'**{member.mention}** left.',color=discord.Colour.random())
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
    changeStatus.stop()
    await ctx.send("Goodbye.")
    await client.change_presence(activity=discord.Game("Shutting Down."))
    await client.change_presence(status=discord.Status.invisible)
    await client.close()
    await ctx.send("Unable to shutdown.")

def restart_bot():
    os.execv(sys.executable, ['python'] + sys.argv)

@client.command()
@commands.is_owner()
async def restart(ctx):
    changeStatus.stop()
    await client.change_presence(activity=discord.Game("Restarting."))
    await client.change_presence(status=discord.Status.invisible)
    await ctx.send("Restarting.")
    restart_bot()


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
#  
#    status = discord.Embed (
#    color=discord.Colour.random()
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
    msg = await ctx.send("one seccc")
    embed=discord.Embed(
    title=title,
        desc=desc,
        color=discord.Colour.random()
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
 
