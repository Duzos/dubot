# =====================
# INFO:
# Most of this code is very messy and unorganised, just a warning.
# I recommend you check out dubot-slash as it is a better version of this!
# - Duzo
# =====================

# le importing
import discord
from discord_slash import SlashCommand,SlashContext
from discord_slash.utils.manage_commands import create_choice,create_option
import json
import random
import os
import sys
from discord import guild
from discord import permissions
from discord.ext import commands
from discord.ext.commands.core import has_permissions, is_owner
from discord.ext.commands.errors import MissingPermissions
from discord.message import Message
from discord.utils import get
from discord import Member
from discord.ext import tasks
from itertools import cycle
import time
from datetime import datetime

#le intents
intents = discord.Intents.default()
intents.presences = True
intents.members = True
# le client stuff

def get_prefix(client, message):
    with open('json/data.json', 'r') as f:
        prefixes = json.load(f)

    guildID = str(message.guild.id)
    return prefixes[f"{guildID} prefix"]


client = commands.Bot(command_prefix = get_prefix, intents=intents, case_insensitive=True)
slash =  SlashCommand(client,sync_commands=True)
client.remove_command('help')
statusList=['Running on the Server','d.help','in Python','RIP north west development']
statuses = cycle(statusList)

with open('config.json','r') as cf:
    config = json.load(cf)

token = config['token']
prefix = config['prefix']

#le on le ready
@client.event
async def on_ready():
    client.start_time = datetime.utcnow()
    statusList.append(f"in {len(client.guilds)} servers.")
    changeStatus.start()
    print(f'{client.user.name} is ready')

#le error handling
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound) or isinstance(error, commands.NotOwner) or isinstance(error, commands.NoPrivateMessage):
        return
    elif isinstance(error, commands.BotMissingPermissions):
        botPermEmbed = discord.Embed(title='ERROR',description='The Bot is missing the required permission(s).',color=0x992D22)
        permValues = ''
        for perm in error.missing_perms:
            permValues = permValues+ f"{perm}\n"
        botPermEmbed.add_field(name="Missing Permission(s):",value=permValues,inline=False)
        botPermEmbed.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url
        )
        botPermEmbed.set_thumbnail(url=client.user.avatar_url)
        await ctx.send(embed=botPermEmbed)
        return
    elif isinstance(error, commands.MissingPermissions):
        botPermEmbed = discord.Embed(title='ERROR',description='You are missing the required permission(s).',color=0x992D22)
        permValues = ''
        for perm in error.missing_perms:
            permValues = permValues+ f"{perm}\n"
        botPermEmbed.add_field(name="Missing Permission(s):",value=permValues,inline=False)
        botPermEmbed.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url
        )
        botPermEmbed.set_thumbnail(url=client.user.avatar_url)
        await ctx.send(embed=botPermEmbed)
        return
    else:
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
    with open('json/data.json', 'r') as f:
        joinSetup = json.load(f)

    idGuild = str(guild.id)

    joinSetup[f"{idGuild} leave"] = False
    joinSetup[f"{idGuild} leaveChannel"] = False
    joinSetup[f"{idGuild} welcome"] = False
    joinSetup[f"{idGuild} welcomeChannel"] = False
    joinSetup[f"{idGuild} prefix"] = prefix

    with open('json/data.json', 'w') as f:
        json.dump(joinSetup, f, indent=4)


@client.event
async def on_guild_remove(guild):
    with open('json/data.json', 'r') as f:
        leave = json.load(f)


    idGuild = str(guild.id)

    leave.pop(f"{idGuild} leaveChannel")
    leave.pop(f"{idGuild} leave")
    leave.pop(f"{idGuild} welcomeChannel")
    leave.pop(f"{idGuild} welcome")
    leave.pop(f"{idGuild} prefix")


    with open('json/data.json', 'w') as f:
        json.dump(leave, f, indent=4)

@client.command()
@is_owner()
async def owner_help(ctx):
    oEmbed = discord.Embed(title='Owner Help',color=discord.Colour.random())
    oEmbed.set_thumbnail(url=client.user.avatar_url)
    oEmbed.set_footer(text=f'Requested by {ctx.message.author.name}',icon_url=client.user.avatar_url)
    oEmbed.add_field(name="Commands:",value="**Owner_Hel|p** - This command\n**DataReset** - Resets the data for a specific server\n**DataResetAll** - Resets all the data for every server.\n**Online** - Sets the bots status to online\n**Idle** - Sets the bots status to idle\n**Offline** - Sets the bots status to offline\n**DND** - Sets the bots status to DND\n**PauseBot** - Pauses the bot in the console\n**Shutdown** - Shuts the bot down\n**Restart** - Restarts the bot\n**Load** - Loads an unloaded cog\n**Unload** - Unloads a loaded cog\n**Reload** - Reloads a loaded cog\n**server_list** - DMs the owner with a list of servers the bot is in\n**server_info_owner** - DMs the owner with info on a server\n**server_invite_owner** - DMs the owner with an invite to a server\n**startStatus** - Restarts the auto-status\n**WIPLoad** - Loads a WIP cog\n**WIPUnload** - Unloads a WIP cog\n**WIPReload** - Reloads a WIP cog\n**IdeaApprove** - Approve an idea\n**IdeaDeny** - Deny an Idea\n")
    await ctx.send(embed=oEmbed)
@client.command()
@is_owner()
async def datareset(ctx):
    def check(ms):
        return ms.channel == ctx.message.channel and ms.author == ctx.message.author

    await ctx.send("are you sure.")
    msg = await client.wait_for('message', check=check)
    if msg.content.upper() == "NO":
        await ctx.send("Cancelling.")
        return
    elif msg.content.upper() == "YES":
        await ctx.send("Proceeding.")
    else:
        await ctx.send("Invalid response.")
        return
    
    message = ""
    for guild in client.guilds:
        message += f"{guild.name}: {guild.id}\n"
    await ctx.send(message)
    await ctx.send("Please choose a server to reset in ID form")
    msg = await client.wait_for('message', check=check)
    guildValue = msg.content
    with open("json/data.json","r") as f:
        add = json.load(f)
        
    add[f"{guildValue} leave"] = False
    add[f"{guildValue} leaveChannel"] = False
    add[f"{guildValue} welcome"] = False
    add[f"{guildValue} welcomeChannel"] = False
    add[f"{guildValue} prefix"] = prefix

    with open("json/data.json","w") as f:
        json.dump(add,f,indent=4)
        
    await ctx.send("complete.")
    
@client.command()
@is_owner()
async def dataresetall(ctx):    
    def check(ms):
        return ms.channel == ctx.message.channel and ms.author == ctx.message.author

    await ctx.send("are you sure.")
    msg = await client.wait_for('message', check=check)
    if msg.content == "no":
        await ctx.send("Cancelling.")
        return
    elif msg.content == "yes":
        await ctx.send("Proceeding.")
    else:
        await ctx.send("Invalid response.")
        return

    for guild in client.guilds:
        guildValue = guild.id
        with open("json/data.json","r") as f:
            add = json.load(f)
            
        add[f"{guildValue} leave"] = False
        add[f"{guildValue} leaveChannel"] = False
        add[f"{guildValue} welcome"] = False
        add[f"{guildValue} welcomeChannel"] = False
        add[f"{guildValue} prefix"] = prefix

        with open("json/data.json","w") as f:
            json.dump(add,f,indent=4)
    await ctx.send("Complete.")
        


#@client.event
#async def on_member_update(before, after):
#
#    if before.status != after.status:  # to only run on status
#        embed = discord.Embed(title=f"Changed status")
#        embed.add_field(name='User', value=before.mention)
#        embed.add_field(name='Before', value=before.status)
#        embed.add_field(name='After', value=after.status)#
        # send to admin or channel you choose
#        admin = client.get_user(327807253052653569)  # admin to notify
#        await admin.send(embed=embed)
#        return

# le comands

#@client.event
#async def on_message(message):
#    if message.author == client.user:
#        return
#    if message.content == "amogus":
#        await message.channel.send("sus")
#    if message.content == "sus":
#        await message.channel.send("amogus")
#    await client.process_commands(message)

#changing the status
@tasks.loop(seconds=30)
async def changeStatus():
    await client.change_presence(activity=discord.Game(next(statuses),status=discord.Status.idle))

@client.event
async def on_message(message):
    # Blocked users.
    with open('json/blocked.json','r') as bf:
        blocked = json.load(bf)
    if f"{message.author.id}" in blocked:
        return
    # if the message is the bot, dont work.
    if message.author.id == client.user.id:
        return
    #run the command.    
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

#@client.command()
#@commands.is_owner()
#async def setbal(ctx, amount=0):
#    with open('json/econ.json', 'r') as ef:
#        econ = json.load(ef)
#    
#    econ[str(ctx.message.author.id)] = amount
#
#    with open('json/econ.json', 'w') as ef:
#        json.dump(econ, ef, indent=4)
#    
#    await ctx.send(f"Successfully set your balance to: D{amount}")

@client.command()
async def voicetest(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()
    guild = ctx.guild
    voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=guild)
    audio_source = discord.FFmpegPCMAudio('test.mp3')
    if not voice_client.is_playing():
        voice_client.play(audio_source, after=None)

# @client.command()
# @commands.is_owner()
# async def override(ctx,command=None,*,query=None):
#     if command == None:
#         return
    
#     await ctx.invoke(client.get_command(command),user=query)

@client.command()
@commands.is_owner()
async def idle(ctx, *, text):
    changeStatus.stop()
    await client.change_presence(status=discord.Status.idle, activity=discord.Game(f"{text}"))
    await ctx.send(f"Changed status to **idle** with a description of **{text}**")

@client.command()
@commands.is_owner()
async def online(ctx, *, text):
    changeStatus.stop()
    await client.change_presence(status=discord.Status.online, activity=discord.Game(f"{text}"))
    await ctx.send(f"Changed status to **online** with a description of **{text}**")

@client.command()
@commands.is_owner()
async def offline(ctx, *, text):
    changeStatus.stop()
    await client.change_presence(status=discord.Status.offline, activity=discord.Game(f"{text}"))
    await ctx.send(f"Changed status to **offline** with a description of **{text}**")

@client.command()
@commands.is_owner()
async def dnd(ctx, *, text):
    changeStatus.stop()
    await client.change_presence(status=discord.Status.dnd, activity=discord.Game(f"{text}"))
    await ctx.send(f"Changed status to **dnd** with a description of **{text}**")

@client.command()
@commands.is_owner()
async def startStatus(ctx):
    changeStatus.start()
    await ctx.send("Started status changing again.")

@client.command()
@commands.is_owner()
async def pausebot(ctx):
    await ctx.send("Bot Paused")
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

@client.command()
@is_owner()
async def WIPLoad(ctx, extension):
    client.load_extension(f'WIP.{extension}')
    await ctx.send("Successfully Loaded WIP cog.")

@client.command()
@is_owner()
async def WIPunload(ctx, extension):
    client.unload_extension(f'WIP.{extension}')
    await ctx.send("Successfully unloaded WIP cog.")

@client.command()
@is_owner()
async def WIPreload(ctx,extension):
    client.unload_extension(f'WIP.{extension}')
    client.load_extension(f'WIP.{extension}')
    await ctx.send("WIP reload complete.")

@client.command()
@is_owner()
async def block(ctx,user: commands.MemberConverter=None):
    if user == None:
        await ctx.send("Please provide a user!")
        return

    with open('json/blocked.json','r') as f:
        blockList = json.load(f)
    
    blockList[f"{user.id}"] = user.name

    with open('json/blocked.json','w') as f:
        json.dump(blockList, f, indent=4)
    await ctx.send(f"Blocked {user.name}")

@client.command()
@is_owner()
async def unblock(ctx,user: commands.MemberConverter=None):
    if user == None:
        await ctx.send("Please provide a user!")
        return

    with open('json/blocked.json','r') as f:
        blockList = json.load(f)
    
    blockList.pop(f"{user.id}")

    with open('json/blocked.json','w') as f:
        json.dump(blockList, f, indent=4)
    await ctx.send(f"Unblocked {user.name}")

@client.command()
@is_owner()
async def blocked(ctx):
    with open('json/blocked.json','r') as f:
        blockList = json.load(f)
    
    await ctx.send(blockList)

    with open('json/blocked.json','w') as f:
        json.dump(blockList, f, indent=4)

@client.command()
@commands.is_owner()
async def server_list(ctx):
    await ctx.message.delete()
    duzo = client.get_user(327807253052653569)
    message = ""
    for guild in client.guilds:
        message += f"{guild.name}: {guild.id}\n"
    await duzo.send(f"I am in **{len(client.guilds)}** servers.")
    await duzo.send(message)

@client.command()
@commands.is_owner()
async def server_info_owner(ctx,guild: commands.GuildConverter=None):
    await ctx.message.delete()
    duzo = client.get_user(327807253052653569)
    guild = guild or ctx.guild

    date_format = "%a, %d %b %Y %I:%M %p"

    roleList = ", ".join([str(r.name) for r in guild.roles])

    ginfoEmbed = discord.Embed(title=f'Info on {guild.name}',description=f'**Description:**\n```{guild.description}```\n**Member Count:**\n```{guild.member_count}```\n**Owner:**\n```{guild.owner}```\n**Roles:**\n```{roleList}```\n**Boost Level:**\n```{guild.premium_tier}```\n**Boost Count:**\n```{guild.premium_subscription_count}```\n**ID:**\n```{guild.id}```\n**Guild Created On:**\n```{guild.created_at.strftime(date_format)}```\n**Region:**\n```{guild.region}```',color=discord.Colour.random())
    ginfoEmbed.set_thumbnail(url=guild.icon_url)
    ginfoEmbed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
    await duzo.send(embed=ginfoEmbed)

@client.command()
@commands.is_owner()
async def server_invite_owner(ctx, guild: commands.GuildConverter=None):
    await ctx.message.delete()
    duzo = client.get_user(327807253052653569)
    guild = guild or ctx.guild
    guildChannel = guild.text_channels[0]
    invite = await guildChannel.create_invite(unique=False)
    await duzo.send(f"Here's the invite: {invite}")

@client.command(aliases=['iapprove','ia','iaccept'])
@commands.is_owner()
async def ideaApprove(ctx, idea=None):
    if idea==None:
        return
    with open('json/data.json','r') as f:
        approve = json.load(f)

    approveEmbed = discord.Embed(title='Hooray!',description='Your idea has been approved!',color=discord.Colour.random())
    approveEmbed.set_footer(text=f'Idea ID: {idea}')

    approvePerson = client.get_user(approve[idea])
    await approvePerson.send(embed=approveEmbed)
    await ctx.send(f"Idea {idea} approved.")
    approve.pop(idea)
    with open("json/data.json",'w') as f:
        json.dump(approve, f, indent=4)

@client.command(aliases=['ideny','id'])
@commands.is_owner()
async def ideaDeny(ctx, idea=None):
    if idea==None:
        return
    with open('json/data.json','r') as f:
        deny = json.load(f)

    denyEmbed = discord.Embed(title='Sorry.',description='Your idea has been denied.',color=discord.Colour.random())
    denyEmbed.set_footer(text=f'Idea ID: {idea}')

    denyPerson = client.get_user(deny[idea])
    await denyPerson.send(embed=denyEmbed)
    await ctx.send(f"Idea {idea} denied.")
    deny.pop(idea) 
    with open("json/data.json",'w') as f:
        json.dump(deny, f, indent=4)



@client.command(aliases=["fardultrahd"])
async def fard(ctx):
    fdescription = ""
    fardmessages = ["", "https://media1.tenor.com/images/4829a619ed1a8fbf2369a56f814f589b/tenor.gif?itemid=16776506", "https://media1.tenor.com/images/fe3596baf57eb04ed26698c843d29bca/tenor.gif?itemid=17107071", "https://media.giphy.com/media/QsZol42CPIjMzke1QW/giphy.gif"]
    fardchoice = random.choice(fardmessages)
    if fardchoice == "https://media2.giphy.com/media/QsZol42CPIjMzke1QW/200w_s.gif":
        fdescription = "YOU GOT THE GOLDEN FARD?!!?!???"
    if fardchoice == "https://media1.tenor.com/images/fe3596baf57eb04ed26698c843d29bca/tenor.gif?itemid=17107071":
        fdescription = "LOL YOU GOT UN;LUCKY FARD????!!!!!!"
    if fardchoice == "https://media1.tenor.com/images/4829a619ed1a8fbf2369a56f814f589b/tenor.gif?itemid=16776506":
        fdescription = "i feels bad for you :pensive: you got the cocomelon jr fard"
    if fardchoice == "":
        fdescription = "YOU GOT NO FARD LOL"
    fardembed = discord.Embed(title=f'{ctx.author.name} farded',description=f'{fdescription}',color=discord.Colour.random(),type='gifv')
    fardembed.set_image(url=fardchoice)
    fardembed.set_author(
        name=ctx.message.author.name,
        icon_url=ctx.message.author.avatar_url
    )
    await ctx.send(embed=fardembed)

@client.command()
async def shootout(ctx):
    await ctx.send("https://tenor.com/view/fat-guy-gun-gif-20983542")
    await ctx.send("https://tenor.com/view/gun-fat-guy-firing-shoot-gif-17510265")



@client.command()
async def satano(ctx):
    satEmbed = discord.Embed(title='**BOW DOWN TO BARNS AND NOBLE**',color=discord.Colour.random(),type='image')
    satEmbed.set_image(url="https://cdn.discordapp.com/attachments/859863853143162961/888534045108101150/images8.jpg")
    await ctx.send(embed=satEmbed)

@client.command()
async def cum3theendofcum(ctx):
    await ctx.send("I'm Andy the hedgehog saying goodbye")

@client.command()
async def cum2electricboogaloo(ctx):
    await ctx.send("**YOU WILL COME WITH US TO ELECTRIC BOOGALOO**")

@client.command()
async def cum(ctx):
    await ctx.send("this is a werd command why did i add this")

@client.command()
async def mzsty(ctx):
    mzstygif = "https://media.tenor.com/images/417f08657d11aaa7cc76be7eaafb9f80/tenor.gif"
    mzstyembed = discord.Embed(title='secret mzsty command',description='',color=discord.Colour.random(),type='gifv')
    mzstyembed.set_image(url=mzstygif)
    mzstyembed.set_author(
        name=ctx.message.author.name,
        icon_url=ctx.message.author.avatar_url
    )
    await ctx.send(embed=mzstyembed)

@client.command()
async def bean(ctx):
    beangif = "https://media1.tenor.com/images/677f726b9f9021915cca17067eb5634a/tenor.gif"
    beanEmbed = discord.Embed(title='omg its mr bean',color=discord.Colour.random(),type='gifv')
    beanEmbed.set_image(url=beangif)
    beanEmbed.set_author(
        name=ctx.message.author.name,
        icon_url=ctx.message.author.avatar_url
    )
    await ctx.send(embed=beanEmbed)


#@client.command()
#async def test(ctx):
#    title="test"
#    desc="test"
#    msg = await ctx.send("one seccc")
#    embed=discord.Embed(
##    title=title,
#        desc=desc,
#        color=discord.Colour.random()
#    )
#    embed.set_thumbnail(url=client.user.avatar_url)
#    embed.set_author(
#        name=ctx.message.author.name,
#        icon_url=ctx.message.author.avatar_url
#    )
#    await msg.edit(
#        embed=embed,
#        content=None
#    )

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