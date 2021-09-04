import discord
from discord.ext import commands
from discord.ext.commands.core import has_permissions
import json

class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='mute',description='Mutes the user you ping.')
    @has_permissions(manage_roles=True)
    async def mute(self,ctx, user: commands.MemberConverter=None):
        if user == None:
            await ctx.send("Please provide a user!")
            return
        await ctx.message.delete()
        guild = ctx.message.guild 
        roles = await guild.fetch_roles()
        channels = await guild.fetch_channels()
        for discord.Role in roles:
            if discord.Role.name.upper() == "MUTED":
                await user.add_roles(discord.Role)
                muteEmbed = discord.Embed(title='Mute',description=f'Muted {user.mention}',color=discord.Colour.random())
                muteEmbed.set_thumbnail(url=self.client.user.avatar_url)
                muteEmbed.set_author(
                        name=ctx.message.author.name,
                        icon_url=ctx.message.author.avatar_url
                    )
                await ctx.send(embed=muteEmbed)
                return
        permissions=discord.Permissions(permissions=0,send_messages=False)
        role = await guild.create_role(name="Muted",reason="Muted role did not exist.",permissions=permissions)
        msg = await ctx.send("Please wait while I setup the Muted role.")
        for discord.TextChannel in channels:
            await discord.TextChannel.set_permissions(role,send_messages=False)
        await msg.delete()
        await user.add_roles(role)
        muteEmbed = discord.Embed(title='Mute',description=f'Muted {user.mention}',color=discord.Colour.random())
        muteEmbed.set_thumbnail(url=self.client.user.avatar_url)
        muteEmbed.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url
        )
        await ctx.send(embed=muteEmbed)
    
    @commands.command(name='unmute',description='Unmutes the user you ping.')
    @has_permissions(manage_roles=True)
    async def unmute(self,ctx,user: commands.MemberConverter=None):
        if user == None:
            await ctx.send("Please provide a user!")
            return
        await ctx.message.delete()
        roles = user.roles
        for discord.Role in roles:
            if discord.Role.name.upper() == "MUTED":
                await user.remove_roles(discord.Role,reason="Unmuting the user.")
                unmuteEmbed = discord.Embed(title='Unmute',description=f'Unmuted {user.mention}',color=discord.Colour.random())
                unmuteEmbed.set_thumbnail(url=self.client.user.avatar_url)
                unmuteEmbed.set_author(
                        name=ctx.message.author.name,
                        icon_url=ctx.message.author.avatar_url
                    )
                await ctx.send(embed=unmuteEmbed)
                return
        await ctx.send(f"{user.mention} is not muted!")

    @commands.command(aliases=['lockchannel','lockc','clock','lc'],name='channellock',description='Locks the channel.')
    @has_permissions(manage_channels=True)
    async def channellock(self, ctx, channel: discord.TextChannel=None):
        await ctx.message.delete()
        
        #This bit of code came from https://stackoverflow.com/questions/62706813/how-do-i-lock-a-channel-that-is-mentioned-discord-py 
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send('Channel locked.')

    @commands.command(aliases=['unlockchannel','unlockc','cunlock','ulc'],name='channelunlock',description='Unlocks a channel.')
    @has_permissions(manage_channels=True)
    async def channelunlock(self,ctx, channel: discord.TextChannel=None):
        await ctx.message.delete()
        
        #This bit of code came from https://stackoverflow.com/questions/62706813/how-do-i-lock-a-channel-that-is-mentioned-discord-py 
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send('Channel unlocked.')

    @commands.command(aliases=["toggletickets","toggleticket","ticketstoggle"],name='tickettoggle',description='Toggles tickets.')
    @has_permissions(manage_channels=True)
    async def tickettoggle(self,ctx):
        with open("json/data.json","r") as f:
            ticketToggle = json.load(f)
        

        if f"{ctx.message.guild.id} Ticket" not in ticketToggle:
            ticketToggle[f"{ctx.message.guild.id} Ticket"] = False
            with open("json/data.json","w") as f:
                json.dump(ticketToggle, f,indent=4)
            return await ctx.send("Tickets are now off.")
        elif ticketToggle[f"{ctx.message.guild.id} Ticket"] == True:
            ticketToggle[f"{ctx.message.guild.id} Ticket"] = False
            with open("json/data.json","w") as f:
                json.dump(ticketToggle,f,indent=4)
            return await ctx.send("Tickets are now off.")
        elif ticketToggle[f"{ctx.message.guild.id} Ticket"] == False:
            ticketToggle[f"{ctx.message.guild.id} Ticket"] = True
            with open("json/data.json","w") as f:
                json.dump(ticketToggle,f,indent=4)
            return await ctx.send("Tickets are now on.")
        

    @commands.command(aliases=['ticket_create','create_ticket','createticket'],name='ticketcreate',description='Creates a ticket.')
    #@has_permissions(administrator=True)
    async def ticketcreate(self, ctx):
        with open("json/data.json","r") as f:
            ticketCheck = json.load(f)

        if f"{ctx.message.guild.id} Ticket" not in ticketCheck:
            ticketCheck[f"{ctx.message.guild.id} Ticket"] = False
            return await ctx.send("Tickets are off. (test)")
        elif ticketCheck[f"{ctx.message.guild.id} Ticket"] == False:
            return await ctx.send("Tickets are off.")

        await ctx.message.delete()

        def check(reaction, user):  
            return str(reaction) == "🔒" and user == ctx.message.author

        guild = ctx.message.guild
        overwrites={
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
            ctx.message.author: discord.PermissionOverwrite(manage_channels=True),
            ctx.message.author: discord.PermissionOverwrite(read_messages=True),
        }
        channel = await guild.create_text_channel(f'ticket-{ctx.author}', overwrites=overwrites, reason="ticket system")

        pingMessage = await channel.send(f"<@!{ctx.message.author.id}>")
        await pingMessage.delete()

        message = await channel.send("React with :lock: to close the ticket.")
        await message.add_reaction("🔒")
        await ctx.message.delete()

        await self.client.wait_for("reaction_add", check=check)
        await channel.set_permissions(ctx.message.author,reason="Closing the ticket.", send_messages=False)
        await channel.send("Ticket Closed.")


    @commands.command(aliases=['comeback', 'revive', 'oops', 'pardon'], permissions=["ban_members"], name='unban', description='Unbans a banned user')
    @has_permissions(ban_members=True)    
    async def unban(self, ctx, *, user=None):
        

        try:
            user = await commands.converter.UserConverter().convert(ctx, user)
        except:
            await ctx.send("User not found!")
            return

        try:
            bans = tuple(ban_entry.user for ban_entry in await ctx.guild.bans())
            if user in bans:
                await ctx.guild.unban(user)
            else:
                await ctx.send("User not banned!")
                return
        except discord.Forbidden:
            await ctx.send("I do not have permission to unban!")
            return

        except:
            await ctx.send("Unbanning failed!")
            return
    
        await ctx.message.delete()
        unbanEmbed = discord.Embed(title='Unban',description=f'{user.mention} has been unbanned.',color=discord.Colour.random())
        unbanEmbed.set_thumbnail(url=self.client.user.avatar_url)
        unbanEmbed.set_author(
                name=ctx.message.author.name,
                icon_url=ctx.message.author.avatar_url
            )
        await ctx.send(embed=unbanEmbed)


    
    @commands.command(aliases=['goawayforever'], name='ban', description='Bans a user')
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member : commands.MemberConverter, *, reason=None):
        await ctx.message.delete()
        
        if member.id == 509436097835827210:
            await ctx.send(f"Unable to ban **{member.name}**: Person too epic")
            return
        if member.id == 327807253052653569:
            await ctx.send(f"Unable to ban **{member.name}**: Person too epic")
            return
        if member.id == 578844127878184961:
            await ctx.send(f"Unable to ban **{member.name}**: Person too epic")
            return
        await member.ban(reason=reason)
        banEmbed = discord.Embed(title='Ban',description=f'**{member.display_name}** has been banned for **{reason}**', color=discord.Colour.random())
        banEmbed.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url
        )
        banEmbed.set_thumbnail(url=self.client.user.avatar_url)
        await ctx.send(embed=banEmbed)

    @commands.command(name='slowmode', description='Adds slowmode to a channel, limit is 21600')
    @has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int):
        await ctx.message.delete()
        
        await ctx.channel.edit(slowmode_delay=seconds)
        slowEmbed = discord.Embed(title='Slowmode',description=f'Slowmode is now on **{seconds}** seconds.',color=discord.Colour.random())
        slowEmbed.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url
        )
        slowEmbed.set_thumbnail(url=self.client.user.avatar_url)
        await ctx.send(embed=slowEmbed)

    @commands.command(aliases=['goaway'], name='kick', description='Kicks a user')
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member : commands.MemberConverter, *, reason=None):
        
        await ctx.message.delete()
        if member.id == 509436097835827210:
            await ctx.send(f"Unable to ban **{member.name}**: Person too epic")
            return
        if member.id == 327807253052653569:
            await ctx.send(f"Unable to ban **{member.name}**: Person too epic")
            return
        if member.id == 578844127878184961:
            await ctx.send(f"Unable to ban **{member.name}**: Person too epic")
            return
        await member.kick(reason=reason)
        kickEmbed = discord.Embed(title='Kick',description=f'**{member.name}** has been kicked for **{reason}**',color=discord.Colour.random())
        kickEmbed.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url
        )
        kickEmbed.set_thumbnail(url=self.client.user.avatar_url)
        await ctx.send(embed=kickEmbed)

    @commands.command(name='clear', description='Clears the amount of messages you want')
    @has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=2):
        await ctx.channel.purge(limit=amount)

def setup(client):
    client.add_cog(Moderation(client))