from operator import truediv
from discord import channel, client
from discord.errors import NotFound
from random_word import RandomWords
rword = RandomWords()
from PyDictionary import PyDictionary
dict = PyDictionary
#import re
import discord
from discord import guild
from discord.ext import commands
import random
import json
from discord.ext.commands.converter import MessageConverter
from discord.ext.commands.core import has_permissions, is_nsfw
import praw
import requests

# Getting items from config.json
with open('config.json','r') as cf:
    config = json.load(cf)

ownerID = config['ownerID']
redditID = config['redditID']
redditSecret = config['redditSecret']
redditAgent = config['redditAgent']
reddit = praw.Reddit(client_id=redditID,client_secret=redditSecret,user_agent=redditAgent,check_for_async=False)

# le cog of le other
class Other(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['rule34'],name='nsfw',description='Finds a nsfw image of what you request.')
    @is_nsfw()
    async def _nsfw(self, ctx, request=None):
        await ctx.trigger_typing()
        if request == None:
            nsfwJson = requests.get("http://api.rule34.xxx//index.php?page=dapi&s=post&q=index&json=1").json()
        else:
            nsfwJson = requests.get("http://api.rule34.xxx//index.php?page=dapi&s=post&q=index&json=1&tags="+request).json()
        chosenKey = random.choice(nsfwJson)
        nsfwFile = chosenKey["file_url"]
        nsfwID = chosenKey["id"]
        nsfwTags = chosenKey["tags"].split()

        tagMessage = ""
        for i in nsfwTags:
            tagMessage = tagMessage + f"`{i}` "


        nsfw_extension = nsfwFile[len(nsfwFile) - 3 :].lower()
        if nsfw_extension == "mp4":
            nsfwPreview = chosenKey["preview_url"]
            nsfwEmbed = discord.Embed(title="Click description for full video.",description=f"[{request}]({nsfwFile})",color=discord.Colour.random(),type='image')
            nsfwEmbed.set_image(url=nsfwPreview)
            nsfwEmbed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
            nsfwEmbed.add_field(name='Tags:',value=tagMessage)
            nsfwEmbed.set_footer(text=f"ID: {nsfwID} | API by api.rule34.xxx")
            await ctx.reply(embed=nsfwEmbed)
            return
        if nsfw_extension == "jpg" or nsfw_extension == "peg" or nsfw_extension == "png" or nsfw_extension == "gif":
            nsfwEmbed = discord.Embed(title="NSFW",description=f'[{request}]({nsfwFile})',color=discord.Colour.random(),type='image')
            nsfwEmbed.set_image(url=nsfwFile)
            nsfwEmbed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
            nsfwEmbed.add_field(name='Tags:',value=tagMessage)
            nsfwEmbed.set_footer(text=f"ID: {nsfwID} | API by api.rule34.xxx")
            await ctx.reply(embed=nsfwEmbed)
            return
        await ctx.reply("An error occured while trying to get data from the API.")
            
    



    @commands.command(name='nsfwreddit',description='Get posts from a random nsfw subreddit.')
    @is_nsfw()
    async def _nsfwreddit(self, ctx):
        await ctx.trigger_typing()
        sb_random = reddit.random_subreddit(nsfw=True)
        sb_submissions=sb_random.hot()
        post_to_pick = random.randint(1,20)
        for i in range(0,post_to_pick):
            submission = next(x for x in sb_submissions if not x.stickied)


        sb_extension = submission.url[len(submission.url) - 3 :].lower()
        if sb_extension == "jpg" or sb_extension == "png" or sb_extension == "gif":
            sbEmbed = discord.Embed(title=sb_random.display_name,description=f'[{submission.title}]({submission.url})',color=discord.Colour.random(),type='image')
            sbEmbed.set_image(url=submission.url)
            sbEmbed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
            await ctx.reply(embed=sbEmbed)
            return
        sbEmbed = discord.Embed(title=sb_random.display_name,description=f'[{submission.title}]({submission.url})',color=discord.Colour.random())
        sbEmbed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
        await ctx.reply(embed=sbEmbed)

    @commands.command(name='vote',description='Vote for the bot.')
    async def _vote(self, ctx):
        voteEmbed = discord.Embed(title=f'Vote',description=f'[top.gg](https://top.gg/bot/{self.client.user.id}/vote)',color=discord.Colour.random())
        voteEmbed.set_thumbnail(url=self.client.user.avatar_url)
        voteEmbed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
        await ctx.reply(embed=voteEmbed)


    # @commands.command(name='slashcommand',description='run this command or else')
    # async def _slashCommand(self, ctx):
    #     await ctx.reply("GET THE SLASH COMMANDS BOT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    #     inviteEmbed = discord.Embed(title="Invite Link",description="[Bot Invite](https://discord.com/api/oauth2/authorize?client_id=900481597311172660&permissions=0&scope=bot%20applications.commands)",color=discord.Colour.random())
    #     inviteEmbed.add_field(name='Support Server',value="[Server Invite](https://discord.gg/Raakw6367z)")
    #     await ctx.reply(embed=inviteEmbed)

    @commands.command(name='math',description='Does calculations')
    async def math(self,ctx):
        def check(ms):
            return ms.channel == ctx.message.channel and ms.author == ctx.message.author


        msg = await ctx.reply("What is the first number?")
        Msg = await self.client.wait_for('message', check=check)
        numberOne=int(Msg.content)
        await msg.delete()
        await Msg.delete()

        msg = await ctx.reply("What is the operator? ( + - / * )")
        Msg = await self.client.wait_for('message', check=check)
        numberOperator = Msg.content
        await msg.delete()
        await Msg.delete()

        msg = await ctx.reply("What is the second number?")
        Msg = await self.client.wait_for('message', check=check)
        numberTwo = int(Msg.content)
        await msg.delete()
        await Msg.delete()



        if numberOperator == "+":
            numberEmbed = discord.Embed(title=f'{numberOne} {numberOperator} {numberTwo}',description=numberOne+numberTwo,color=discord.Color.random())
            numberEmbed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
            numberEmbed.set_thumbnail(url=self.client.user.avatar_url)
            await ctx.reply(embed=numberEmbed)
            return
        elif numberOperator == "-":
            numberEmbed = discord.Embed(title=f'{numberOne} {numberOperator} {numberTwo}',description=numberOne-numberTwo,color=discord.Color.random())
            numberEmbed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
            numberEmbed.set_thumbnail(url=self.client.user.avatar_url)
            await ctx.reply(embed=numberEmbed)
            return
        elif numberOperator == "/":
            numberEmbed = discord.Embed(title=f'{numberOne} {numberOperator} {numberTwo}',description=numberOne/numberTwo,color=discord.Color.random())
            numberEmbed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
            numberEmbed.set_thumbnail(url=self.client.user.avatar_url)
            await ctx.reply(embed=numberEmbed)
            return
        elif numberOperator == "*":
            numberEmbed = discord.Embed(title=f'{numberOne} {numberOperator} {numberTwo}',description=numberOne*numberTwo,color=discord.Color.random())
            numberEmbed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
            numberEmbed.set_thumbnail(url=self.client.user.avatar_url)
            await ctx.reply(embed=numberEmbed)
            return
        else:
            await ctx.reply("Invalid operator! Please choose from ( + - / * )")
            return    
        



    @commands.command(aliases=['sword','searchw'],name='searchword',description='Searches a word.')
    async def searchword(self, ctx,word=None):
        wordDict=dict(word)
        wordDictLong=wordDict.getMeanings()

        searchEmbed=discord.Embed(title=f'{word}',description=f'{wordDictLong}',color=discord.Colour.random())
        searchEmbed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
        searchEmbed.set_thumbnail(url=self.client.user.avatar_url)
        await ctx.reply(embed=searchEmbed)


    @commands.command(aliases=["randomword","randomw","rword"],name="random_word",description="Gives you a random word and a definition.")
    async def random_word(self, ctx):
        word = rword.get_random_word(hasDictionaryDef='true')
        wordDict=dict(word)
        wordDefLong = wordDict.getMeanings()
    #    wordDefSearch=re.search("['(.+?)']", wordDefLong)
    #    if wordDefSearch:
    #        wordDef=wordDefSearch.group(1)
        wordEmbed=discord.Embed(title=f'{word}',description=f'{wordDefLong}',color=discord.Colour.random())
        wordEmbed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
        wordEmbed.set_thumbnail(url=self.client.user.avatar_url)
        await ctx.reply(embed=wordEmbed)
    
    @commands.command(aliases=['rcolour','rcolor','randomcolor'],name='randomcolour',description='Gives you a random colour.')
    async def randomcolour(self, ctx):
        colour=discord.Color.random()
        colourEmbed=discord.Embed(title=colour,description='The colour is the colour of this embed.',color=colour)
        colourEmbed.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url
            )
        colourEmbed.set_thumbnail(url=self.client.user.avatar_url)
        await ctx.reply(embed=colourEmbed)

        

    #@commands.command()
    #async def cum(self, ctx):
    #    await ctx.reply("no im not adding this command this is getting removed after.")

    @commands.command(aliases=['reportbug', 'bug', 'error'],name='bug_report',description='Reports a bug.')
    async def bug_report(self, ctx, *, message=None):
        if message == None:
            def check(ms):
                return ms.channel == ctx.message.channel and ms.author == ctx.message.author
            bugMessage = await ctx.reply("What's the bug?")
            OtherMessage = await self.client.wait_for('message', check=check)
            message = OtherMessage.content
            await bugMessage.delete()
            await OtherMessage.delete()

        duzo = await self.client.fetch_user(ownerID)
        duzoChannel = self.client.get_channel(899683973356204126)
        duzoBug = discord.Embed(title='New Bug:',color=discord.Colour.random())
        duzoBug.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
        duzoBug.add_field(name='Bug:',value=message)
        duzoBug.add_field(name='Reported By:',value=f'<@!{ctx.message.author.id}>')
        await duzo.send(embed=duzoBug)
        await duzoChannel.send(embed=duzoBug)

        confirmEmbed = discord.Embed(title='Bug Recieved.',color=discord.Colour.random())
        confirmEmbed.add_field(name='Bug:',value=message)
        confirmEmbed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
        await ctx.message.author.send(embed=confirmEmbed) 

    @commands.command(aliases=['suggest', 'suggestion'],name='idea', description='give me ideas')
    async def idea(self, ctx, *, message=None):
        if message == None:
            def check(ms):
                return ms.channel == ctx.message.channel and ms.author == ctx.message.author
            ideaMessage = await ctx.reply("What's your idea?")
            OtherMessage = await self.client.wait_for('message', check=check)
            message = OtherMessage.content
            await ideaMessage.delete()
            await OtherMessage.delete()

        with open('json/data.json','r') as f:
            ideaID = json.load(f)
        
        IDNumber = random.randint(1,1000000)
        ideaID[f'{IDNumber}'] = ctx.message.author.id


        duzo = await self.client.fetch_user(ownerID)
        duzoChannel = self.client.get_channel(899683961117237268)
        duzoIdea = discord.Embed(title='New Idea:',color=discord.Colour.random())
        duzoIdea.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
        duzoIdea.add_field(name='Idea:',value=f'{message}')
        duzoIdea.add_field(name='Author:',value=f'<@!{ctx.message.author.id}>')
        duzoIdea.set_footer(text=f"ID: {IDNumber}")
        await duzo.send(embed=duzoIdea)
        await duzoChannel.send(embed=duzoIdea)

        confirmEmbed = discord.Embed(title='Idea Recieved.',color=discord.Colour.random())
        confirmEmbed.add_field(name='Your Idea:',value=message)
        confirmEmbed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar_url)
        confirmEmbed.set_footer(text=f'ID: {IDNumber}')
        await ctx.message.author.send(embed=confirmEmbed)        
    
        with open('json/data.json','w') as f:
            json.dump(ideaID, f, indent=4)

    
    @commands.command(aliases=['welcomeoption','woption'],name='welcome_option', description='Turn welcome messages on and off.')
    @has_permissions(manage_channels=True)
    async def welcome_option(self, ctx,welcomeChoice=None,welcomeChannel=None):
        def check(ms):
            return ms.channel == ctx.message.channel and ms.author == ctx.message.author
        with open('json/data.json', 'r') as f:
            welcome = json.load(f)
        

        if welcomeChoice==None:
            msg = await ctx.reply("Do you want it to be on or off?")
            Msg = await self.client.wait_for('message', check=check)
            welcomeChoice = Msg.content.upper()
            await msg.delete()
            await Msg.delete()


        idGuild = str(ctx.guild.id)

        if welcomeChoice == "ON":
            welcomeChoice = True
        elif welcomeChoice == "OFF":
            welcomeChoice = False
            return
        else:
            msg = await ctx.reply("Invalid choice, please choose on or off")
            await msg.delete()
            return

        if welcomeChannel==None:
            msg = await ctx.reply("What is the channel you want the message to be sent in?")
            ChannelMsg = await self.client.wait_for('message',check=check)
            welcomeChannel = await commands.TextChannelConverter().convert(ctx, ChannelMsg.content)
            await msg.delete()
            await ChannelMsg.delete()

        welcomeChannelID = welcomeChannel.id


        welcome[f"{idGuild} welcome"] = welcomeChoice
        welcome[f"{idGuild} welcomeChannel"] = welcomeChannelID

        msg = await ctx.reply("Done.")
        await msg.delete()

        with open('json/data.json', 'w') as f:
            json.dump(welcome, f , indent=4)

    @commands.command(aliases=['leaveoption','loption'],name='leave_option', description='Turn leave messages on and off.')
    @has_permissions(manage_channels=True)
    async def leave_option(self, ctx,leaveChoice=None,leaveChannel=None):
        def check(ms):
            return ms.channel == ctx.message.channel and ms.author == ctx.message.author
        with open('json/data.json', 'r') as f:
            leave = json.load(f)
        

        idGuild = str(ctx.guild.id)
        if leaveChoice==None:
            msg = await ctx.reply("Do you want it to be on or off?")
            Msg = await self.client.wait_for('message', check=check)
            leaveChoice = Msg.content.upper()
            await msg.delete()
            await Msg.delete()

        if leaveChoice == "ON":
            leaveChoice = True
        elif leaveChoice == "OFF":
            leaveChoice = False
            return
        else:
            msg = await ctx.reply("Invalid choice, please choose on or off")
            await msg.delete()
            return

        if leaveChannel==None:
            msg = await ctx.reply("What is the channel you want the message to be sent in?")
            Msg = await self.client.wait_for('message',check=check)
            leaveChannel = await commands.TextChannelConverter().convert(ctx, Msg.content)
            await msg.delete()
            await Msg.delete()

        leaveChannelID = leaveChannel.id


        leave[f"{idGuild} leave"] = leaveChoice
        leave[f"{idGuild} leaveChannel"] = leaveChannelID

        msg = await ctx.reply("Done.")
        await msg.delete()

        with open('json/data.json', 'w') as f:
            json.dump(leave, f , indent=4)


    @commands.command(aliases=['changeprefix'],name='prefix',description='Changes the bots prefix.')
    @has_permissions(manage_channels=True)
    async def prefix(self, ctx):

    
        def check(ms):
            return ms.channel == ctx.message.channel and ms.author == ctx.message.author
        #await ctx.channel.purge(limit=1)
        with open('json/data.json', 'r') as f:
            prefixes = json.load(f)

        msgRequest = await ctx.reply("What is the new prefix?")
        msg1 = await self.client.wait_for('message', check=check)
        await msgRequest.delete()
        await msg1.delete()
        prefixList = []
        prefixList.append(msg1.content)
        prefixList.append(f"<@!{self.client.user.id}> ")
        prefixLoop = True
        while prefixLoop == True:
            msgRequest = await ctx.reply("Would you like to add another prefix?")
            msg2 = await self.client.wait_for('message', check=check)
            await msgRequest.delete()
            await msg2.delete()
            if msg2.content.upper() == "YES":
                msgRequest = await ctx.reply("What is the extra prefix?")
                msg3 = await self.client.wait_for('message',check=check)
                await msgRequest.delete()
                await msg3.delete()
                prefixList.append(msg3.content)
            elif msg2.content.upper() == "NO":
                prefixLoop = False
            else:
                await ctx.reply("Invalid choice please choose between Yes or No.")

        guildID = str(ctx.guild.id)
        prefixes[f"{guildID} prefix"] = prefixList

        with open('json/data.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
        await ctx.reply(f'Changed the Prefixes to **{prefixList}**')
     
    @commands.command(name='help',description='This command.',aliases=['commands','command'],usage='cog')
    async def help(self,ctx,cog='all'):

        help_embed = discord.Embed(title='Help',color=discord.Colour.random())
        help_embed.set_thumbnail(url=self.client.user.avatar_url)
        help_embed.set_footer(text=f'Requested by {ctx.message.author.name}',icon_url=ctx.message.author.avatar_url)
        
        cogs = [c for c in self.client.cogs.keys()]

        if cog == 'all':
            values = ""
            for cog in cogs:
                values = values + f"**{cog}**\n"
            pass
            help_embed.add_field(name='Cogs',value=values,inline=True)
        else:
            lower_cogs = [c.lower() for c in cogs]

            if cog.lower() in lower_cogs:

                commands_list = self.client.get_cog(cogs[ lower_cogs.index(cog.lower()) ]).get_commands()
                help_text=''

                for command in commands_list:
                    help_text+= f'`{command.name}` - {command.description}\n'
                help_embed.description = help_text
            else:
                await ctx.reply('Invalid cog specified.\nUse `help` command to list all cogs.')
                return


        await ctx.reply(embed=help_embed)
        
        return

def setup(client):
    client.add_cog(Other(client))