from urllib import request
import discord
from discord.embeds import EmptyEmbed
from discord.ext import commands
import random
from random import randint
import json
import requests
import praw
import asyncio

with open('config.json','r') as f:
    config = json.load(f)
ttsToken = config['ttsToken']
redditID = config['redditID']
redditSecret = config['redditSecret']
redditAgent = config['redditAgent']
reddit = praw.Reddit(client_id=redditID,client_secret=redditSecret,user_agent=redditAgent,check_for_async=False)

def embed_set_author(ctx, embed: discord.Embed):
    return embed.set_author(name=ctx.message.author.display_name,icon_url=ctx.message.author.display_avatar.url)
    
class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='tts',description='Text to speech!')
    async def _tts(self, ctx,*,args: str):
        args = "%20".join( args.split() )
        url = f'https://api.voicerss.org/?key={ttsToken}&hl=en-us&c=MP3&f=16khz_16bit_stereo&src={args}'
        request.urlretrieve(url,'tts.mp3')
        await ctx.reply(file = discord.File('./tts.mp3'))

    @commands.command(name='insult',description='Produces an insult for you')
    async def _insult(self, ctx):
        await ctx.trigger_typing()
        url = 'https://insult.mattbas.org/api/insult.json'
        responseApi = requests.get(url).json()
        insult = responseApi['insult']

        embed = discord.Embed(title='Insult',description=insult,color=0xED1C06)
        embed.set_footer(text=f'API: {url}')
        embed_set_author(ctx, embed)
        embed.set_thumbnail(url=self.client.user.display_avatar.url)
        await ctx.reply(embed=embed)


    @commands.command(name='truth',description='Pick a truth')
    async def _truth(self, ctx):
        await ctx.trigger_typing()
        url = 'https://api.truthordarebot.xyz/v1/truth'
        choice = requests.get(url).json()

        choiceType = choice['type']
        choiceID = choice['id']
        choiceRating = choice['rating']
        choiceQuestion = choice['question']

        embed = discord.Embed(title=choiceType,description=choiceQuestion,color=discord.Colour.random())
        embed_set_author(ctx, embed)
        embed.set_thumbnail(url=self.client.user.display_avatar.url)
        embed.set_footer(text=f'ID: {choiceID} | Rating: {choiceRating}')
        await ctx.reply(embed=embed)

    @commands.command(name='dare',description='Pick a dare')
    async def _dare(self, ctx):
        await ctx.trigger_typing()
        url = 'https://api.truthordarebot.xyz/v1/dare'
        choice = requests.get(url).json()

        choiceType = choice['type']
        choiceID = choice['id']
        choiceRating = choice['rating']
        choiceQuestion = choice['question']

        embed = discord.Embed(title=choiceType,description=choiceQuestion,color=discord.Colour.random())
        embed_set_author(ctx, embed)
        embed.set_thumbnail(url=self.client.user.display_avatar.url)
        embed.set_footer(text=f'ID: {choiceID} | Rating: {choiceRating}')
        await ctx.reply(embed=embed)


    @commands.command(aliases=['tod'],name='truthordare',description='Play truth or dare')
    async def _tod(self, ctx):
        await ctx.trigger_typing()
        urls = ['https://api.truthordarebot.xyz/v1/dare','https://api.truthordarebot.xyz/v1/truth']
        url = random.choice(url)
        choice = requests.get(url).json()

        choiceType = choice['type']
        choiceID = choice['id']
        choiceRating = choice['rating']
        choiceQuestion = choice['question']

        embed = discord.Embed(title=choiceType,description=choiceQuestion,color=discord.Colour.random())
        embed_set_author(ctx, embed)
        embed.set_thumbnail(url=self.client.user.display_avatar.url)
        embed.set_footer(text=f'ID: {choiceID} | Rating: {choiceRating}')
        await ctx.reply(embed=embed)

    @commands.command(aliases=['wyr'],name='wouldyourather',description='Play would you rather!')
    async def _wyr(self, ctx):
        await ctx.trigger_typing()
        url = 'https://api.truthordarebot.xyz/v1/wyr'
        choice = requests.get(url).json()

        choiceType = choice['type']
        choiceID = choice['id']
        choiceRating = choice['rating']
        choiceQuestion = choice['question']

        embed = discord.Embed(title=choiceType,description=choiceQuestion,color=discord.Colour.random())
        embed_set_author(ctx, embed)
        embed.set_thumbnail(url=self.client.user.display_avatar.url)
        embed.set_footer(text=f'ID: {choiceID} | Rating: {choiceRating}')
        await ctx.reply(embed=embed)

    @commands.command(aliases=['nhie'],name='neverhaveiever',description='Play never have i ever!')
    async def _nhie(self, ctx):
        await ctx.trigger_typing()
        url = 'https://api.truthordarebot.xyz/v1/nhie'
        choice = requests.get(url).json()

        choiceType = choice['type']
        choiceID = choice['id']
        choiceRating = choice['rating']
        choiceQuestion = choice['question']

        embed = discord.Embed(title=choiceType,description=choiceQuestion,color=discord.Colour.random())
        embed_set_author(ctx, embed)
        embed.set_thumbnail(url=self.client.user.display_avatar.url)
        embed.set_footer(text=f'ID: {choiceID} | Rating: {choiceRating}')
        await ctx.reply(embed=embed)

    @commands.command(name='paranoia',description='Get a random paranoia question!')
    async def _paranoia(self, ctx):
        await ctx.trigger_typing()
        url = 'https://api.truthordarebot.xyz/v1/paranoia'
        choice = requests.get(url).json()

        choiceType = choice['type']
        choiceID = choice['id']
        choiceRating = choice['rating']
        choiceQuestion = choice['question']

        embed = discord.Embed(title=choiceType,description=choiceQuestion,color=discord.Colour.random())
        embed_set_author(ctx, embed)
        embed.set_thumbnail(url=self.client.user.display_avatar.url)
        embed.set_footer(text=f'ID: {choiceID} | Rating: {choiceRating}')
        await ctx.reply(embed=embed)

    @commands.command(name='ben-call',description='Call Talking Ben.')
    async def _ben_call(self, ctx):
        def check(ms):
            return ms.channel == ctx.message.channel and ms.author == ctx.message.author
        msg1 = await ctx.reply('Do you want this to be spammy or not (yes or no, providing anything else defaults to no.)')
        msg = await self.client.wait_for('message',check=check)
        spam_choice = msg.content.lower()
        await msg1.delete()
        await msg.delete()
        msg = await ctx.reply('You rang Ben.',file=discord.File('./ben-ring.mp4'))
        valid_words = ["yes","no","laugh","tongue"]
        responses = {
            "no": "./ben-no.mp4",
            "yes": "./ben-yes.mp4",
            "laugh": "./ben-laugh.mp4",
            "tongue": "./ben-tongue.mp4"
        }
        ben_talking = True
        if spam_choice == "yes":
            while ben_talking == True:
                await msg.reply("Ask Talking Ben a question within 8 seconds or he will hang up.")
                try:
                    msg = await self.client.wait_for('message',check=check,timeout=8)
                except asyncio.TimeoutError:
                    await ctx.reply('Ben hung up',file=discord.File('./ben-hang-up.mp4'))
                    ben_talking = False
                    return
                bens_choice = random.choice(valid_words)
                await ctx.reply(content=f"Your question: {msg.content}\nBen's Response:",file=discord.File(responses[bens_choice]))            
        else:
            while ben_talking == True:
                askMsg = await ctx.reply("Ask Talking Ben a question within 8 seconds or he will hang up.")
                try:
                    userQuestion = await self.client.wait_for('message',check=check,timeout=8)
                except asyncio.TimeoutError:
                    await ctx.reply('Ben hung up',file=discord.File('./ben-hang-up.mp4'))
                    ben_talking = False
                    return
                bens_choice = random.choice(valid_words)
                await msg.delete()
                msg = await ctx.reply(content=f"Your question: {userQuestion.content}\nBen's Response:",file=discord.File(responses[bens_choice]))  
                await userQuestion.delete()
                await askMsg.delete() 

    @commands.command(name='ben',description='Ask Talking Ben a question.')
    async def _ben(self, ctx,*,question=None):
        if question == None:
            return await ctx.reply("please give ben a question.")
        valid_words = ["yes","no","laugh","tongue"]
        responses = {
            "no": "./ben-no.mp4",
            "yes": "./ben-yes.mp4",
            "laugh": "./ben-laugh.mp4",
            "tongue": "./ben-tongue.mp4"
        }
        bens_choice = random.choice(valid_words)
        await ctx.reply(content=f"Your question: {question}\nBen's Response:",file=discord.File(responses[bens_choice]))

    @commands.command(name='spaceweights',description='Get your weight on other planets.')
    async def _spaceweights(self, ctx, weight, planet):
        planet = planet.lower()
        weight = int(weight)
        if planet == None or weight == None:
            return ctx.reply("Please provide a weight in kg and a planet.")
                
        planets = {
        "sun": 27.01,
        "mercury": 0.38,
        "venus": 0.91,
        "moon": 0.166,
        "mars": 0.38,
        "jupiter": 2.34,
        "saturn": 1.06,
        "uranus": 0.92,
        "neptune": 1.19,
        "pluto": 0.06,
        "earth": 1,
        "io": 0.183,
        "europa": 0.133,
        "ganymede": 0.144,
        "callisto": 0.126
        }


        if planet not in planets:
            planetList = ""
            for val in planets:
                planetList = planetList + val + "\n"
            return await ctx.reply(f"Please provide a valid planet:\n{planetList}")

        multiple = planets[planet]
        embed = discord.Embed(title='Space Weights', description=f"Your weight on {planet} is {weight * multiple}kg.",color=discord.Colour.random())
        embed_set_author(ctx, embed)
        embed.set_thumbnail(url=self.client.user.display_avatar.url)
        await ctx.reply(embed=embed)

    @commands.command(name='meme',description='Sends a random meme.')
    async def meme(self,ctx):
        await ctx.trigger_typing()
        memes_submissions = reddit.subreddit('memes').hot()
        post_to_pick = random.randint(1, 20)
        for i in range(0, post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)

        memeEmbed = discord.Embed(title='Meme',color=discord.Colour.random(),type='image')
        memeEmbed.set_image(url=submission.url)
        memeEmbed.set_author(name=ctx.message.author.display_name,icon_url=ctx.message.author.display_avatar.url)
        await ctx.reply(embed=memeEmbed)

    @commands.command(name='subreddit',description='Get posts from a subreddit.')
    async def _subreddit(self, ctx, sbreddit):
        await ctx.trigger_typing()
        sb_submissions = reddit.subreddit(sbreddit).hot()
        post_to_pick = random.randint(1,20)
        for i in range(0,post_to_pick):
            submission = next(x for x in sb_submissions if not x.stickied)


        sb_extension = submission.url[len(submission.url) - 3 :].lower()
        if sb_extension == "jpg" or sb_extension == "png" or sb_extension == "gif":
            sbEmbed = discord.Embed(title=sbreddit,description=f'[{submission.title}]({submission.url})',color=discord.Colour.random(),type='image')
            sbEmbed.set_image(url=submission.url)
            sbEmbed.set_author(name=ctx.message.author.display_name,icon_url=ctx.message.author.display_avatar.url)
            await ctx.reply(embed=sbEmbed)
            return
        sbEmbed = discord.Embed(title=sbreddit,description=f'[{submission.title}]({submission.url})',color=discord.Colour.random())
        sbEmbed.set_author(name=ctx.message.author.display_name,icon_url=ctx.message.author.display_avatar.url)
        await ctx.reply(embed=sbEmbed)
        

    @commands.command(name='randomreddit',description='Get posts from a random subreddit.')
    async def _randomreddit(self, ctx):
        await ctx.trigger_typing()
        sb_random = reddit.random_subreddit()
        sb_submissions=sb_random.hot()
        post_to_pick = random.randint(1,20)
        for i in range(0,post_to_pick):
            submission = next(x for x in sb_submissions if not x.stickied)


        sb_extension = submission.url[len(submission.url) - 3 :].lower()
        if sb_extension == "jpg" or sb_extension == "png" or sb_extension == "gif":
            sbEmbed = discord.Embed(title=sb_random.display_name,description=f'[{submission.title}]({submission.url})',color=discord.Colour.random(),type='image')
            sbEmbed.set_image(url=submission.url)
            sbEmbed.set_author(name=ctx.message.author.display_name,icon_url=ctx.message.author.display_avatar.url)
            await ctx.reply(embed=sbEmbed)
            return
        sbEmbed = discord.Embed(title=sb_random.display_name,description=f'[{submission.title}]({submission.url})',color=discord.Colour.random())
        sbEmbed.set_author(name=ctx.message.author.display_name,icon_url=ctx.message.author.display_avatar.url)
        await ctx.reply(embed=sbEmbed)
        

    @commands.command(aliases=['rname','randomn'],name='randomname',description='Gives you a random name.')
    async def randomname(self,ctx):
        await ctx.trigger_typing()
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
        nameEmbed.set_author(name=ctx.message.author.display_name,icon_url=ctx.message.author.display_avatar.url)
        await ctx.reply(embed=nameEmbed)

    @commands.command(name='fact',description='Gives you a random fact.')
    async def fact(self, ctx):
        await ctx.trigger_typing()
        responseAPI = requests.get("https://uselessfacts.jsph.pl/random.json?language=en").json()   
        factID = responseAPI["id"]
        factResponse = responseAPI["text"]
        factLink = responseAPI["permalink"]

        factEmbed = discord.Embed(title='Fact',description=f'{factResponse}',color=discord.Colour.random())
        factEmbed.set_footer(text=f"ID: {factID}")
        factEmbed.add_field(name='Link',value=f'[Click!]({factLink})')
        factEmbed.set_author(name=ctx.message.author.display_name,icon_url=ctx.message.author.display_avatar.url)        
        await ctx.reply(embed=factEmbed)

    @commands.command(name='trivia',description='Play a trivia game.')
    async def _trivia(self, ctx, difficulty=None):
        if difficulty == None:
            url = 'https://opentdb.com/api.php?amount=1&type=boolean'
        else:
            url = f'https://opentdb.com/api.php?amount=1&type=boolean&difficulty={difficulty}'
            difficulty = difficulty.lower()
            allowedChoices = ['easy','medium','hard']
            if difficulty not in allowedChoices:
                return await ctx.reply('Please choose a difficulty of easy, medium or hard')
        
        responseAPI = requests.get(url).json()
        for i in responseAPI['results']:
            triviaCat = i['category']
            triviaDiff = i['difficulty']
            triviaQuestion = i['question']
            triviaQuestion = triviaQuestion.replace('&quot;','')
            triviaAnswer = i['correct_answer']
            triviaAnswer = triviaAnswer.lower()

        questionEmbed = discord.Embed(title='Trivia Question',description=f'{triviaQuestion}\nUse the reactions for either true or false.',color=discord.Colour.random())
        questionEmbed.set_author(name=ctx.message.author.display_name,icon_url=ctx.message.author.display_avatar.url)
        questionEmbed.set_thumbnail(url=self.client.user.display_avatar.url)
        questionEmbed.set_footer(text=f'Category: {triviaCat} | Difficulty: {triviaDiff}')
        msg = await ctx.reply(embed=questionEmbed)

        def check(reaction, user):
                return user == ctx.message.author and str(reaction.emoji) in choices
        choices = ['✅','❌']
        for reaction in choices:
            await msg.add_reaction(reaction)
        try:
            reaction = await self.client.wait_for('reaction_add',check=check,timeout=60.0)
        except asyncio.TimeoutError:
            return await ctx.reply(f'{ctx.author.mention} trivia question over, you took too long to respond.')
        
        if str(reaction[0].emoji) == choices[0]:
            playerAnswer = 'true'
        elif str(reaction[0].emoji) == choices[1]:
            playerAnswer = 'false'

        if playerAnswer == triviaAnswer:
            embed = discord.Embed(title='Trivia Question',description='You won!',color=discord.Colour.green())
            embed.set_thumbnail(url=self.client.user.display_avatar.url)
            embed_set_author(ctx, embed)
            await msg.reply(embed=embed)
        else:
            embed = discord.Embed(title='Trivia Question',description=f'You Lost!\nThe correct answer was: **{triviaAnswer}**',color=discord.Colour.red())
            embed.set_thumbnail(url=self.client.user.display_avatar.url)
            embed_set_author(ctx, embed)
            await msg.reply(embed=embed)

    @commands.command(name='dog',description='Sends a random dog.')
    async def _dog(self, ctx):
        await ctx.trigger_typing()
        url = 'https://dog.ceo/api/breeds/image/random'
        responseAPI = requests.get(url).json()
        dogPicture = responseAPI['message']

        embed = discord.Embed(title='Dog',description=dogPicture,color=discord.Colour.random(),type='image')
        embed.set_image(url=dogPicture)
        embed.set_footer(text=f'API: {url}')
        embed_set_author(ctx, embed)
        await ctx.reply(embed=embed)

    @commands.command(aliases=['cat','catrandom','neko'],name='randomcat',description='Gives you a random cat picture.')
    async def randomcat(self, ctx):
        await ctx.trigger_typing()
        for i in requests.get("https://api.thecatapi.com/v1/images/search").json():
            catURL = i["url"]
            catID = i["id"]

        catEmbed = discord.Embed(title='Cat',color=discord.Colour.random(),type='image')
        catEmbed.set_image(url=catURL)
        catEmbed.set_footer(text=f'ID: {catID}',icon_url=EmptyEmbed)
        catEmbed.set_author(name=ctx.message.author.display_name,icon_url=ctx.message.author.display_avatar.url)
        await ctx.reply(embed=catEmbed)

    @commands.command(aliases=['bored'],name='activity',description='Gives you something to do.')
    async def activity(self, ctx):

        await ctx.trigger_typing()
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
        activityEmbed.set_thumbnail(url=self.client.user.display_avatar.url)
        activityEmbed.set_author(name=ctx.message.author.display_name,icon_url=ctx.message.author.display_avatar.url)
        await ctx.reply(embed=activityEmbed)   

    @commands.command(name='advice',description='Gives you a random piece of advice.')
    async def advice(self, ctx):
        await ctx.trigger_typing()
        response_API = requests.get("https://api.adviceslip.com/advice")
        data = response_API.text
        parse_json = json.loads(data)
        currentAdvice = parse_json['slip']['advice']
        currentAdviceID = parse_json['slip']['id']

        adviceEmbed = discord.Embed(title='Advice',description=currentAdvice,color=discord.Colour.random())
        adviceEmbed.set_footer(text=f"ID: {currentAdviceID}",icon_url=EmptyEmbed)
        adviceEmbed.set_thumbnail(url=self.client.user.display_avatar.url)
        adviceEmbed.set_author(name=ctx.message.author.display_name,icon_url=ctx.message.author.display_avatar.url)
        await ctx.reply(embed=adviceEmbed)

    @commands.command(name='e',description='e')
    async def e(self, ctx,eAmount=None):
        eList = ""
        if eAmount != None:
            eAmount = int(eAmount)
        if eAmount == None:
            eAmount = random.randint(1,100)
        elif eAmount > 2000:
            eAmount = 2000
            await ctx.reply("Limit is 2000.")

        #await ctx.reply(eAmount)
        if ctx.message.author.id == 509436097835827210:
            eAmount = random.randint(100,2000)
        while 0 < eAmount:
            eList = eList + "e"
            eAmount = eAmount - 1
        await ctx.reply(eList)
        #await ctx.reply(eAmount)

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

            await ctx.reply("Repeating is now off.")
            return

        if sayCurrent == False:
            with open('json/data.json', 'r') as tf:
                sTrue = json.load(tf)

            sTrue[authorID] = True

            with open('json/data.json', 'w') as tf:
                json.dump(sTrue, tf, indent=4)
            await ctx.reply("Repeating is now on.")
            return



    @commands.command(aliases=['speak','saythis', 'copy', 'doasisayslave'], name='say', description='Makes the bot say what you want it to say')
    async def say(self, ctx, *, message=None):
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass
        #with open('json/econ.json', 'r') as ef:
        #    econ = json.load(ef)
        #if econ[f"{ctx.message.author.id} say"] == False:
        #    await ctx.reply("You do not own this command!")
        #    return
        message = message or "Please say something to use this command!"
        message_components = message.split()
        if "@everyone" in message_components or "@here" in message_components:
            await ctx.reply("You cannot have `@everyone` or `@here` in your message!")    
            return
        try:
            await ctx.reply(f'{message}\nMessage from {ctx.message.author.mention}')
        except:
            await ctx.send(f'{message}\nMessage from {ctx.message.author.mention}')
        


    @commands.command(name='reverse',description='Reverses a text.')
    async def reverse(self,ctx,*,message=None):
        if message == None:
            def check(ms):
                return ms.channel == ctx.message.channel and ms.author == ctx.message.author
            askMessage = await ctx.reply("What's your messaage?")
            OtherMessage = await self.client.wait_for('message', check=check)
            message = OtherMessage.content
            try:
                await askMessage.delete()
                await OtherMessage.delete()
            except discord.Forbidden:
                pass

        reverseMessage = message[::-1]
        await ctx.reply(reverseMessage)

    @commands.command(aliases=['coinflip','coin_flip'],name='flip',description='Flips a coin.')
    async def flip(self, ctx):
        coin = ['Heads', 'Tails']
        result = random.choice(coin)
        
        flipEmbed = discord.Embed(title=':coin:',description=f'The coin landed on **{result}**.',color=discord.Colour.random())
        flipEmbed.set_thumbnail(url=self.client.user.display_avatar.url)
        flipEmbed.set_author(
            name=ctx.message.author.display_name,
            icon_url=ctx.message.author.display_avatar.url
        )
        await ctx.reply(embed=flipEmbed)

    @commands.command(aliases=["roll"],name='dice',description='Rolls a dice from 1-6.')
    async def dice(self, ctx):
        roll = randint(1,6)
        diceEmbed = discord.Embed(title=":game_die:",description=f'The dice rolled a **{roll}**.',color=discord.Colour.random())
        diceEmbed.set_thumbnail(url=self.client.user.display_avatar.url)
        diceEmbed.set_author(
            name=ctx.message.author.display_name,
            icon_url=ctx.message.author.display_avatar.url
        )
        await ctx.reply(embed=diceEmbed)

    # @commands.command(aliases=['rockpaperscissors'],name='rps',description='Play Rock Paper Scissors against someone')
    # async def _rps(self, ctx, user: commands.MemberConverter):
    #     if ctx.author.dm_channel == None:
    #         await ctx.author.create_dm()
    #     if user.dm_channel == None:
    #         await user.create_dm()
    #     def check(ms):
    #         return ms.channel == ctx.message.channel and ms.author == user
    #     def check2(ms):
    #         return ms.channel == ctx.author.dm_channel and ms.author == ctx.message.author
    #     def check3(ms):
    #         return ms.channel == user.dm_channel and ms.author == user
    #     choices = ['rock','paper','scissors']

    #     await ctx.send(f'{user.mention}\n{ctx.message.author.mention} has challenged you to a game of Rock Paper Scissors, do you accept?\n(yes or no)')
    #     msg = await self.client.wait_for('message',check=check)
    #     if msg.content.lower() != 'yes':
    #         return await ctx.reply(f'{user.mention} denied the rock paper scissors challenge.')
    #     await ctx.reply(f'{user.mention} accepted the challenge! I will DM {ctx.message.author.mention} first then {user.mention}')

    #     await ctx.message.author.send('Your turn! Rock, Paper or Scissors?')
    #     msg = await self.client.wait_for('message',check=check2)
    #     if msg.content.lower() not in choices:
    #         await msg.reply('invalid choice, cancelling challenge')
    #         return await ctx.send(f'{ctx.author.mention} used an invalid choice of {msg.content}, challenge cancelled.')
    #     authorChoice = msg.content.lower()

    #     await user.send('Your turn! Rock, Paper or Scissors?')
    #     msg = await self.client.wait_for('message',check=check3)
    #     if msg.content.lower() not in choices:
    #         await msg.reply('invalid choice, cancelling challenge')
    #         return await ctx.send(f'{user.mention} used an invalid choice of {msg.content}, challenge cancelled.')
    #     userChoice = msg.content.lower()

    #     authorWinEmbed = discord.Embed(title=f'{ctx.author.display_name} won!',description=f'{ctx.author.mention} chose {authorChoice} which beat {userChoice}')
    #     authorWinEmbed.set_thumbnail(url=self.client.user.display_avatar.url)
    #     embed_set_author(ctx, authorWinEmbed)

    #     userWinEmbed = discord.Embed(title=f'{user.display_name} won!',description=f'{user.mention} chose {userChoice} which beat {authorChoice}')
    #     userWinEmbed.set_thumbnail(url=self.client.user.display_avatar.url)
    #     embed_set_author(ctx, userWinEmbed)
        
    #     tieEmbed = discord.Embed(title='Tie',description=f'{user.mention} and {ctx.author.mention} both chose {userChoice}')
    #     tieEmbed.set_thumbnail(url=self.client.user.display_avatar.url)
    #     embed_set_author(ctx, tieEmbed)

    #     if authorChoice == 'rock':
    #         if userChoice == 'rock':
    #             await ctx.reply(embed=tieEmbed)
    #         elif userChoice == 'paper':
    #             await ctx.reply(embed=userWinEmbed)
    #         elif userChoice == 'scissors':
    #             await ctx.reply(embed=authorWinEmbed)
    #     elif authorChoice == 'paper':
    #         if userChoice == 'rock':
    #             await ctx.reply(embed=authorWinEmbed)
    #         elif userChoice == 'paper':
    #             await ctx.reply(embed=tieEmbed)
    #         elif userChoice == 'scissors':
    #             await ctx.reply(embed=userWinEmbed)
    #     elif authorChoice == 'scissors':
    #         if userChoice == 'rock':
    #             await ctx.reply(embed=userWinEmbed)
    #         elif userChoice == 'paper':
    #             await ctx.reply(embed=authorWinEmbed)
    #         elif userChoice == 'scissors':
    #             await ctx.reply(embed=tieEmbed)

    @commands.command(aliases=['rockpaperscissors'],name='rps',description='Play Rock Paper Scissors against someone')
    async def _rps(self, ctx, user: commands.MemberConverter=None):
        if ctx.author.dm_channel == None:
            await ctx.author.create_dm()
        def check(reaction, member):
            return member == user and str(reaction.emoji) in askChoices
        def check2(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) in choices
        def check3(reaction, member):
            return member == user and str(reaction.emoji) in choices
        choices = ['🪨','📝','✂️']
        askChoices = ['✅','❌']

        if user != None:
            if user.dm_channel == None:
                await user.create_dm()
            msg = await ctx.send(f'{user.mention}\n{ctx.message.author.mention} has challenged you to a game of Rock Paper Scissors, do you accept?\n(use the reactions)')
            for reaction in askChoices:
                await msg.add_reaction(reaction)
            try:
                reaction = await self.client.wait_for('reaction_add',check=check,timeout=60.0)
            except asyncio.TimeoutError:
                return await ctx.reply(f'{user.mention} took to long to respond to the rock paper scissors challenge.')

            if str(reaction[0].emoji) == askChoices[1]:
                return await ctx.reply(f'{user.mention} denied the rock paper scissors challenge.')
            elif str(reaction[0].emoji) == askChoices[0]:
                await ctx.reply(f'{user.mention} accepted the challenge! I will DM {ctx.message.author.mention} first then {user.mention}')
            else:
                return await ctx.reply('An error happened')
            msg = await ctx.message.author.send('Your turn! Rock, Paper or Scissors?\nUse the reactions to pick!')
        else:
            msg =  await ctx.reply('Rock, Paper or Scissors?\nUse the reactions to pick!')
        for reaction in choices:
            await msg.add_reaction(reaction)
        reaction = await self.client.wait_for('reaction_add',check=check2)

        if str(reaction[0].emoji) == choices[0]:
            authorChoice = "rock"
        elif str(reaction[0].emoji) == choices[1]:
            authorChoice = "paper"
        elif str(reaction[0].emoji) == choices[2]:
            authorChoice = "scissors"
        else:
            return await ctx.send(f'{ctx.author.mention} used an invalid reaction')

        if user != None:
            msg = await user.send('Your turn! Rock, Paper or Scissors?\nUse the reactions to pick!')
            for reaction in choices:
                await msg.add_reaction(reaction)
            reaction = await self.client.wait_for('reaction_add',check=check3)

            if str(reaction[0].emoji) == choices[0]:
                userChoice = "rock"
            elif str(reaction[0].emoji) == choices[1]:
                userChoice = "paper"
            elif str(reaction[0].emoji) == choices[2]:
                userChoice = "scissors"
            else:
                return await ctx.send(f'{user.mention} used an invalid reaction')
        else:
            botChoices = ['rock','paper','scissors']
            userChoice = random.choice(botChoices)
        

        authorWinEmbed = discord.Embed(title=f'{ctx.author.display_name} won!',description=f'{ctx.author.mention} chose {authorChoice} which beat {userChoice}')
        authorWinEmbed.set_thumbnail(url=self.client.user.display_avatar.url)
        embed_set_author(ctx, authorWinEmbed)

        if user != None:
            userWinEmbed = discord.Embed(title=f'{user.display_name} won!',description=f'{user.mention} chose {userChoice} which beat {authorChoice}')
            userWinEmbed.set_thumbnail(url=self.client.user.display_avatar.url)
            embed_set_author(ctx, userWinEmbed)
            
            tieEmbed = discord.Embed(title='Tie',description=f'{user.mention} and {ctx.author.mention} both chose {userChoice}')
            tieEmbed.set_thumbnail(url=self.client.user.display_avatar.url)
            embed_set_author(ctx, tieEmbed)
        else:
            userWinEmbed = discord.Embed(title=f'Dubot won!',description=f'Dubot chose {userChoice} which beat {authorChoice}')
            userWinEmbed.set_thumbnail(url=self.client.user.display_avatar.url)
            embed_set_author(ctx, userWinEmbed)
            
            tieEmbed = discord.Embed(title='Tie',description=f'Dubot and {ctx.author.mention} both chose {userChoice}')
            tieEmbed.set_thumbnail(url=self.client.user.display_avatar.url)
            embed_set_author(ctx, tieEmbed)

        if authorChoice == 'rock':
            if userChoice == 'rock':
                await ctx.reply(embed=tieEmbed)
            elif userChoice == 'paper':
                await ctx.reply(embed=userWinEmbed)
            elif userChoice == 'scissors':
                await ctx.reply(embed=authorWinEmbed)
        elif authorChoice == 'paper':
            if userChoice == 'rock':
                await ctx.reply(embed=authorWinEmbed)
            elif userChoice == 'paper':
                await ctx.reply(embed=tieEmbed)
            elif userChoice == 'scissors':
                await ctx.reply(embed=userWinEmbed)
        elif authorChoice == 'scissors':
            if userChoice == 'rock':
                await ctx.reply(embed=userWinEmbed)
            elif userChoice == 'paper':
                await ctx.reply(embed=authorWinEmbed)
            elif userChoice == 'scissors':
                await ctx.reply(embed=tieEmbed)


    #@commands.command(name='rps',description='Play Rock Paper Scissors against the bot.')
    #async def rps(self, ctx, message):
    #    answer = message.lower()
    #    choices = ["rock", "paper", "scissors"]
    #    computers_answer = random.choice(choices)
    #    if answer not in choices:
    #        incorrectEmbed = discord.Embed(title="Invalid",description=f"'{answer}' is not valid. Please use one of the following: rock, paper, scissors.",color=discord.Colour.random())
    #        incorrectEmbed.set_thumbnail(url=self.client.user.display_avatar.url)
    #        incorrectEmbed.set_author(
    #            name=ctx.message.author.display_name,
    #            icon_url=ctx.message.author.display_avatar.url
    #        )
    #        await ctx.reply(embed=incorrectEmbed)
    #    else:
    #        if computers_answer == answer:
    #            answerEmbed = discord.Embed(color=discord.Colour.random(),title="Tie",description=f"We both picked **{answer}**.")
    #            answerEmbed.set_thumbnail(url=self.client.user.display_avatar.url)
    #            answerEmbed.set_author(
    #                name=ctx.message.author.display_name,
    #                icon_url=ctx.message.author.display_avatar.url
    #            )
    #            await ctx.reply(embed=answerEmbed)
    #        if computers_answer == "rock":
    #            if answer == "paper":
    #                answerEmbed = discord.Embed(color=discord.Colour.random(),title="You win",description=f"I picked **{computers_answer}**. :rock:")
    #                answerEmbed.set_thumbnail(url=self.client.user.display_avatar.url)
    #                answerEmbed.set_author(
    #                    name=ctx.message.author.display_name,
    #                    icon_url=ctx.message.author.display_avatar.url
    #                )
    #                await ctx.reply(embed=answerEmbed) 
    #            if answer == "scissors":
    #                answerEmbed = discord.Embed(color=discord.Colour.random(),title="I win",description=f"I picked **{computers_answer}**. :rock:")
    #                answerEmbed.set_thumbnail(url=self.client.user.display_avatar.url)
    #                answerEmbed.set_author(
    #                    name=ctx.message.author.display_name,
    #                    icon_url=ctx.message.author.display_avatar.url
    #                )
    #                await ctx.reply(embed=answerEmbed) 
    #        if computers_answer == "paper":
    #            if answer == "rock":
    #                answerEmbed = discord.Embed(color=discord.Colour.random(),title="I win",description=f"I picked **{computers_answer}**. :newspaper:")
    #                answerEmbed.set_thumbnail(url=self.client.user.display_avatar.url)
    #                answerEmbed.set_author(
    #                    name=ctx.message.author.display_name,
    #                    icon_url=ctx.message.author.display_avatar.url
    #                )
    #                await ctx.reply(embed=answerEmbed) 
    #            if answer == "scissors":
    #                answerEmbed = discord.Embed(color=discord.Colour.random(),title="You win",description=f"I picked **{computers_answer}**. :newspaper:")
    #                answerEmbed.set_thumbnail(url=self.client.user.display_avatar.url)
    #                answerEmbed.set_author(
    #                    name=ctx.message.author.display_name,
    #                    icon_url=ctx.message.author.display_avatar.url
    #                )
    #                await ctx.reply(embed=answerEmbed) 
    #        if computers_answer == "scissors":
    #            if answer == "rock":
    #                answerEmbed = discord.Embed(color=discord.Colour.random(),title="You win",description=f"I picked **{computers_answer}**. :scissors:")
    #                answerEmbed.set_thumbnail(url=self.client.user.display_avatar.url)
    #                answerEmbed.set_author(
    #                    name=ctx.message.author.display_name,
    #                    icon_url=ctx.message.author.display_avatar.url
    #                )
    #                await ctx.reply(embed=answerEmbed) 
    #            if answer == "paper":
    #                answerEmbed = discord.Embed(color=discord.Colour.random(),title="I win",description=f"I picked **{computers_answer}**. :scissors:")
    #                answerEmbed.set_thumbnail(url=self.client.user.display_avatar.url)
    #                answerEmbed.set_author(
    #                    name=ctx.message.author.display_name,
    #                    icon_url=ctx.message.author.display_avatar.url
    #                )
    #                await ctx.reply(embed=answerEmbed) 

    @commands.command(aliases=['ng','numberg','numberguess'], name='nguess', description='Guess the bots number.')
    async def nguess(self,ctx, *, number=0):
        number_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        correct_number = random.choice(number_list)
        if number == correct_number:
            embedVar = discord.Embed(title=f'Your Number Is {number}', color=0x2ECC71)
            embedVar.add_field(name='You Picked The Correct Number! You Won', value=f"The correct number was {correct_number}.")
            await ctx.reply(embed=embedVar)
        
        else:
            embedVar = discord.Embed(title=f'Your Number Is {number}', color=0xE74C3C)
            embedVar.add_field(name="Sorry, You Picked The Wrong Number", value=f"The correct number was {correct_number}.")
            await ctx.reply(embed=embedVar)
    



#    @commands.command(name='dm', description='Sends a DM to the user you @')
#    async def dm(self, ctx, user: discord.Member):
#        await ctx.reply(f"sliding into {user.mention}'s DMs")
#        responses = ['hows it goin bb', '*slides into your DMs* wassup baby girl', 'hey', 'uwu *pounces on you* rawr x3 owo? whats this? *notices your buldge*', 'you just got ***botted***  :sunglasses:', 'get DMed punk', 'Duzo is my God', '0portalboy0 is my God']
#        choice = random.choice(responses)
#        await user.send(f"{choice}")
#        await ctx.reply(f'i DMed them and said "{choice}"')

    #@commands.command(aliases=['trick or treat', 'trickortreat', 'trick-or-treat', 'trick_or_treat'], name='Trick or Treat', description='A command that only works on Halloween')
    #async def tricktreat(self, ctx):
    #    responses = ['Trick! Muhahaha :ghost:', "Treat! Here's some candy  :candy:", "Treat! Here's some sweets  :candy:"]
    #    await ctx.reply(f'{random.choice(responses)}')


#    @commands.command(name='datetime', description='Gives the date and time (in the UK)')
#    async def datetime(self, ctx):
#        now = datetime.now()
#        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
#        await ctx.reply(f"It is {dt_string} right now in the UK.")

#    @commands.command(name='time', description='Gives the current time (in the UK)')
#    async def time(self, ctx):
#        now = datetime.now()
#        dt_string = now.strftime("%H:%M:%S")
#        await ctx.reply(f"The time in the UK is {dt_string}.")

#    @commands.command(name='date', description='Gives the date (in the UK)')
#    async def date(self, ctx):
#        today = date.today()
#        datenow = today.strftime("%B %d, %Y")
#        await ctx.reply(f"The date in the UK is {datenow}.") 

    @commands.command(name='nwordchoice',description='Do you want this feature enabled?')
    async def _nwordchoice(self, ctx, choice=None):
        if choice == None:
            msg = await ctx.reply('Do you want this to be enabled?\nUse the reactions')
            def check(reaction, user):
                    return user == ctx.message.author and str(reaction.emoji) in choices
            choices = ['✅','❌']
            for reaction in choices:
                await msg.add_reaction(reaction)
            try:
                reaction = await self.client.wait_for('reaction_add',check=check,timeout=60.0)
            except asyncio.TimeoutError:
                return await ctx.reply(f'{ctx.author.mention} you took too long to respond (60 seconds)')
            
            if str(reaction[0].emoji) == choices[0]:
                choice = 'true'
            elif str(reaction[0].emoji) == choices[1]:
                choice = 'false'
                
        choice = choice.lower()
        if choice != 'false' and choice != 'true':
            return await ctx.reply('invalid choice.')

        with open('json/data.json','r') as f:
            data = json.load(f)

        if choice == 'false':
            data[f'{ctx.guild.id} nword'] = False
            with open('json/data.json', 'w') as f:
                json.dump(data, f, indent=4)
            return await ctx.reply('Feature disabled.')

        data[f'{ctx.guild.id} nword'] = True
        with open('json/data.json', 'w') as f:
            json.dump(data, f, indent=4)
        await ctx.reply('Feature enabled.')        

    @commands.command(name='nwordcount',description='How many times you have been racist!')
    async def _nwordcount(self, ctx, user: commands.MemberConverter=None):
        if user == None:
            user = ctx.message.author
        with open('json/data.json', 'r') as f:
            data = json.load(f)
        
        count = data[f'{user.id} nwordcount']

        await ctx.reply(f'{user.mention} has said the n word {count} times.')

    @commands.command(name='pedo',description='sends info on a random sex offender')
    async def _pedo(self, ctx):
        await ctx.trigger_typing()
        url = 'https://maps2.dcgis.dc.gov/dcgis/rest/services/FEEDS/MPD/MapServer/20/query?where=1%3D1&outFields=FIRSTNAME,LASTNAME,ALIASES,ZIPCODE,LATITUDE,LONGITUDE&returnGeometry=false&outSR=1&f=json'
        responseAPI = requests.get(url).json()
        chosen_pedo = random.choice(responseAPI['features'])
        chosen_pedo = chosen_pedo['attributes']
        pedo_firstName = chosen_pedo['FIRSTNAME']
        pedo_lastName = chosen_pedo['LASTNAME']
        pedo_aliases = chosen_pedo['ALIASES']
        pedo_zipcode = chosen_pedo['ZIPCODE']
        pedo_latitude = chosen_pedo['LATITUDE']
        pedo_longitude = chosen_pedo['LONGITUDE']

        embed = discord.Embed(title='Random Pedophile',color=discord.Colour.random())
        embed.add_field(name='Name:',value=f'{pedo_firstName} {pedo_lastName}')
        embed.add_field(name='Aliases:',value=pedo_aliases)
        embed.add_field(name='Zipcode:',value=pedo_zipcode)
        embed.add_field(name='Latitude:',value=pedo_latitude)
        embed.add_field(name='Longitude:',value=pedo_longitude)
        embed_set_author(ctx, embed)
        await ctx.reply(embed=embed)

    @commands.command(aliases=["furry"], name='howfurry', description='Gives a value from 1-100 depending on how much of a furry you are')
    async def howfurry(self, ctx, user : commands.MemberConverter=None):
        if user == None:
            user = ctx.message.author
        randomfurry = randint(0,100)

        if user.id == 673124115250544661:
            randomfurry = 0
        elif user.id == 597102599694712844 or user.id == 509436097835827210 or user.id == 578844127878184961:
            randomfurry = 100 
        elif user.id == 595358806389555201:
            randomfurry = "-1"
        elif user.id == 475231164173385728:
            randomfurry = "-100"

        embed = discord.Embed(title=f'How much of a furry is {user.display_name}?', description=f'{user.mention} is **{randomfurry}%** furry.',color=discord.Colour.random(),type='image')
        embed.set_image(url='https://upload.wikimedia.org/wikipedia/commons/a/aa/Furry_flag.png')
        embed.set_author(
            name=ctx.message.author.display_name,
            icon_url=ctx.message.author.display_avatar.url
        )
        await ctx.reply(embed=embed)

    @commands.command(aliases=["bi"], name='bisexual', description='actually predicts if your are bi or yourent bi')
    async def bi(self, ctx, user : commands.MemberConverter=None):
        if user == None:
            user = ctx.message.author
        
        choices = ['is bisexual','is not bisexual']
        randombi = random.choice(choices)
        if user.id == 509436097835827210 or user.id == 597102599694712844 or user.id == 578844127878184961 or user.id == 327807253052653569 or user.id == 709763530232168560: 
            randombi = choices[0]
        embed = discord.Embed(title=f'is {user.display_name} bi?', description=f'{user.mention} {randombi}',color=discord.Colour.random(),type='image')
        embed.set_image(url='https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Bisexual_Pride_Flag.svg/800px-Bisexual_Pride_Flag.svg.png')
        embed_set_author(ctx, embed)
        await ctx.reply(embed=embed)

    @commands.command(aliases=["gay"], name='howgay', description='Gives a value from 1-100 depending on how gay you are')
    async def howgay(self, ctx, user : commands.MemberConverter=None):
        if user == None:
            user = ctx.message.author
        randomgay = randint(0,100)
        if user.id == 709763530232168560:
            randomgay = 100
        elif user.id == 509436097835827210 or user.id == 597102599694712844 or user.id == 578844127878184961 or user.id == 327807253052653569: 
            randomgay = 50
        gayembed = discord.Embed(title=f'How gay is {user.display_name}?', description=f'{user.mention} is **{randomgay}%** gay.',color=discord.Colour.random(),type='image')
        gayembed.set_image(url='https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Gay_Pride_Flag.svg/383px-Gay_Pride_Flag.svg.png')
        gayembed.set_author(
            name=ctx.message.author.display_name,
            icon_url=ctx.message.author.display_avatar.url
        )
        await ctx.reply(embed=gayembed)

    @commands.command(name='love',description='Sees how compatible two people are.')
    async def _love(self, ctx, user1: commands.MemberConverter=None,user2: commands.MemberConverter=None):
        if user1 == None or user2 == None:
            return await ctx.send("Please define both people.")
        
        loveEmbed = discord.Embed(title=f'How compatible are {user1.display_name} and {user2.display_name}?',description=f'{user1.display_name} and {user2.display_name} are {randint(1,100)}% compatible',color=discord.Colour.random(),type='image')
        loveEmbed.set_image(url='https://upload.wikimedia.org/wikipedia/commons/f/f1/Heart_coraz%C3%B3n.svg')
        loveEmbed.set_author(
            name=ctx.message.author.display_name,
            icon_url=ctx.message.author.display_avatar.url
        )
        await ctx.reply(embed=loveEmbed)


    #@commands.command(name='ping', description='Gets the bots ping')
    #async def ping(self, ctx):
    #    await ctx.reply('Why do you want this from me. Please leave me alone.')

    @commands.command(name='gif', description='Looks up a gif using tenor. Seperate tags with spaces.')
    async def _gif(self, ctx,*, query=None):
        query_seperate = query.replace(' ', '+')
        url = f'https://api.tenor.com/v1/random?key=LIVDSRZULELA&q={query_seperate}&limit=1'
        if query == None:
            url = 'https://api.tenor.com/v1/random?key=LIVDSRZULELA&limit=1'
        responseApi = requests.get(url).json()
        gif = responseApi['results'][0]['media'][0]['gif']['url']

        embed = discord.Embed(title=f'{query}',description=f'Result for {query} on Tenor',type='gifv')
        embed.set_image(url=gif)
        embed_set_author(ctx, embed)
        await ctx.reply(embed=embed)

    @commands.command(name='meth', description='meth')
    async def _meth(self, ctx):
        gif = 'https://media.tenor.com/images/b4ff5850dbdc71b5f9da4c87d132be0d/tenor.gif'

        embed = discord.Embed(title=f'{ctx.author.display_name} meth',description=f'meth {ctx.author.mention}',color=0xA7C7E7,type='gifv')
        embed.set_image(url=gif)
        embed.set_footer(text='meth video by monke :)')
        embed_set_author(ctx, embed)
        await ctx.reply(embed=embed,file=discord.File('./meth.mp4'))

    @commands.command(name='headpat', description='Lets you headpat a user you @')
    async def _headpat(self, ctx, user: commands.MemberConverter):   
        url = 'https://api.tenor.com/v1/random?key=LIVDSRZULELA&q=anime+headpat&limit=1'
        responseApi = requests.get(url).json()
        gif = responseApi['results'][0]['media'][0]['gif']['url']

        embed = discord.Embed(title=f'{ctx.author.display_name} headpats {user.display_name}',description=f'{ctx.author.mention} headpats {user.mention}',color=0xF8C8DC,type='gifv')
        embed.set_image(url=gif)
        embed_set_author(ctx, embed)
        await ctx.reply(embed=embed)

    @commands.command(name='hug', description='Lets you hug a user you @')
    async def hug(self, ctx, user: commands.MemberConverter):   
        url = 'https://api.tenor.com/v1/random?key=LIVDSRZULELA&q=anime+hug&limit=1'
        responseApi = requests.get(url).json()
        gif = responseApi['results'][0]['media'][0]['gif']['url']

        embed = discord.Embed(title=f'{ctx.author.display_name} hugs {user.display_name}',description=f'{ctx.author.mention} hugs {user.mention}',color=0xF8C8DC,type='gifv')
        embed.set_image(url=gif)
        embed_set_author(ctx, embed)
        await ctx.reply(embed=embed)

    @commands.command(name='kiss', description='Lets you kiss a user you @')
    async def _kiss(self, ctx, user: commands.MemberConverter):
        url = 'https://api.tenor.com/v1/random?key=LIVDSRZULELA&q=anime+kiss&limit=1'
        responseApi = requests.get(url).json()
        gif = responseApi['results'][0]['media'][0]['gif']['url']

        embed = discord.Embed(title=f'{ctx.author.display_name} kisses {user.display_name}',description=f'{ctx.author.mention} kisses {user.mention}',color=0xF8C8DC,type='gifv')
        embed.set_image(url=gif)
        embed_set_author(ctx, embed)
        await ctx.reply(embed=embed)

    @commands.command(name='slap', description='Lets you slap a user you @')
    async def slap(self, ctx, user: commands.MemberConverter):
        url = 'https://api.tenor.com/v1/random?key=LIVDSRZULELA&q=anime+slap&limit=1'
        responseApi = requests.get(url).json()
        gif = responseApi['results'][0]['media'][0]['gif']['url']

        embed = discord.Embed(title=f'{ctx.author.display_name} slaps {user.display_name}',description=f'{ctx.author.mention} slaps {user.mention}',color=0xa91834,type='gifv')
        embed.set_image(url=gif)
        embed_set_author(ctx, embed)
        await ctx.reply(embed=embed)

    @commands.command(name='kill', description='Lets you kill a user you @')
    async def kill(self, ctx, user: commands.MemberConverter):
        url = 'https://api.tenor.com/v1/random?key=LIVDSRZULELA&q=anime+kill&limit=1'
        responseApi = requests.get(url).json()
        gif = responseApi['results'][0]['media'][0]['gif']['url']

        embed = discord.Embed(title=f'{ctx.author.display_name} kills {user.display_name}',description=f'{ctx.author.mention} kills {user.mention}',color=0xa91834,type='gifv')
        embed.set_image(url=gif)
        embed_set_author(ctx, embed)
        await ctx.reply(embed=embed)

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
        mesg = await ctx.reply(content='What would you like the title to be?')

        # Wait for a response and get the title
        msg = await self.client.wait_for('message', check=check)
        title = msg.content # Set the title
        try:
            await msg.delete()
            await mesg.delete()
        except discord.Forbidden:
            pass

        # Next, ask for the content
        mesg = await ctx.reply(content='What would you like the Description to be?')
        msg = await self.client.wait_for('message', check=check)
        desc = msg.content
        try:
            await msg.delete()
            await mesg.delete()
        except discord.Forbidden:
            pass

        # Finally make the embed and send it
        msg = await ctx.reply(content='Now generating the embed...')

        # Convert the colors into a list
        # To be able to use random.choice on it

        embed = discord.Embed(
            title=title,
            description=desc,
            color=discord.Colour.random()
        )
        # Also set the thumbnail to be the bot's pfp
        embed.set_thumbnail(url=self.client.user.display_avatar.url)

        # Also set the embed author to the command user
        embed.set_author(
            name=ctx.message.author.display_name,
            icon_url=ctx.message.author.display_avatar.url
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
#        await ctx.reply('im not gay you are')

#    @commands.command(name='fightclub', description='We dont talk about fight club')
#    async def fightclub(self, ctx):
#        await ctx.reply("We dont talk about fight club here. No fight clubs in this server, Officer.")

    @commands.command(name='yn',description='Gives you a yes or no answer.')
    async def yn(self, ctx, *, question):
        responses=['Yes.','No.']
        answer = random.choice(responses)
        ynEmbed = discord.Embed(title=question,description=answer,color=discord.Colour.random())
        ynEmbed.set_author(
            name=ctx.message.author.display_name,
            icon_url=ctx.message.author.display_avatar.url
        )
        ynEmbed.set_thumbnail(url=self.client.user.display_avatar.url)
        await ctx.reply(embed=ynEmbed)

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
            name=ctx.message.author.display_name,
            icon_url=ctx.message.author.display_avatar.url
        )
        ballembed.set_thumbnail(url=self.client.user.display_avatar.url)
        await ctx.reply(embed=ballembed)




def setup(client):
    client.add_cog(Fun(client))