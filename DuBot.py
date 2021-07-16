# le importing
import discord
import random
import os
from discord.ext import commands
from discord.utils import get
from discord import Member
#le intents
intents = discord.Intents.default()
intents.presences = True
intents.members = True
# le client stuff
client = commands.Bot(command_prefix = 'd.', intents=intents)
client.remove_command('help')
token = 'TOKENHERE'

#le on le ready
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("banana"))
    print(f'{client.user.name} is ready')


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
    await ctx.send("I am shutting down..")
    await client.change_presence(status=discord.Status.offline)
    await client.close()
    await ctx.send("Unable to shutdown.")


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
@client.command(aliases=["fardultrahd"])
async def fard(ctx):
    fdescription = ""
    fardmessages = ["", "https://media1.tenor.com/images/4829a619ed1a8fbf2369a56f814f589b/tenor.gif?itemid=16776506", "https://media1.tenor.com/images/fe3596baf57eb04ed26698c843d29bca/tenor.gif?itemid=17107071", "https://media.giphy.com/media/QsZol42CPIjMzke1QW/giphy.gif"]
    fardchoice = random.choice(fardmessages)
    color_list = [c for c in colors.values()]
    if fardchoice == "https://media2.giphy.com/media/QsZol42CPIjMzke1QW/200w_s.gif":
        fdescription = "YOU GOT THE GOLDEN FARD?!!?!???"
    if fardchoice == "https://media1.tenor.com/images/fe3596baf57eb04ed26698c843d29bca/tenor.gif?itemid=17107071":
        fdescription = "LOL YOU GOT UN;LUCKY FARD????!!!!!!"
    if fardchoice == "https://media1.tenor.com/images/4829a619ed1a8fbf2369a56f814f589b/tenor.gif?itemid=16776506":
        fdescription = "i feels bad for you :pensive: you got the cocomelon jr fard"
    if fardchoice == "":
        fdescription = "YOU GOT NO FARD LOL"
    fardembed = discord.Embed(title=f'{ctx.author.name} farded',description=f'{fdescription}',color=random.choice(color_list),type='gifv')
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
async def status(ctx, user: discord.Member):
    color_list = [c for c in colors.values()]
    status = discord.Embed (
    color=random.choice(color_list)
    )
    
    stat = user.status


    status.add_field(name=f"Status for {user.display_name}", value=f"currently: {stat}")

    await ctx.send(embed=status)

@client.command()
async def mzsty(ctx):
    mzstygif = "https://media.tenor.com/images/417f08657d11aaa7cc76be7eaafb9f80/tenor.gif"
    color_list = [c for c in colors.values()]
    mzstyembed = discord.Embed(title='secret mzsty command',description='',color=random.choice(color_list),type='gifv')
    mzstyembed.set_image(url=mzstygif)
    mzstyembed.set_author(
        name=ctx.message.author.name,
        icon_url=ctx.message.author.avatar_url
    )
    await ctx.send(embed=mzstyembed)

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
