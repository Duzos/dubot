#importing
import discord
import random
from random import *
from discord.ext import commands
from discord.utils import get
from discord import Member


#le token
token = 'ODY1MTkwMDIwMTc5Mjk2MjY3.YPAY_w.sqazc0J3MavapwVtOPFGomtlmuA'

#le client
client = commands.Bot(command_prefix = 'd.')
#client.remove_command('help')

#le embed le colours
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


#on ready
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("banana"))
    print(f'{client.user.name} is ready')


#le comands
@client.command(name='dice',description='Rolls a dice from 1-6.')
async def dice(ctx):
    roll = randint(1,6)
    await ctx.send(f":game_die: The dice rolled a **{roll}**")
    print("Ran dice command and rolled a", roll)

@client.command(name='rps',description='Play Rock Paper Scissors against the bot.')
async def rps(ctx, message):
    answer = message.lower()
    choices = ["rock", "paper", "scissors"]
    computers_answer = choice(choices)
    if answer == "gun":
        await ctx.send(f"I pick **{computers_answer}**, wait is that a gun?")
        await ctx.send(f"You win.")
        return
    if answer not in choices:
        await ctx.send(f"'{answer}' is not a valid choice. Please use one of the following: rock, paper, scissors")
    else:
        if computers_answer == answer:
            await ctx.send(f"Tie, we both picked **{answer}**.")
        if computers_answer == "rock":
            if answer == "paper":
                await ctx.send(f"You win, I picked **{computers_answer}** :rock:") 
            if answer == "scissors":
                await ctx.send(f"I win, I picked **{computers_answer}** :rock:")
        if computers_answer == "paper":
            if answer == "rock":
                await ctx.send(f"I win, I picked **{computers_answer}** :newspaper: ")
            if answer == "scissors":
                await ctx.send(f"You win, I picked **{computers_answer}** :newspaper: ")
        if computers_answer == "scissors":
            if answer == "rock":
                await ctx.send(f"You win, I picked **{computers_answer}** :scissors: ")
            if answer == "paper":
                await ctx.send(f"I win, I picked **{computers_answer}** :scissors: ")


#@client.command(aliases=['ng','numberguess','numberg'],name='nguess',description='Guess the bots number from 1-10')
#async def nguess(ctx, message):
#    answer = message.lower
#    numbers = ['1','2','3','4','5','6','7','8','9','10']
#    lucky = choice(numbers)
#    if answer not in numbers:
#        await ctx.send(f"{answer} is not a valid number, please pick one from 1-10.")
#    else:
#        if lucky == answer:
#            await ctx.send(f"You win, my number was **{lucky}**.")
#        else:
#            await ctx.send(f"You lose, my number was **{lucky}**.")

@client.command(name='info', description='Tells you the language this bot was coded in')
async def info(self, ctx):
    title="Python"
    desc="by Duzo"
    color_list = [c for c in colors.values()]
    msg = await ctx.send("one seccc")
    embed=discord.Embed(
    title=title,
     desc=desc,
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

#run the bot
client.run(token)