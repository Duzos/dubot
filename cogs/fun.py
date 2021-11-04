import discord
from discord import activity
from discord.embeds import EmptyEmbed
from discord.ext import commands
import random
from random import Random, randint
import datetime
from datetime import datetime
from datetime import date
import json
import requests
from discord.ext.commands.converter import PartialMessageConverter, clean_content
from requests.api import request
from requests.sessions import TooManyRedirects
import praw

with open('config.json','r') as f:
    config = json.load(f)
redditID = config['redditID']
redditSecret = config['redditSecret']
redditAgent = config['redditAgent']
reddit = praw.Reddit(client_id=redditID,client_secret=redditSecret,user_agent=redditAgent)



class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='meme',description='Sends a random meme.')
    async def meme(self,ctx):

        memes_submissions = reddit.subreddit('memes').hot()
        post_to_pick = random.randint(1, 10)
        for i in range(0, post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)

        memeEmbed = discord.Embed(title='Meme',color=discord.Colour.random(),type='image')
        memeEmbed.set_image(url=submission.url)
        memeEmbed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=memeEmbed)

    @commands.command(aliases=['rname','randomn'],name='randomname',description='Gives you a random name.')
    async def randomname(self,ctx):

        r = requests.get('http://api.randomuser.me/?format=json&?nat=gb')
        results = json.loads(r.text)
        results = results['results'][0]
        name=results['name']
        picture=results['picture']
        dob=results['dob']

        nameTitle=name['title']
        firstName=name['first']
        lastName=name['last']
        nameThumbnail=picture['large']
        nameAge=dob['age']
        nameDate=dob['date'][0:][:10]

        nameEmbed = discord.Embed(title='Random Person',color=discord.Colour.random(),type='image')
        nameEmbed.set_image(url=nameThumbnail)
        nameEmbed.add_field(name='Name',value=f"{nameTitle} {firstName} {lastName}",inline=False)
        nameEmbed.add_field(name='Age',value=f'{nameAge}\n{nameDate}')
        nameEmbed.add_field(name='Gender',value=results['gender'])
        nameEmbed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=nameEmbed)

    @commands.command(name='fact',description='Gives you a random fact.')
    async def fact(self, ctx):
        responseAPI = requests.get("https://uselessfacts.jsph.pl/random.json?language=en").json()   
        factID = responseAPI["id"]
        factResponse = responseAPI["text"]
        factLink = responseAPI["permalink"]

        factEmbed = discord.Embed(title='Fact',description=f'{factResponse}',color=discord.Colour.random())
        factEmbed.set_footer(text=f"ID: {factID}")
        factEmbed.add_field(name='Link',value=f'[Click!]({factLink})')
        factEmbed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)        
        await ctx.send(embed=factEmbed)

    @commands.command(aliases=['cat','catrandom'],name='randomcat',description='Gives you a random cat picture.')
    async def randomcat(self, ctx):


        for i in requests.get("https://api.thecatapi.com/v1/images/search").json():
            catURL = i["url"]
            catID = i["id"]

        catEmbed = discord.Embed(title='Cat',color=discord.Colour.random(),type='image')
        catEmbed.set_image(url=catURL)
        catEmbed.set_footer(text=f'ID: {catID}',icon_url=EmptyEmbed)
        catEmbed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=catEmbed)

    @commands.command(aliases=['bored'],name='activity',description='Gives you something to do.')
    async def activity(self, ctx):


        response_API = requests.get("https://www.boredapi.com/api/activity/")
        data = response_API.text
        parse_json = json.loads(data)
        activityCurrent = parse_json['activity']
        activityType = parse_json['type']
        #activityLink = parse_json['link']
        activityKey = parse_json['key']
        activityPeople = parse_json['participants']

        activityEmbed = discord.Embed(title='Activity',color=discord.Colour.random())
        activityEmbed.add_field(name='Activity:',value=activityCurrent,inline=False)
        activityEmbed.add_field(name='Type:',value=activityType,inline=False)
        activityEmbed.add_field(name='Number of People:',value=activityPeople,inline=False)
        #activityEmbed.add_field(name="",value=activityLink,inline=True)
        activityEmbed.set_footer(text=f"ID: {activityKey}",icon_url=EmptyEmbed)
        activityEmbed.set_thumbnail(url=self.client.user.avatar_url)
        activityEmbed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=activityEmbed)   

    @commands.command(name='advice',description='Gives you a random piece of advice.')
    async def advice(self, ctx):


        response_API = requests.get("https://api.adviceslip.com/advice")
        data = response_API.text
        parse_json = json.loads(data)
        currentAdvice = parse_json['slip']['advice']
        currentAdviceID = parse_json['slip']['id']

        adviceEmbed = discord.Embed(title='Advice',description=currentAdvice,color=discord.Colour.random())
        adviceEmbed.set_footer(text=f"ID: {currentAdviceID}",icon_url=EmptyEmbed)
        adviceEmbed.set_thumbnail(url=self.client.user.avatar_url)
        adviceEmbed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=adviceEmbed)

    @commands.command(name='e',description='e')
    async def e(self, ctx,eAmount=None):
        eList = ""
        if eAmount != None:
            eAmount = int(eAmount)
        if eAmount == None:
            eAmount = random.randint(1,100)
        elif eAmount > 2000:
            eAmount = 2000
            await ctx.send("Limit is 2000.")

        #await ctx.send(eAmount)
        if ctx.message.author.id == 509436097835827210:
            eAmount = random.randint(100,2000)
        while 0 < eAmount:
            eList = eList + "e"
            eAmount = eAmount - 1
        await ctx.send(eList)
        #await ctx.send(eAmount)

    @commands.command(aliases=['sayt','tsay','saytoggle'],name='togglesay',description='A version of say that can be toggled.')
    async def togglesay(self, ctx):
        with open('json/data.json', 'r') as f:
            sayToggle = json.load(f)
        
        authorID = f'{ctx.message.author.id} say'

        if authorID not in sayToggle:
            with open('json/data.json', 'r') as nf:
                sNew = json.load(nf)

                sNew[f'{ctx.message.author.id} say'] = False

                with open('json/data.json', 'w') as nf:
                    json.dump(sNew, nf, indent=4)
        
        sayCurrent = sayToggle[authorID]

        if sayCurrent == True:
            with open('json/data.json', 'r') as ff:
                sFalse = json.load(ff)

            sFalse[authorID] = False

            with open('json/data.json', 'w') as ff:
                json.dump(sFalse, ff, indent=4)

            await ctx.send("Repeating is now off.")
            return

        if sayCurrent == False:
            with open('json/data.json', 'r') as tf:
                sTrue = json.load(tf)

            sTrue[authorID] = True

            with open('json/data.json', 'w') as tf:
                json.dump(sTrue, tf, indent=4)
            await ctx.send("Repeating is now on.")
            return



    @commands.command(aliases=['speak','saythis', 'copy', 'doasisayslave'], name='say', description='Makes the bot say what you want it to say')
    async def say(self, ctx, *, message=None):
        #with open('json/econ.json', 'r') as ef:
        #    econ = json.load(ef)
        #if econ[f"{ctx.message.author.id} say"] == False:
        #    await ctx.send("You do not own this command!")
        #    return
        message = message or "Please say something to use this command!"
        message_components = message.split()
        if "@everyone" in message_components or "@here" in message_components:
            await ctx.send("You cannot have `@everyone` or `@here` in your message!")
            return
        await ctx.send(message)

    @commands.command(name='reverse',description='Reverses a text.')
    async def reverse(self,ctx,*,message=None):
        if message == None:
            def check(ms):
                return ms.channel == ctx.message.channel and ms.author == ctx.message.author
            askMessage = await ctx.send("What's your messaage?")
            OtherMessage = await self.client.wait_for('message', check=check)
            message = OtherMessage.content
            await askMessage.delete()
            await OtherMessage.delete()

        reverseMessage = message[::-1]
        await ctx.send(reverseMessage)

    @commands.command(aliases=['coinflip','coin_flip'],name='flip',description='Flips a coin.')
    async def flip(self, ctx):
        coin = ['Heads', 'Tails']
        result = random.choice(coin)
        
        flipEmbed = discord.Embed(title=':coin:',description=f'The coin landed on **{result}**.',color=discord.Colour.random())
        flipEmbed.set_thumbnail(url=self.client.user.avatar_url)
        flipEmbed.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url
        )
        await ctx.send(embed=flipEmbed)

    @commands.command(aliases=["roll"],name='dice',description='Rolls a dice from 1-6.')
    async def dice(self, ctx):
        roll = randint(1,6)
        diceEmbed = discord.Embed(title=":game_die:",description=f'The dice rolled a **{roll}**.',color=discord.Colour.random())
        diceEmbed.set_thumbnail(url=self.client.user.avatar_url)
        diceEmbed.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url
        )
        await ctx.send(embed=diceEmbed)

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
            incorrectEmbed = discord.Embed(title="Invalid",description=f"'{answer}' is not valid. Please use one of the following: rock, paper, scissors.",color=discord.Colour.random())
            incorrectEmbed.set_thumbnail(url=self.client.user.avatar_url)
            incorrectEmbed.set_author(
                name=ctx.message.author.name,
                icon_url=ctx.message.author.avatar_url
            )
            await ctx.send(embed=incorrectEmbed)
        else:
            if computers_answer == answer:
                answerEmbed = discord.Embed(color=discord.Colour.random(),title="Tie",description=f"We both picked **{answer}**.")
                answerEmbed.set_thumbnail(url=self.client.user.avatar_url)
                answerEmbed.set_author(
                    name=ctx.message.author.name,
                    icon_url=ctx.message.author.avatar_url
                )
                await ctx.send(embed=answerEmbed)
            if computers_answer == "rock":
                if answer == "paper":
                    answerEmbed = discord.Embed(color=discord.Colour.random(),title="You win",description=f"I picked **{computers_answer}**. :rock:")
                    answerEmbed.set_thumbnail(url=self.client.user.avatar_url)
                    answerEmbed.set_author(
                        name=ctx.message.author.name,
                        icon_url=ctx.message.author.avatar_url
                    )
                    await ctx.send(embed=answerEmbed) 
                if answer == "scissors":
                    answerEmbed = discord.Embed(color=discord.Colour.random(),title="I win",description=f"I picked **{computers_answer}**. :rock:")
                    answerEmbed.set_thumbnail(url=self.client.user.avatar_url)
                    answerEmbed.set_author(
                        name=ctx.message.author.name,
                        icon_url=ctx.message.author.avatar_url
                    )
                    await ctx.send(embed=answerEmbed) 
            if computers_answer == "paper":
                if answer == "rock":
                    answerEmbed = discord.Embed(color=discord.Colour.random(),title="I win",description=f"I picked **{computers_answer}**. :newspaper:")
                    answerEmbed.set_thumbnail(url=self.client.user.avatar_url)
                    answerEmbed.set_author(
                        name=ctx.message.author.name,
                        icon_url=ctx.message.author.avatar_url
                    )
                    await ctx.send(embed=answerEmbed) 
                if answer == "scissors":
                    answerEmbed = discord.Embed(color=discord.Colour.random(),title="You win",description=f"I picked **{computers_answer}**. :newspaper:")
                    answerEmbed.set_thumbnail(url=self.client.user.avatar_url)
                    answerEmbed.set_author(
                        name=ctx.message.author.name,
                        icon_url=ctx.message.author.avatar_url
                    )
                    await ctx.send(embed=answerEmbed) 
            if computers_answer == "scissors":
                if answer == "rock":
                    answerEmbed = discord.Embed(color=discord.Colour.random(),title="You win",description=f"I picked **{computers_answer}**. :scissors:")
                    answerEmbed.set_thumbnail(url=self.client.user.avatar_url)
                    answerEmbed.set_author(
                        name=ctx.message.author.name,
                        icon_url=ctx.message.author.avatar_url
                    )
                    await ctx.send(embed=answerEmbed) 
                if answer == "paper":
                    answerEmbed = discord.Embed(color=discord.Colour.random(),title="I win",description=f"I picked **{computers_answer}**. :scissors:")
                    answerEmbed.set_thumbnail(url=self.client.user.avatar_url)
                    answerEmbed.set_author(
                        name=ctx.message.author.name,
                        icon_url=ctx.message.author.avatar_url
                    )
                    await ctx.send(embed=answerEmbed) 

    @commands.command(aliases=['ng','numberg','numberguess'], name='nguess', description='Guess the bots number.')
    async def nguess(self,ctx, *, number=0):
        number_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        correct_number = random.choice(number_list)
        if number == correct_number:
            embedVar = discord.Embed(title=f'Your Number Is {number}', color=0x2ECC71)
            embedVar.add_field(name='You Picked The Correct Number! You Won', value=f"The correct number was {correct_number}.")
            await ctx.send(embed=embedVar)
        
        else:
            embedVar = discord.Embed(title=f'Your Number Is {number}', color=0xE74C3C)
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


#    @commands.command(name='datetime', description='Gives the date and time (in the UK)')
#    async def datetime(self, ctx):
#        now = datetime.now()
#        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
#        await ctx.send(f"It is {dt_string} right now in the UK.")

#    @commands.command(name='time', description='Gives the current time (in the UK)')
#    async def time(self, ctx):
#        now = datetime.now()
#        dt_string = now.strftime("%H:%M:%S")
#        await ctx.send(f"The time in the UK is {dt_string}.")

#    @commands.command(name='date', description='Gives the date (in the UK)')
#    async def date(self, ctx):
#        today = date.today()
#        datenow = today.strftime("%B %d, %Y")
#        await ctx.send(f"The date in the UK is {datenow}.") 

    @commands.command(aliases=["gay"], name='howgay', description='Gives a value from 1-100 depending on how gay you are')
    async def howgay(self, ctx, user : commands.MemberConverter=None):
        if user == None:
            user = ctx.message.author
        randomgay = randint(0,100)
        if user.id == 709763530232168560:
            randomgay = 100
        if user.id == 327807253052653569 or user.id == 578844127878184961:
            randomgay = 0
        gayembed = discord.Embed(title=f'How gay is {user.display_name}?', description=f'{user.mention} is **{randomgay}%** gay.',color=discord.Colour.random(),type='image')
        gayembed.set_image(url='https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Gay_Pride_Flag.svg/383px-Gay_Pride_Flag.svg.png')
        gayembed.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url
        )
        await ctx.send(embed=gayembed)




    #@commands.command(name='ping', description='Gets the bots ping')
    #async def ping(self, ctx):
    #    await ctx.send('Why do you want this from me. Please leave me alone.')

    @commands.command(name='hug', description='Lets you hug a user you @')
    async def hug(self, ctx, user: commands.MemberConverter):   
        huglist = ['https://media1.tenor.com/images/cef4ae44dfe06872eb0661dddf26f207/tenor.gif?itemid=13829297']
        huggif = random.choice(huglist)
        hugembed = discord.Embed(description=f'{ctx.author.mention} hugs {user.mention}',color=discord.Colour.random())
        hugembed.set_image(url=huggif)
        hugembed.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url
        )
        await ctx.send(embed=hugembed)
    @commands.command(name='kiss', description='Lets you kiss a user you @')
    async def kiss(self, ctx, user: commands.MemberConverter):
        kisslist = ['https://media1.tenor.com/images/ef9687b36e36605b375b4e9b0cde51db/tenor.gif?itemid=12498627','https://media1.tenor.com/images/e673b68b323f14ee902cfdb2da5ca65e/tenor.gif?itemid=16000723','https://media1.tenor.com/images/293d18ad6ab994d9b9d18aed8a010f73/tenor.gif?itemid=13001030','https://media1.tenor.com/images/015c71df440861e567364cf44e5d00fe/tenor.gif?itemid=16851922','https://media1.tenor.com/images/eb7502a33cbeca31c2e97af07d1c4285/tenor.gif?itemid=14270726','https://media1.tenor.com/images/45e529c116a1758fd09bdb27e2172eca/tenor.gif?itemid=11674749']
        kissgif = random.choice(kisslist)
        kissembed = discord.Embed(description=f'{ctx.author.mention} kisses {user.mention}',color=discord.Colour.random(),type='gifv')
        kissembed.set_image(url=kissgif)
        kissembed.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url
        )
        await ctx.send(embed=kissembed)
    @commands.command(name='slap', description='Lets you slap a user you @')
    async def slap(self, ctx, user: commands.MemberConverter):
        slaplist = ['https://media1.tenor.com/images/49de17c6f21172b3abfaf5972fddf6d6/tenor.gif?itemid=10206784','https://media1.tenor.com/images/42621cf33b44ca6a717d448b1223bccc/tenor.gif?itemid=15696850','https://media1.tenor.com/images/73adef04dadf613cb96ed3b2c8a192b4/tenor.gif?itemid=9631495','https://media1.tenor.com/images/e29671457384a94a7e19fea26029b937/tenor.gif?itemid=10048943','https://media.tenor.com/images/f26f807e70ee677f8e3aaee51779fc6f/tenor.gif','https://media1.tenor.com/images/b7a844cc66ca1c6a4f06c266646d070f/tenor.gif?itemid=17423278']
        slapgif = random.choice(slaplist)
        slapembed = discord.Embed(description=f'{ctx.author.mention} slaps {user.mention}',color=discord.Colour.random(),type='gifv')
        slapembed.set_image(url=slapgif)
        slapembed.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url
        )
        await ctx.send(embed=slapembed)
        #await ctx.send(f'{ctx.author.mention} slaps {user.mention} {slapgif}')

    @commands.command(
        name='embed',
        description='Creates your custom embed',
    )
    async def embed_command(self, ctx):
        # Define a check function that validates the message received by the bot
        def check(ms):
            # Look for the message sent in the same channel where the command was used
            # As well as by the user who used the command.
            return ms.channel == ctx.message.channel and ms.author == ctx.message.author

        # First ask the user for the title
        mesg = await ctx.send(content='What would you like the title to be?')

        # Wait for a response and get the title
        msg = await self.client.wait_for('message', check=check)
        title = msg.content # Set the title
        await msg.delete()
        await mesg.delete()

        # Next, ask for the content
        mesg = await ctx.send(content='What would you like the Description to be?')
        msg = await self.client.wait_for('message', check=check)
        desc = msg.content
        await msg.delete()
        await mesg.delete()

        # Finally make the embed and send it
        msg = await ctx.send(content='Now generating the embed...')

        # Convert the colors into a list
        # To be able to use random.choice on it

        embed = discord.Embed(
            title=title,
            description=desc,
            color=discord.Colour.random()
        )
        # Also set the thumbnail to be the bot's pfp
        embed.set_thumbnail(url=self.client.user.avatar_url)

        # Also set the embed author to the command user
        embed.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url
        )

        await msg.edit(
            embed=embed,
            content=None
        )
        # Editing the message
        # We have to specify the content to be 'None' here
        # Since we don't want it to stay to 'Now generating embed...'

        return

#    @commands.command(name='whyareyougay', description='The question we are all asking')
#    async def whyareyougay(self, ctx):
#        await ctx.send('im not gay you are')

#    @commands.command(name='fightclub', description='We dont talk about fight club')
#    async def fightclub(self, ctx):
#        await ctx.send("We dont talk about fight club here. No fight clubs in this server, Officer.")

    @commands.command(name='yn',description='Gives you a yes or no answer.')
    async def yn(self, ctx, *, question):
        responses=['Yes.','No.']
        answer = random.choice(responses)
        ynEmbed = discord.Embed(title=question,description=answer,color=discord.Colour.random())
        ynEmbed.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url
        )
        ynEmbed.set_thumbnail(url=self.client.user.avatar_url)
        await ctx.send(embed=ynEmbed)

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
        answer = random.choice(responses)
        ballembed = discord.Embed(title=question,description=answer,color=discord.Colour.random())
        ballembed.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url
        )
        ballembed.set_thumbnail(url=self.client.user.avatar_url)
        await ctx.send(embed=ballembed)




def setup(client):
    client.add_cog(Fun(client))