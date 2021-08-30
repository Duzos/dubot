import discord
from discord.ext import commands
import random
from random import Random, randint
import datetime
from datetime import datetime
from datetime import date
import json
import requests
from discord.embeds import EmptyEmbed
from discord.ext.commands.converter import PartialMessageConverter, clean_content


class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['cat','catrandom'],name='randomcat',description='Gives you a random cat picture.')
    async def randomcat(self, ctx):


        await ctx.message.delete()

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


        await ctx.message.delete()

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


        await ctx.message.delete()

        response_API = requests.get("https://api.adviceslip.com/advice")
        data = response_API.text
        parse_json = json.loads(data)
        currentAdvice = parse_json['slip']['advice']
        currentAdviceID = parse_json['slip']['id']

        adviceEmbed = discord.Embed(title='Advice',description=currentAdvice,color=discord.Colour.random())
        adviceEmbed.set_footer(text=f"ID: {currentAdviceID}",icon_url=EmptyEmbed)
        adviceEmbed.set_thumbnail(url=self.client.user.avatar_url)
        adviceEmbed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)

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
        message = message or "Please say something to use this command!"
        message_components = message.split()
        if "@everyone" in message_components or "@here" in message_components:
            await ctx.send("You cannot have everyone or here in your message!")
            return
        await ctx.message.delete()
        await ctx.send(message)

    @commands.command(aliases=['coinflip','coin_flip'],name='flip',description='Flips a coin.')
    async def flip(self, ctx):

        await ctx.message.delete()
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

        await ctx.message.delete()
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

        await ctx.message.delete()
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
        await ctx.message.delete()
        if number == correct_number:
            embedVar = discord.Embed(title=f'Your Number Is {number}', color=0x2ECC71)
            embedVar.add_field(name='You Picked The Correct Number! You Won', value=f"The correct number was {correct_number}.")
            await ctx.send(embed=embedVar)
        
        else:
            embedVar = discord.Embed(title=f'Your Number Is {number}', color=0xE74C3C)
            embedVar.add_field(name="Sorry, You Picked The Wrong Number", value=f"The correct number was {correct_number}.")
            await ctx.send(embed=embedVar)
    

    @commands.command(aliases=["gay"], name='howgay', description='Gives a value from 1-100 depending on how gay you are')
    async def howgay(self, ctx, user : commands.MemberConverter):
        await ctx.message.delete()
        randomgay = randint(0,100)

        gayembed = discord.Embed(title=f'How gay is {user.display_name}?', description=f'{user.mention} is **{randomgay}%** gay.',color=discord.Colour.random(),type='image')
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

    @commands.command(name='hug', description='Lets you hug a user you @')
    async def hug(self, ctx, user: commands.MemberConverter):
        await ctx.message.delete()
   
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
        await ctx.message.delete()

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

        await ctx.message.delete()
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
        await ctx.message.delete()
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
        
    @commands.command(name='yn',description='Gives you a yes or no answer.')
    async def yn(self, ctx, *, question):
        await ctx.message.delete()
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
        await ctx.message.delete()

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