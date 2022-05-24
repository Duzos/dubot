# Made by Duzo
# ================


# Importing
import json
import os
from datetime import datetime
import discord
from discord.ext import commands, tasks

# Getting the prefix for the server

def get_prefix(client, message):
    with open('json/data.json', 'r') as f:
        prefixes = json.load(f)

    try:
        guildID = str(message.guild.id)
    except:
        pass
    try:
        return prefixes[f"{guildID} prefix"]
    except:
        return ['d.','D.']

# The bots intents
intents = discord.Intents.default()
intents.presences = True
intents.members = True
intents.reactions = True

# Getting items from the config
with open('config.json','r') as cf:
    config = json.load(cf)

token = config['token']
prefix = config['prefix']
topToken = config['topToken']
ownerID = config['ownerID']

# Setting up the client.
client = commands.Bot(command_prefix = get_prefix, intents=intents, case_insensitive=True)
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

def embed_set_author(ctx, embed: discord.Embed):
    return embed.set_author(name=ctx.message.author.display_name,icon_url=ctx.message.author.display_avatar.url)


# On Messages


@client.event
async def on_message(message):
    # if the message is the bot, dont work.
    if message.author.id == client.user.id:
        return   

    # open that json
    with open('json/data.json','r') as f:
        jsonData = json.load(f)
    
    # n word stuff
    try:
        if jsonData[f'{message.guild.id} nword'] == True:
            splitMsg = message.content.lower().split()
            for value in splitMsg:
                if value in ['nigger','nigga','niggers','niggas']: # ok i know im white but please dont get mad about this, i kinda have to put it somewhere if i want this feature to work :/
                    count = jsonData[f'{message.author.id} nwordcount']
                    count += 1
                    jsonData[f'{message.author.id} nwordcount'] = count
                    await message.reply(f'You have now said the n word {count} times.')
                    with open('json/data.json', 'w') as f:
                        json.dump(jsonData, f, indent=4)
    except:
        pass
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

    # seeing if the message author has the nword stuff setup for them already
    if f'{message.author.id} nwordcount' not in jsonData:
        jsonData[f'{message.author.id} nwordcount'] = 0
        with open('json/data.json', 'w') as f:
            json.dump(jsonData, f, indent=4)

    # say toggle stuff
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
            name=ctx.message.author.display_name,
            icon_url=ctx.message.author.display_avatar.url
        )
        botPermEmbed.set_thumbnail(url=client.user.display_avatar.url)
        await ctx.send(embed=botPermEmbed)
        return
    elif isinstance(error, commands.MissingPermissions):
        botPermEmbed = discord.Embed(title='ERROR',description='You are missing the required permission(s).',color=0x992D22)
        permValues = ''
        for perm in error.missing_perms:
            permValues = permValues+ f"{perm}\n"
        botPermEmbed.add_field(name="Missing Permission(s):",value=permValues,inline=False)
        botPermEmbed.set_author(
            name=ctx.message.author.display_name,
            icon_url=ctx.message.author.display_avatar.url
        )
        botPermEmbed.set_thumbnail(url=client.user.display_avatar.url)
        await ctx.send(embed=botPermEmbed)
        return
    else:
        errorEmbed = discord.Embed(title='ERROR',description=error,color=0x992D22)
        errorEmbed.set_author(
            name=ctx.message.author.display_name,
            icon_url=ctx.message.author.display_avatar.url
        )
        errorEmbed.set_thumbnail(url=client.user.display_avatar.url)
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
        try:
            welcomeMessageChoice = jsonData[f"{idGuild} welcomeMessageChoice"]
        except:
            pass
        welcomeChannel = jsonData[f"{idGuild} welcomeChannel"]
        welcomeEmbed = discord.Embed(title='New Member', description=f'{member.mention} joined!',color=discord.Colour.random())
        welcomeEmbed.set_thumbnail(url=member.display_avatar.url)
        welcomeEmbed.set_author(
            name=client.user.display_name,
            icon_url=client.user.display_avatar.url
            )
        try:
            await client.get_channel(welcomeChannel).send(embed=welcomeEmbed)
        except:
            pass
        
        try:
            if welcomeMessageChoice == True:
                welcomeMessage = jsonData[f"{idGuild} welcomeMessage"]
                await member.send(welcomeMessage)
        except:
            pass

    try:
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
    except:
        pass

@client.event
async def on_member_remove(member : discord.Member):
    guild = member.guild

    with open('json/data.json', 'r') as lf:
        jsonData = json.load(lf)    
    
    idGuild = str(guild.id)
    leaveChoiceGuild = jsonData[f"{idGuild} leave"]
    try:
        statsChoice = jsonData[f'{guild.id} stats']
    except:
        pass


    if leaveChoiceGuild == True:
        leaveChannel = jsonData[f"{idGuild} leaveChannel"]
        leaveEmbed = discord.Embed(title='Member Left', description=f'**{member.mention}** left.',color=discord.Colour.random())
        leaveEmbed.set_thumbnail(url=member.display_avatar.url)
        leaveEmbed.set_author(
            name=client.user.display_name,
            icon_url=client.user.display_avatar.url
            )
        await client.get_channel(leaveChannel).send(embed=leaveEmbed)
    try:
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
    except:
        pass
    

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
# these are gone now, look in the owner cog.


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
#         name=ctx.message.author.display_name,
#         icon_url=ctx.message.author.display_avatar.url
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
#         name=ctx.message.author.display_name,
#         icon_url=ctx.message.author.display_avatar.url
#     )
#     await ctx.send(embed=mzstyembed)

# @client.command()
# async def bean(ctx):
#     beangif = "https://media1.tenor.com/images/677f726b9f9021915cca17067eb5634a/tenor.gif"
#     beanEmbed = discord.Embed(title='omg its mr bean',color=discord.Colour.random(),type='gifv')
#     beanEmbed.set_image(url=beangif)
#     beanEmbed.set_author(
#         name=ctx.message.author.display_name,
#         icon_url=ctx.message.author.display_avatar.url
#     )
#     await ctx.send(embed=beanEmbed)

# Made by Duzo
