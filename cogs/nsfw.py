import discord
from discord.ext import commands
from discord.ext.commands.core import is_nsfw
import random
import requests
import praw
import json 

def embed_set_author(ctx, embed: discord.Embed):
    return embed.set_author(name=ctx.message.author.display_name,icon_url=ctx.message.author.display_avatar.url)

# Getting items from config.json
with open('config.json','r') as cf:
    config = json.load(cf)

ownerID = config['ownerID']
redditID = config['redditID']
redditSecret = config['redditSecret']
redditAgent = config['redditAgent']
reddit = praw.Reddit(client_id=redditID,client_secret=redditSecret,user_agent=redditAgent,check_for_async=False)

class NSFW(commands.Cog):

    def __init__(self, client):
        self.client = client
        
    @commands.command(name='lewdneko',description='Sends a lewd neko (wtf is a neko)')
    @is_nsfw()
    async def _lewdneko(self, ctx):
        await ctx.trigger_typing()
        url = 'https://nekos.life/api/v2/img/nsfw_neko_gif'
        responseApi = requests.get(url).json()
        nekoImagery = responseApi['url']

        embed = discord.Embed(title='Neko',description=nekoImagery,color=0xC3B1E1,type='image')
        embed.set_footer(text=f'API: {url}')
        embed.set_image(url=nekoImagery)
        embed_set_author(ctx, embed)
        await ctx.reply(embed=embed)

    @commands.command(aliases=['sex'],name='fuck', description='Lets you do that with a user you @')
    @is_nsfw()
    async def fuck(self, ctx, user: commands.MemberConverter):
        await ctx.trigger_typing()
        url = 'https://api.tenor.com/v1/random?key=LIVDSRZULELA&q=anime+sex&limit=1'
        responseApi = requests.get(url).json()
        gif = responseApi['results'][0]['media'][0]['gif']['url']

        embed = discord.Embed(title=f'{ctx.author.display_name} fuck {user.display_name}',description=f'{ctx.author.mention} fucks {user.mention}',color=0xF8C8DC,type='gifv')
        embed.set_image(url=gif)
        embed.set_author(name=ctx.message.author.display_name,icon_url=ctx.message.author.display_avatar.url)
        await ctx.reply(embed=embed)


    @commands.command(aliases=['nsfwtod'],name='nsfwtruthordare',description='Play nsfw truth or dare')
    @is_nsfw()
    async def _tod(self, ctx):
        await ctx.trigger_typing()
        url = 'https://gist.githubusercontent.com/deepakshrma/9498a19a3ed460fc662c536d138c29b1/raw/f29d323b9b3f0a82f66ed58c7117fb9b599fb8d5/truth-n-dare.json'
        responseApi = requests.get(url).json()
        nsfw_list = [
            item
            for item in responseApi
            if int(item['level']) > 3
        ]
        choice = random.choice(nsfw_list)
        choiceID = choice['id']
        choiceLevel = choice['level']
        choiceType = choice['type']
        choiceSum = choice['summary']


        embed = discord.Embed(title=choiceType,description=choiceSum,color=discord.Colour.random())
        embed.set_author(name=ctx.message.author.display_name,icon_url=ctx.message.author.display_avatar.url)
        embed.set_thumbnail(url=self.client.user.display_avatar.url)
        embed.set_footer(text=f'ID: {choiceID} | Level: {choiceLevel}')
        await ctx.reply(embed=embed)


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

        tagMessage = tagMessage[:1024]

        nsfw_extension = nsfwFile[len(nsfwFile) - 3 :].lower()
        if nsfw_extension == "mp4":
            nsfwPreview = chosenKey["preview_url"]
            nsfwEmbed = discord.Embed(title="NSFW",description=f"[Click me for the video!]({nsfwFile})",color=discord.Colour.random(),type='image')
            nsfwEmbed.set_image(url=nsfwPreview)
            nsfwEmbed.set_author(name=ctx.message.author.display_name,icon_url=ctx.message.author.display_avatar.url)
            nsfwEmbed.add_field(name='Tags:',value=tagMessage)
            nsfwEmbed.set_footer(text=f"ID: {nsfwID} | API by api.rule34.xxx")
            await ctx.reply(embed=nsfwEmbed)
            await ctx.reply(nsfwFile)
            return
        if nsfw_extension == "jpg" or nsfw_extension == "peg" or nsfw_extension == "png" or nsfw_extension == "gif":
            nsfwEmbed = discord.Embed(title="NSFW",description=f'[{request}]({nsfwFile})',color=discord.Colour.random(),type='image')
            nsfwEmbed.set_image(url=nsfwFile)
            nsfwEmbed.set_author(name=ctx.message.author.display_name,icon_url=ctx.message.author.display_avatar.url)
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
            sbEmbed.set_author(name=ctx.message.author.display_name,icon_url=ctx.message.author.display_avatar.url)
            await ctx.reply(embed=sbEmbed)
            return
        sbEmbed = discord.Embed(title=sb_random.display_name,description=f'[{submission.title}]({submission.url})',color=discord.Colour.random())
        sbEmbed.set_author(name=ctx.message.author.display_name,icon_url=ctx.message.author.display_avatar.url)
        await ctx.reply(embed=sbEmbed)

def setup(client):
    client.add_cog(NSFW(client))