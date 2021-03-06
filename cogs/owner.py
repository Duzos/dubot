import discord
from discord.ext import commands
from discord.ext.commands.core import is_owner
import json
import os
import sys
import random
import asyncio

# Getting items from the config
with open('config.json','r') as cf:
    config = json.load(cf)
prefix = config['prefix']

# change this with your own ids
allowed_owner_ids = [327807253052653569,578844127878184961,509436097835827210,597102599694712844]
def allowed_owner(ctx):
    return ctx.message.author.id in allowed_owner_ids

def restart_bot():
    os.execv(sys.executable, ['python'] + sys.argv)

class owner(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Owner only commands. 

    @commands.command(name='perms_check',description='Run this command to check if you have the perms to run some other commands, if it fails you dont if it doesnt fail you do')
    @commands.check(allowed_owner)
    async def _perms_check(self, ctx):
        await ctx.reply('yo u got perms')
        await ctx.reply(allowed_owner_ids)

    @commands.command(name='list_dms_id')
    @commands.check(allowed_owner)
    async def _list_dms_id(self, ctx, member):   
        member = await self.client.fetch_user(member)
        messages = await member.dm_channel.history(limit=99999).flatten()
        f = open('./list_dms.txt','w')
        msg = await ctx.reply('I will edit this message with the embeds')
        for message in messages:
            f.write(f'{message.id} | {message.author.name}: {message.content}\n')
        f.close()
        await ctx.reply(file=discord.File('./list_dms.txt'))
        for message in messages:
            for embed in message.embeds:
                await msg.edit(embed=embed)
                await asyncio.sleep(1.5)


    @commands.command(name='list_dms')
    @commands.check(allowed_owner)
    async def _list_dms(self, ctx, member: commands.MemberConverter):   
        await member.create_dm()
        messages = await member.dm_channel.history(limit=99999).flatten()
        f = open('./list_dms.txt','w')
        msg = await ctx.reply('I will edit this message with the embeds')
        for message in messages:
            f.write(f'{message.id} | {message.author.name}: {message.content}\n')
        f.close()
        await ctx.reply(file=discord.File('./list_dms.txt'))
        for message in messages:
            for embed in message.embeds:
                await msg.edit(embed=embed)
                await asyncio.sleep(1.5)


    @commands.command(name='leave_server')
    @is_owner()
    async def _leave_server(self, ctx, server: commands.GuildConverter):
        leave_channel = random.choice(server.channels)
        await leave_channel.send("im leaving this server bruh")
        await server.leave()
        await ctx.send('left that dumb server')

    @commands.command(name='datareset',description='Resets the data for a specific server.')
    @is_owner()
    async def _datareset(self, ctx):
        def check(ms):
            return ms.channel == ctx.message.channel and ms.author == ctx.message.author

        await ctx.send("are you sure.")
        msg = await self.client.wait_for('message', check=check)
        if msg.content.upper() == "NO":
            await ctx.send("Cancelling.")
            return
        elif msg.content.upper() == "YES":
            await ctx.send("Proceeding.")
        else:
            await ctx.send("Invalid response.")
            return
    
        message = ""
        for guild in self.client.guilds:
            message += f"{guild.name}: {guild.id}\n"
        await ctx.send(message)
        await ctx.send("Please choose a server to reset in ID form")
        msg = await self.client.wait_for('message', check=check)
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
    
    @commands.command(name='dataresetall',description='The command to reset all the data.')
    @is_owner()
    async def _dataresetall(self, ctx):    
        def check(ms):
            return ms.channel == ctx.message.channel and ms.author == ctx.message.author

        await ctx.send("are you sure.")
        msg = await self.client.wait_for('message', check=check)
        if msg.content == "no":
            await ctx.send("Cancelling.")
            return
        elif msg.content == "yes":
            await ctx.send("Proceeding.")
        else:
            await ctx.send("Invalid response.")
            return

        for guild in self.client.guilds:
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
        
    @commands.command()
    @commands.is_owner()
    async def idle(self, ctx, *, text):
        await self.client.change_presence(status=discord.Status.idle, activity=discord.Game(f"{text}"))
        await ctx.send(f"Changed status to **idle** with a description of **{text}**")

    @commands.command()
    @commands.is_owner()
    async def online(self, ctx, *, text):
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game(f"{text}"))
        await ctx.send(f"Changed status to **online** with a description of **{text}**")

    @commands.command()
    @commands.is_owner()
    async def offline(self, ctx, *, text):
        await self.client.change_presence(status=discord.Status.offline, activity=discord.Game(f"{text}"))
        await ctx.send(f"Changed status to **offline** with a description of **{text}**")

    @commands.command()
    @commands.is_owner()
    async def dnd(self, ctx, *, text):
        await self.client.change_presence(status=discord.Status.dnd, activity=discord.Game(f"{text}"))
        await ctx.send(f"Changed status to **dnd** with a description of **{text}**")

    @commands.command()
    @commands.is_owner()
    async def pausebot(self, ctx):
        await ctx.send("Bot Paused")
        input("Bot Paused")
        await ctx.send("Unpaused")
        print("Unpaused")

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.send("Goodbye.")
        await self.client.change_presence(activity=discord.Game("Shutting Down."))
        await self.client.change_presence(status=discord.Status.invisible)
        await self.client.close()
        await ctx.send("Unable to shutdown.")


    @commands.command()
    @commands.check(allowed_owner)
    async def restart(self, ctx):
        await self.client.change_presence(activity=discord.Game("Restarting."))
        await self.client.change_presence(status=discord.Status.invisible)
        await ctx.send("Restarting.")
        restart_bot()


    @commands.command()
    @commands.check(allowed_owner)
    async def load(self, ctx, extension):
        self.client.load_extension(f'cogs.{extension}')
        await ctx.send("Successfully loaded")

    @commands.command()
    @commands.check(allowed_owner)
    async def unload(self, ctx, extension):
        self.client.unload_extension(f'cogs.{extension}')
        await ctx.send("Successfully unloaded")

    @commands.command()
    @commands.check(allowed_owner)
    async def reload(self, ctx, extension):
        self.client.unload_extension(f'cogs.{extension}')
        self.client.load_extension(f'cogs.{extension}')
        await ctx.send("Reload complete.")

    @commands.command()
    @commands.check(allowed_owner)
    async def WIPLoad(self, ctx, extension):
        self.client.load_extension(f'WIP.{extension}')
        await ctx.send("Successfully Loaded WIP cog.")

    @commands.command()
    @commands.check(allowed_owner)
    async def WIPunload(self, ctx, extension):
        self.client.unload_extension(f'WIP.{extension}')
        await ctx.send("Successfully unloaded WIP cog.")

    @commands.command()
    @commands.check(allowed_owner)
    async def WIPreload(self, ctx,extension):
        self.client.unload_extension(f'WIP.{extension}')
        self.client.load_extension(f'WIP.{extension}')
        await ctx.send("WIP reload complete.")

    @commands.command()
    @is_owner()
    async def block(self, ctx,user: commands.MemberConverter=None):
        if user == None:
            await ctx.send("Please provide a user!")
            return

        with open('json/blocked.json','r') as f:
            blockList = json.load(f)
    
        blockList[f"{user.id}"] = user.name

        with open('json/blocked.json','w') as f:
            json.dump(blockList, f, indent=4)
        await ctx.send(f"Blocked {user.name}")

    @commands.command()
    @is_owner()
    async def unblock(self, ctx,user: commands.MemberConverter=None):
        if user == None:
            await ctx.send("Please provide a user!")
            return

        with open('json/blocked.json','r') as f:
            blockList = json.load(f)
    
        blockList.pop(f"{user.id}")

        with open('json/blocked.json','w') as f:
            json.dump(blockList, f, indent=4)
        await ctx.send(f"Unblocked {user.name}")

    @commands.command()
    @is_owner()
    async def blocked(self, ctx):
        with open('json/blocked.json','r') as f:
            blockList = json.load(f)
    
        await ctx.send(blockList)

        with open('json/blocked.json','w') as f:
            json.dump(blockList, f, indent=4)

    @commands.command(aliases=['iapprove','ia','iaccept'])
    @commands.is_owner()
    async def ideaApprove(self, ctx, idea=None):
        if idea==None:
            return
        with open('json/data.json','r') as f:
            approve = json.load(f)

        approveEmbed = discord.Embed(title='Hooray!',description='Your idea has been approved!',color=discord.Colour.random())
        approveEmbed.set_footer(text=f'Idea ID: {idea}')

        approvePerson = await self.client.fetch_user(approve[idea])
        await approvePerson.send(embed=approveEmbed)
        await ctx.send(f"Idea {idea} approved.")
        approve.pop(idea)
        with open("json/data.json",'w') as f:
            json.dump(approve, f, indent=4)

    @commands.command(aliases=['ideny','id'])
    @commands.is_owner()
    async def ideaDeny(self, ctx, idea=None):
        if idea==None:
            return
        with open('json/data.json','r') as f:
            deny = json.load(f)

        denyEmbed = discord.Embed(title='Sorry.',description='Your idea has been denied.',color=discord.Colour.random())
        denyEmbed.set_footer(text=f'Idea ID: {idea}')

        denyPerson = await self.client.fetch_user(deny[idea])
        await denyPerson.send(embed=denyEmbed)
        await ctx.send(f"Idea {idea} denied.")
        deny.pop(idea) 
        with open("json/data.json",'w') as f:
            json.dump(deny, f, indent=4)

    # Other commands.
    @commands.command()
    async def rawavatar(self, ctx, user: discord.Member):
        await ctx.send(user.display_avatar.url)
        await ctx.send(user.avatar.url)
        await ctx.send(user.banner)

    @commands.command()
    async def d(self, ctx):
        await ctx.send("d <@!597102599694712844>")

    @commands.command(name='kys')
    async def _kys(self, ctx, user: commands.MemberConverter=None):
        user = user or ctx.message.author
        await ctx.reply(f"{user.mention} should commit death")

    @commands.command(name='listservers')
    @is_owner()
    async def _listservers(self, ctx):
        await ctx.send("Found {} servers\nServer List:".format(len(self.client.guilds)))
    
        message = ""
        for guild in self.client.guilds:
            message = message + f"{guild.name} | {guild.id} | {guild.member_count} Members\n"
        await ctx.send(message)

    @commands.command(name='guild_info_owner')
    @commands.check(allowed_owner)
    async def _guild_info_owner(self, ctx, guild: commands.GuildConverter):
        date_format = "%a, %d %b %Y %I:%M %p"

        roleList = ", ".join([str(r.name) for r in guild.roles])

        ginfoEmbed = discord.Embed(title=f'Info on {guild.name}',description=f'**Description:**\n```{guild.description}```\n**Member Count:**\n```{guild.member_count}```\n**Owner:**\n```{guild.owner}```\n**Roles:**\n```{roleList}```\n**Boost Level:**\n```{guild.premium_tier}```\n**Boost Count:**\n```{guild.premium_subscription_count}```\n**ID:**\n```{guild.id}```\n**Guild Created On:**\n```{guild.created_at.strftime(date_format)}```',color=discord.Colour.random())
        ginfoEmbed.set_thumbnail(url=guild.icon)
        ginfoEmbed.set_author(name=ctx.message.author.display_name,icon_url=ctx.message.author.display_avatar.url)
        await ctx.reply(embed=ginfoEmbed)

    @commands.command(name='guild_invite_owner')
    @commands.check(allowed_owner)
    async def _guild_invite_owner(self, ctx, guild: commands.GuildConverter):      
        guildChannel = guild.text_channels[0]
        invite = await guildChannel.create_invite(unique=False)
        await ctx.send(f"Here's the invite: {invite}")
    
def setup(client):
    client.add_cog(owner(client))