import discord
from discord.ext import commands
import random
from random import Random, randint
import datetime
from datetime import datetime
from datetime import date
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



class Fun(commands.Cog):
    @commands.command(aliases=['speak','saythis', 'copy', 'doasisayslave'], name='say', description='Makes the bot say what you want it to say')
    async def say(self, ctx, *, message):
        await ctx.message.delete()
        await ctx.send(message)

    @commands.command(name='dice',description='Rolls a dice from 1-6.')
    async def dice(self, ctx):
        roll = randint(1,6)
        await ctx.send(f":game_die: The dice rolled a **{roll}**")
        print("Ran dice command and rolled a", roll)

    @commands.command(name='rps',description='Play Rock Paper Scissors against the bot.')
    async def rps(self, ctx, message):
        answer = message.lower()
        choices = ["rock", "paper", "scissors"]
        computers_answer = random.choice(choices)
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


    @commands.command(aliases=['ng','numberg','numberguess'], name='nguess', description='Guess the bots number.')
    async def nguess(self,ctx, *, number=0):
        number_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        correct_number = random.choice(number_list)

        if number == correct_number:
            embedVar = discord.Embed(title=f'Your Number Is {number}', color=0xF1C40F)
            embedVar.add_field(name='You Picked The Correct Number! You Won', value=f"The correct number was {correct_number}.")
            await ctx.send(embed=embedVar)
        
        else:
            embedVar = discord.Embed(title=f'Your Number Is {number}', color=0xF1C40F)
            embedVar.add_field(name="Sorry, You Picked The Wrong Number", value=f"The correct number was {correct_number}.")
            await ctx.send(embed=embedVar)
    



#    @commands.command(name='dm', description='Sends a DM to the user you @')
#    async def dm(self, ctx, user: discord.Member):
#        await ctx.send(f"sliding into {user.mention}'s DMs")
#        responses = ['hows it goin bb', '*slides into your DMs* wassup baby girl', 'hey', 'uwu *pounces on you* rawr x3 owo? whats this? *notices your buldge*', 'you just got ***botted***  :sunglasses:', 'get DMed punk', 'Duzo is my God', '0portalboy0 is my God']
#        choice = random.choice(responses)
#        await user.send(f"{choice}")
#        await ctx.send(f'i DMed them and said "{choice}"')

    #@commands.command(aliases=['trick or treat', 'trickortreat', 'trick-or-treat', 'trick_or_treat'], name='Trick or Treat', description='A command that only works on Halloween')
    #async def tricktreat(self, ctx):
    #    responses = ['Trick! Muhahaha :ghost:', "Treat! Here's some candy  :candy:", "Treat! Here's some sweets  :candy:"]
    #    await ctx.send(f'{random.choice(responses)}')


    @commands.command(name='datetime', description='Gives the date and time (in the UK)')
    async def datetime(self, ctx):
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        await ctx.send(f"It is {dt_string} right now in the UK.")

    @commands.command(name='time', description='Gives the current time (in the UK)')
    async def time(self, ctx):
        now = datetime.now()
        dt_string = now.strftime("%H:%M:%S")
        await ctx.send(f"The time in the UK is {dt_string}.")

    @commands.command(name='date', description='Gives the date (in the UK)')
    async def date(self, ctx):
        today = date.today()
        datenow = today.strftime("%B %d, %Y")
        await ctx.send(f"The date in the UK is {datenow}.") 

    @commands.command(aliases=["gay"], name='howgay', description='Gives a value from 1-100 depending on how gay you are')
    async def howgay(self, ctx, user : discord.Member):
        
        randomgay = randint(0,100)
        color_list = [c for c in colors.values()]
        gayembed = discord.Embed(title=f'How gay is {user.display_name}?', description=f'{user.mention} is **{randomgay}%** gay.',color=random.choice(color_list),type='image')
        gayembed.set_image(url='https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Gay_Pride_Flag.svg/383px-Gay_Pride_Flag.svg.png')
        gayembed.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url
        )
        if user.name == "Duzo":
            await ctx.send("Duzo is straight.. so thats 0%")
            return
        if user.name == "monke":
            await ctx.send("monke is 100% not gay. he is monke. he does not know what an lgbtq+ is.")
            return
        await ctx.send(embed=gayembed)

    @commands.command(name='avatar', description='Gets you the avatar of someone.')
    async def avatar(self, ctx, user: discord.Member):
        avatar = user.avatar_url
        color_list = [c for c in colors.values()]
        avatarembed = discord.Embed(title=f'Avatar of {user.display_name}',color=random.choice(color_list),type='image')
        avatarembed.set_image(url=avatar)
        avatarembed.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url
        )
        await ctx.send(embed=avatarembed)
    @commands.command()
    async def rawavatar(self, ctx, user: discord.Member):
        await ctx.send(user.avatar_url)


    #@commands.command(name='ping', description='Gets the bots ping')
    #async def ping(self, ctx):
    #    await ctx.send('Why do you want this from me. Please leave me alone.')

    @commands.command(name='hug', description='Lets you hug a user you @')
    async def hug(self, ctx, user: discord.Member):
        color_list = [c for c in colors.values()]   
        huglist = ['https://media1.tenor.com/images/cef4ae44dfe06872eb0661dddf26f207/tenor.gif?itemid=13829297']
        huggif = random.choice(huglist)
        hugembed = discord.Embed(title=f'{ctx.author.name} hugs {user.name}', description='lol nice',color=random.choice(color_list))
        hugembed.set_image(url=huggif)
        hugembed.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url
        )
        await ctx.send(embed=hugembed)
    @commands.command(name='kiss', description='Lets you kiss a user you @')
    async def kiss(self, ctx, user: discord.Member):
        color_list = [c for c in colors.values()]
        kisslist = ['https://media1.tenor.com/images/ef9687b36e36605b375b4e9b0cde51db/tenor.gif?itemid=12498627','https://media1.tenor.com/images/e673b68b323f14ee902cfdb2da5ca65e/tenor.gif?itemid=16000723','https://media1.tenor.com/images/293d18ad6ab994d9b9d18aed8a010f73/tenor.gif?itemid=13001030','https://media1.tenor.com/images/015c71df440861e567364cf44e5d00fe/tenor.gif?itemid=16851922','https://media1.tenor.com/images/eb7502a33cbeca31c2e97af07d1c4285/tenor.gif?itemid=14270726','https://media1.tenor.com/images/45e529c116a1758fd09bdb27e2172eca/tenor.gif?itemid=11674749']
        kissgif = random.choice(kisslist)
        kissembed = discord.Embed(title=f'{ctx.author.name} kisses {user.name}', description='ew',color=random.choice(color_list),type='gifv')
        kissembed.set_image(url=kissgif)
        kissembed.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url
        )
        await ctx.send(embed=kissembed)
    @commands.command(name='slap', description='Lets you slap a user you @')
    async def slap(self, ctx, user: discord.Member):
        color_list = [c for c in colors.values()]
        slaplist = ['https://media1.tenor.com/images/49de17c6f21172b3abfaf5972fddf6d6/tenor.gif?itemid=10206784','https://media1.tenor.com/images/42621cf33b44ca6a717d448b1223bccc/tenor.gif?itemid=15696850','https://media1.tenor.com/images/73adef04dadf613cb96ed3b2c8a192b4/tenor.gif?itemid=9631495','https://media1.tenor.com/images/e29671457384a94a7e19fea26029b937/tenor.gif?itemid=10048943','https://media.tenor.com/images/f26f807e70ee677f8e3aaee51779fc6f/tenor.gif','https://media1.tenor.com/images/b7a844cc66ca1c6a4f06c266646d070f/tenor.gif?itemid=17423278']
        slapgif = random.choice(slaplist)
        slapembed = discord.Embed(title=f'{ctx.author.name} slaps {user.name}', description='haha get slapped',color=random.choice(color_list),type='gifv')
        slapembed.set_image(url=slapgif)
        slapembed.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url
        )
        await ctx.send(embed=slapembed)
        #await ctx.send(f'{ctx.author.mention} slaps {user.mention} {slapgif}')

    @commands.command(name='whyareyougay', description='The question we are all asking')
    async def whyareyougay(self, ctx):
        await ctx.send('im not gay you are')

    @commands.command(name='fightclub', description='We dont talk about fight club')
    async def fightclub(self, ctx):
        await ctx.send("We dont talk about fight club here. No fight clubs in this server, Officer.")

    @commands.command(aliases=['8ball', 'eightball'], name='ball', description='Gives you advice')
    async def _8ball (self, ctx, *, question):
        responses = [
        "It is certain",
        "It is decidedly so",
        "Without a doubt",
        "Yes, definitely",
        "You may rely on it",
        "As I see it, yes",
        "Most likely",
        "Outlook good",
        "Yes",
        "Signs point to yes",
        "Reply hazy try again",
        "Ask again later",
        "Better not tell you now",
        "Cannot predict now",
        "Concentrate and ask again",
        "Don't count on it",
        "My reply is no",
        "My sources say no",
        "Outlook not so good",
        "Very doubtful"]
        await ctx.send(f'Your Question: {question}\nThe Answer: {random.choice(responses)}')

def setup(client):
    client.add_cog(Fun(client))