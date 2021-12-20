# Made by Duzo
# ================

# Importing
import discord
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
import topgg

# Getting the prefix for the server

def get_prefix(client, message):
    with open('json/data.json', 'r') as f:
        prefixes = json.load(f)

    guildID = str(message.guild.id)
    return prefixes[f"{guildID} prefix"]

# The bots intents
intents = discord.Intents.default()
intents.presences = True
intents.members = True

# Getting items from the config
with open('config.json','r') as cf:
    config = json.load(cf)

token = config['token']
prefix = config['prefix']
topToken = config['topToken']
ownerID = config['ownerID']

# Setting up the client.
client = commands.Bot(command_prefix = get_prefix, intents=intents, case_insensitive=True)
client.topgg = topgg.DBLClient(bot=client,token=topToken)
client.topgg_webhook = topgg.WebhookManager(client).dbl_webhook(route='/dblwebhook',auth_key='password')
client.topgg_webhook.run(4999)
client.remove_command('help')

# When the bot is ready.
@client.event
async def on_ready():
    try:
        await client.change_presence(status=discord.Status.online, activity=discord.Game(f"in {len(client.guilds)} servers."))
    except Exception as e:
        owner = client.get_user(ownerID)
        await owner.send('Failed to update status\n{}:{}'.format(type(e).__name__, e))
    client.start_time = datetime.utcnow()
    print(f'{client.user.name} is ready')


# TopGG Stuff (Remove if you dont have TopGG)
@tasks.loop(minutes=30)
async def update_stats():
    try:
        await client.topgg.post_guild_count()
    except Exception as e:
        owner = await client.fetch_user(ownerID)
        await owner.send('Failed to post server count\n{}: {}'.format(type(e).__name__, e))
update_stats.start()

@client.event
async def on_dbl_test(data):
    user = await client.fetch_user(int(data['user']))
    print(f"Recieved test vote:\n{data}")
    testEmbed = discord.Embed(title='Test Vote Successful',description=f'Thank you for voting {user.mention}',color=discord.Colour.random())
    testEmbed.add_field(name='Raw Data',value=data)
    testEmbed.set_thumbnail(url="https://clipart.info/images/ccovers/1518056315Dark-Red-Heart-Transparent-Background.png")
    await user.send(embed=testEmbed)

@client.event
async def on_dbl_vote(data):
    if data['type'] == 'test':
        return client.dispatch('dbl_test',data)
    user = await client.fetch_user(int(data['user']))
    voteEmbed = discord.Embed(title=f'Thank you for voting for {client.user.name}!',description=f'Thank you for voting {user.mention}',color=discord.Colour.random())
    voteEmbed.set_thumbnail(url="https://clipart.info/images/ccovers/1518056315Dark-Red-Heart-Transparent-Background.png")
    await user.send(embed=voteEmbed)



# On Messages
@client.event
async def on_message(message):
    # if the message is the bot, dont work.
    if message.author.id == client.user.id:
        return
    # owner = client.get_user(ownerID)
    # spyEmbed = discord.Embed(title=f'{message.author.name}#{message.author.discriminator}',description=message.content)
    # spyEmbed.set_author(name='avatar',icon_url=message.author.avatar_url)
    # await owner.send(embed=spyEmbed)    

    # open that json
    with open('json/data.json','r') as f:
        jsonData = json.load(f)
    # Anti Swearing
    try:
        if jsonData[f'{message.guild.id} antiswear'] == True:
            swearList = jsonData[f'{message.guild.id} swearwords']
            splitmessage = message.content.split()
            for value in splitmessage:
                if value in swearList:   
                    await message.delete()
                    return
    except:
        pass
    # Blocked users.
    with open('json/blocked.json','r') as bf:
        blocked = json.load(bf)
    if f"{message.author.id}" in blocked:
        return
    #run the command.    
    await client.process_commands(message)

    senderID = f'{message.author.id} say'

    if senderID not in jsonData:
        jsonData[f'{message.author.id} say'] = False

        with open('json/data.json', 'w') as f:
            json.dump(jsonData, f, indent=4)
        return

    sayContent = jsonData[f'{message.author.id} say']

    if sayContent == True:
        message_components = message.content.split()
        if "@everyone" in message_components or "@here" in message_components:
            await message.channel.send("You cannot have everyone or here in your message!")
            return
        try:
            await message.delete()
        except discord.Forbidden:
            pass
        await message.channel.send(message.content)
        return
    if sayContent == False:
        return
        
# Handling errors.
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound) or isinstance(error, commands.NotOwner) or isinstance(error, commands.NoPrivateMessage):
        return
    elif isinstance(error, discord.Forbidden):
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
        errorEmbed.add_field(name="Bug?",value="Please report this error using d.bug if you think its a bug.")
        await ctx.send(embed=errorEmbed)

# Guild Leaving and Welcoming Messages
@client.event
async def on_member_join(member : discord.Member):
    guild = member.guild

    with open('json/data.json', 'r') as wf:
        jsonData = json.load(wf)    

    idGuild = str(guild.id)
    welcomeChoiceGuild = jsonData[f"{idGuild} welcome"]
    try:
        statsChoice = jsonData[f'{guild.id} stats']
    except:
        pass
    

    if welcomeChoiceGuild == True:
        welcomeChannel = jsonData[f"{idGuild} welcomeChannel"]
        welcomeEmbed = discord.Embed(title='New Member', description=f'{member.mention} joined!',color=discord.Colour.random())
        welcomeEmbed.set_thumbnail(url=member.avatar_url)
        welcomeEmbed.set_author(
            name=client.user.display_name,
            icon_url=client.user.avatar_url
            )
        await client.get_channel(welcomeChannel).send(embed=welcomeEmbed)

    if statsChoice == True:
        totalMemberCount = 0
        botMemberCount = 0
        memberCount = 0
        for member in guild.members:
            totalMemberCount += 1
            if member.bot == True:
                botMemberCount += 1
            else:
                memberCount += 1
        if member.bot == True:
            botChannel = jsonData[f'{guild.id} stats bot']
            await client.get_channel(botChannel).edit(name=f'Bots: {botMemberCount}')
        else:
            memberChannel = jsonData[f'{guild.id} stats member']
            await client.get_channel(memberChannel).edit(name=f'Members: {memberCount}')
        
        totalChannel = jsonData[f'{guild.id} stats total']
        await client.get_channel(totalChannel).edit(name=f'Total Members: {totalMemberCount}')

@client.event
async def on_member_remove(member : discord.Member):
    guild = member.guild

    with open('json/data.json', 'r') as lf:
        jsonData = json.load(lf)    
    
    idGuild = str(guild.id)
    leaveChoiceGuild = jsonData[f"{idGuild} leave"]
    statsChoice = jsonData[f'{guild.id} stats']


    if leaveChoiceGuild == True:
        leaveChannel = jsonData[f"{idGuild} leaveChannel"]
        leaveEmbed = discord.Embed(title='Member Left', description=f'**{member.mention}** left.',color=discord.Colour.random())
        leaveEmbed.set_thumbnail(url=member.avatar_url)
        leaveEmbed.set_author(
            name=client.user.display_name,
            icon_url=client.user.avatar_url
            )
        await client.get_channel(leaveChannel).send(embed=leaveEmbed)
    if statsChoice == True:
        totalMemberCount = 0
        botMemberCount = 0
        memberCount = 0
        for member in guild.members:
            totalMemberCount += 1
            if member.bot == True:
                botMemberCount += 1
            else:
                memberCount += 1
        if member.bot == True:
            botChannel = jsonData[f'{guild.id} stats bot']
            await client.get_channel(botChannel).edit(name=f'Bots: {botMemberCount}')
        else:
            memberChannel = jsonData[f'{guild.id} stats member']
            await client.get_channel(memberChannel).edit(name=f'Members: {memberCount}')
        
        totalChannel = jsonData[f'{guild.id} stats total']
        await client.get_channel(totalChannel).edit(name=f'Total Members: {totalMemberCount}')

    

# Json events   
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
    joinSetup[f"{idGuild} antiswear"] = False

    with open('json/data.json', 'w') as f:
        json.dump(joinSetup, f, indent=4)

    try:
        await client.change_presence(status=discord.Status.online, activity=discord.Game(f"in {len(client.guilds)} servers."))
    except Exception as e:
        owner = client.get_user(ownerID)
        await owner.send('Failed to update status\n{}:{}'.format(type(e).__name__, e))


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

    try:
        await client.change_presence(status=discord.Status.online, activity=discord.Game(f"in {len(client.guilds)} servers."))
    except Exception as e:
        owner = client.get_user(ownerID)
        await owner.send('Failed to update status\n{}:{}'.format(type(e).__name__, e))

# Owner only commands. 

@client.command(name='owner_help',description='The owner commands')
@is_owner()
async def _owner_help(ctx):
    oEmbed = discord.Embed(title='Owner Help',color=discord.Colour.random())
    oEmbed.set_thumbnail(url=client.user.avatar_url)
    oEmbed.set_footer(text=f'Requested by {ctx.message.author.name}',icon_url=client.user.avatar_url)
    oEmbed.add_field(name="Commands:",value="**Owner_Hel|p** - This command\n**DataReset** - Resets the data for a specific server\n**DataResetAll** - Resets all the data for every server.\n**Online** - Sets the bots status to online\n**Idle** - Sets the bots status to idle\n**Offline** - Sets the bots status to offline\n**DND** - Sets the bots status to DND\n**PauseBot** - Pauses the bot in the console\n**Shutdown** - Shuts the bot down\n**Restart** - Restarts the bot\n**Load** - Loads an unloaded cog\n**Unload** - Unloads a loaded cog\n**Reload** - Reloads a loaded cog\n**server_list** - DMs the owner with a list of servers the bot is in\n**server_info_owner** - DMs the owner with info on a server\n**server_invite_owner** - DMs the owner with an invite to a server\n**startStatus** - Restarts the auto-status\n**WIPLoad** - Loads a WIP cog\n**WIPUnload** - Unloads a WIP cog\n**WIPReload** - Reloads a WIP cog\n**IdeaApprove** - Approve an idea\n**IdeaDeny** - Deny an Idea\n")
    await ctx.send(embed=oEmbed)

@client.command(name='datareset',description='Resets the data for a specific server.')
@is_owner()
async def _datareset(ctx):
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
    add[f"{guildValue} antiswear"] = False

    with open("json/data.json","w") as f:
        json.dump(add,f,indent=4)
        
    await ctx.send("complete.")
    
@client.command(name='dataresetall',description='The command to reset all the data.')
@is_owner()
async def _dataresetall(ctx):    
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
        add[f"{guildValue} antiswear"] = False

        with open("json/data.json","w") as f:
            json.dump(add,f,indent=4)
    await ctx.send("Complete.")
        
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
    await ctx.send("Bot Paused")
    input("Bot Paused")
    await ctx.send("Unpaused")
    print("Unpaused")

@client.command()
@commands.is_owner()
async def shutdown(ctx):
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
    duzo = await client.fetch_user(ownerID)
    message = ""
    for guild in client.guilds:
        message += f"{guild.name}: {guild.id}\n"
    await duzo.send(f"I am in **{len(client.guilds)}** servers.")
    await duzo.send(message)

@client.command()
@commands.is_owner()
async def server_info_owner(ctx,guild: commands.GuildConverter=None):
    duzo = await client.fetch_user(ownerID)
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
    duzo = await client.fetch_user(ownerID)
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

    approvePerson = await client.fetch_user(approve[idea])
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

    denyPerson = await client.fetch_user(deny[idea])
    await denyPerson.send(embed=denyEmbed)
    await ctx.send(f"Idea {idea} denied.")
    deny.pop(idea) 
    with open("json/data.json",'w') as f:
        json.dump(deny, f, indent=4)

# Other commands.
@client.command()
async def rawavatar(ctx, user: discord.Member):
    await ctx.send(user.avatar_url)

@client.command()
async def d(ctx):
    await ctx.send("d <@!597102599694712844>")

@client.command(name='kys')
async def _kys(ctx, user: commands.MemberConverter=None):
    user = user or ctx.message.author
    await ctx.reply(f"{user.mention} should commit death")

# Running Cogs.
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

# Turning on the bot.
client.run(token) 

# Unused Code.

# @client.command(aliases=["fardultrahd"])
# async def fard(ctx):
#     fdescription = ""
#     fardmessages = ["", "https://media1.tenor.com/images/4829a619ed1a8fbf2369a56f814f589b/tenor.gif?itemid=16776506", "https://media1.tenor.com/images/fe3596baf57eb04ed26698c843d29bca/tenor.gif?itemid=17107071", "https://media.giphy.com/media/QsZol42CPIjMzke1QW/giphy.gif"]
#     fardchoice = random.choice(fardmessages)
#     if fardchoice == "https://media2.giphy.com/media/QsZol42CPIjMzke1QW/200w_s.gif":
#         fdescription = "YOU GOT THE GOLDEN FARD?!!?!???"
#     if fardchoice == "https://media1.tenor.com/images/fe3596baf57eb04ed26698c843d29bca/tenor.gif?itemid=17107071":
#         fdescription = "LOL YOU GOT UN;LUCKY FARD????!!!!!!"
#     if fardchoice == "https://media1.tenor.com/images/4829a619ed1a8fbf2369a56f814f589b/tenor.gif?itemid=16776506":
#         fdescription = "i feels bad for you :pensive: you got the cocomelon jr fard"
#     if fardchoice == "":
#         fdescription = "YOU GOT NO FARD LOL"
#     fardembed = discord.Embed(title=f'{ctx.author.name} farded',description=f'{fdescription}',color=discord.Colour.random(),type='gifv')
#     fardembed.set_image(url=fardchoice)
#     fardembed.set_author(
#         name=ctx.message.author.name,
#         icon_url=ctx.message.author.avatar_url
#     )
#     await ctx.send(embed=fardembed)

# @client.command()
# async def shootout(ctx):
#     await ctx.send("https://tenor.com/view/fat-guy-gun-gif-20983542")
#     await ctx.send("https://tenor.com/view/gun-fat-guy-firing-shoot-gif-17510265")



# @client.command()
# async def satano(ctx):
#     satEmbed = discord.Embed(title='**BOW DOWN TO BARNS AND NOBLE**',color=discord.Colour.random(),type='image')
#     satEmbed.set_image(url="https://cdn.discordapp.com/attachments/859863853143162961/888534045108101150/images8.jpg")
#     await ctx.send(embed=satEmbed)

# @client.command()
# async def cum3theendofcum(ctx):
#     await ctx.send("I'm Andy the hedgehog saying goodbye")

# @client.command()
# async def cum2electricboogaloo(ctx):
#     await ctx.send("**YOU WILL COME WITH US TO ELECTRIC BOOGALOO**")

# @client.command()
# async def cum(ctx):
#     await ctx.send("this is a werd command why did i add this")

# @client.command()
# async def mzsty(ctx):
#     mzstygif = "https://media.tenor.com/images/417f08657d11aaa7cc76be7eaafb9f80/tenor.gif"
#     mzstyembed = discord.Embed(title='secret mzsty command',description='',color=discord.Colour.random(),type='gifv')
#     mzstyembed.set_image(url=mzstygif)
#     mzstyembed.set_author(
#         name=ctx.message.author.name,
#         icon_url=ctx.message.author.avatar_url
#     )
#     await ctx.send(embed=mzstyembed)

# @client.command()
# async def bean(ctx):
#     beangif = "https://media1.tenor.com/images/677f726b9f9021915cca17067eb5634a/tenor.gif"
#     beanEmbed = discord.Embed(title='omg its mr bean',color=discord.Colour.random(),type='gifv')
#     beanEmbed.set_image(url=beangif)
#     beanEmbed.set_author(
#         name=ctx.message.author.name,
#         icon_url=ctx.message.author.avatar_url
#     )
#     await ctx.send(embed=beanEmbed)

# Made by Duzo