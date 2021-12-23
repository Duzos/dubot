import discord
from discord.ext import commands
from discord.ext.commands.core import has_permissions, is_owner
import json


class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='antiswear',description='Automatic anti swearing system')
    @has_permissions(manage_messages=True)
    async def _antiswear(self,ctx, choice=None):
        def check(ms):
            return ms.channel == ctx.message.channel and ms.author == ctx.message.author

        if choice==None:
            await ctx.reply("What do you want to do?")
            await ctx.reply("( On, Off, Add )")
            choice = await self.client.wait_for('message', check=check)
            choice = choice.content

        with open('json/data.json','r') as f:
            jsonFile = json.load(f)

        if choice.lower() == "on":
            jsonFile[f'{ctx.message.guild.id} antiswear'] = True
            jsonFile[f'{ctx.message.guild.id} swearwords'] = ["4r5e", "5h1t", "5hit", "a55", "anal", "anus", "ar5e", "arrse", "arse", "ass", "ass-fucker", "asses", "assfucker", "assfukka", "asshole", "assholes", "asswhole", "a_s_s", "b!tch", "b00bs", "b17ch", "b1tch", "ballbag", "balls", "ballsack", "bastard", "beastial", "beastiality", "bellend", "bestial", "bestiality", "bi+ch", "biatch", "bitch", "bitcher", "bitchers", "bitches", "bitchin", "bitching", "bloody", "blow job", "blowjob", "blowjobs", "boiolas", "bollock", "bollok", "boner", "boob", "boobs", "booobs", "boooobs", "booooobs", "booooooobs", "breasts", "buceta", "bugger", "bum", "bunny fucker", "butt", "butthole", "buttmuch", "buttplug", "c0ck", "c0cksucker", "carpet muncher", "cawk", "chink", "cipa", "cl1t", "clit", "clitoris", "clits", "cnut", "cock", "cock-sucker", "cockface", "cockhead", "cockmunch", "cockmuncher", "cocks", "cocksuck", "cocksucked", "cocksucker", "cocksucking", "cocksucks", "cocksuka", "cocksukka", "cok", "cokmuncher", "coksucka", "coon", "cox", "crap", "cum", "cummer", "cumming", "cums", "cumshot", "cunilingus", "cunillingus", "cunnilingus", "cunt", "cuntlick", "cuntlicker", "cuntlicking", "cunts", "cyalis", "cyberfuc", "cyberfuck", "cyberfucked", "cyberfucker", "cyberfuckers", "cyberfucking", "d1ck", "damn", "dick", "dickhead", "dildo", "dildos", "dink", "dinks", "dirsa", "dlck", "dog-fucker", "doggin", "dogging", "donkeyribber", "doosh", "duche", "dyke", "ejaculate", "ejaculated", "ejaculates", "ejaculating", "ejaculatings", "ejaculation", "ejakulate", "f u c k", "f u c k e r", "f4nny", "fag", "fagging", "faggitt", "faggot", "faggs", "fagot", "fagots", "fags", "fanny", "fannyflaps", "fannyfucker", "fanyy", "fatass", "fcuk", "fcuker", "fcuking", "feck", "fecker", "felching", "fellate", "fellatio", "fingerfuck", "fingerfucked", "fingerfucker", "fingerfuckers", "fingerfucking", "fingerfucks", "fistfuck", "fistfucked", "fistfucker", "fistfuckers", "fistfucking", "fistfuckings", "fistfucks", "flange", "fook", "fooker", "fuck", "fucka", "fucked", "fucker", "fuckers", "fuckhead", "fuckheads", "fuckin", "fucking", "fuckings", "fuckingshitmotherfucker", "fuckme", "fucks", "fuckwhit", "fuckwit", "fudge packer", "fudgepacker", "fuk", "fuker", "fukker", "fukkin", "fuks", "fukwhit", "fukwit", "fux", "fux0r", "f_u_c_k", "gangbang", "gangbanged", "gangbangs", "gaylord", "gaysex", "goatse", "God", "god-dam", "god-damned", "goddamn", "goddamned", "hardcoresex", "hell", "heshe", "hoar", "hoare", "hoer", "homo", "hore", "horniest", "horny", "hotsex", "jack-off", "jackoff", "jap", "jerk-off", "jism", "jiz", "jizm", "jizz", "kawk", "knob", "knobead", "knobed", "knobend", "knobhead", "knobjocky", "knobjokey", "kock", "kondum", "kondums", "kum", "kummer", "kumming", "kums", "kunilingus", "l3i+ch", "l3itch", "labia", "lust", "lusting", "m0f0", "m0fo", "m45terbate", "ma5terb8", "ma5terbate", "masochist", "master-bate", "masterb8", "masterbat*", "masterbat3", "masterbate", "masterbation", "masterbations", "masturbate", "mo-fo", "mof0", "mofo", "mothafuck", "mothafucka", "mothafuckas", "mothafuckaz", "mothafucked", "mothafucker", "mothafuckers", "mothafuckin", "mothafucking", "mothafuckings", "mothafucks", "mother fucker", "motherfuck", "motherfucked", "motherfucker", "motherfuckers", "motherfuckin", "motherfucking", "motherfuckings", "motherfuckka", "motherfucks", "muff", "mutha", "muthafecker", "muthafuckker", "muther", "mutherfucker", "n1gga", "n1gger", "nazi", "nigg3r", "nigg4h", "nigga", "niggah", "niggas", "niggaz", "nigger", "niggers", "nob", "nob jokey", "nobhead", "nobjocky", "nobjokey", "numbnuts", "nutsack", "orgasim", "orgasims", "orgasm", "orgasms", "p0rn", "pawn", "pecker", "penis", "penisfucker", "phonesex", "phuck", "phuk", "phuked", "phuking", "phukked", "phukking", "phuks", "phuq", "pigfucker", "pimpis", "piss", "pissed", "pisser", "pissers", "pisses", "pissflaps", "pissin", "pissing", "pissoff", "poop", "porn", "porno", "pornography", "pornos", "prick", "pricks", "pron", "pube", "pusse", "pussi", "pussies", "pussy", "pussys", "rectum", "retard", "rimjaw", "rimming", "s hit", "s.o.b.", "sadist", "schlong", "screwing", "scroat", "scrote", "scrotum", "semen", "sex", "sh!+", "sh!t", "sh1t", "shag", "shagger", "shaggin", "shagging", "shemale", "shi+", "shit", "shitdick", "shite", "shited", "shitey", "shitfuck", "shitfull", "shithead", "shiting", "shitings", "shits", "shitted", "shitter", "shitters", "shitting", "shittings", "shitty", "skank", "slut", "sluts", "smegma", "smut", "snatch", "son-of-a-bitch", "spac", "spunk", "s_h_i_t", "t1tt1e5", "t1tties", "teets", "teez", "testical", "testicle", "tit", "titfuck", "tits", "titt", "tittie5", "tittiefucker", "titties", "tittyfuck", "tittywank", "titwank", "tosser", "turd", "tw4t", "twat", "twathead", "twatty", "twunt", "twunter", "v14gra", "v1gra", "vagina", "viagra", "vulva", "w00se", "wang", "wank", "wanker", "wanky", "whoar", "whore", "willies", "willy", "xrated", "xxx"];
            await ctx.reply("Antiswearing turned ON!")
            with open('json/data.json', 'w') as f:
                json.dump(jsonFile, f, indent=4)
            return
        if choice.lower() == "off":
            jsonFile[f'{ctx.message.guild.id} antiswear'] = False
            try:
                jsonFile[f'{ctx.message.guild.id} swearwords'].pop()
            except:
                pass
            await ctx.reply("Antiswearing turned OFF!")
            with open('json/data.json', 'w') as f:
                json.dump(jsonFile, f, indent=4)
            return
        
        if choice.lower() == "add":
            swearList = jsonFile[f'{ctx.message.guild.id} swearwords']
            swearLoop = True
            while swearLoop == True:
                msgRequest = await ctx.reply("Would you like to add another swear?")
                msg2 = await self.client.wait_for('message', check=check)
                if msg2.content.upper() == "YES":
                    msgRequest = await ctx.reply("What is the extra swear?")
                    msg3 = await self.client.wait_for('message',check=check)
                    if msg3.content in swearList:
                        await ctx.reply("This swear is already in the list!")
                        return
                    swearList.append(msg3.content)
                elif msg2.content.upper() == "NO":
                    jsonFile[f'{ctx.message.guild.id} swearwords'] = swearList
                    with open('json/data.json', 'w') as f:
                        json.dump(jsonFile, f, indent=4)
                    swearLoop = False
                else:
                    await ctx.reply("Invalid choice please choose between yes or no.")
        

    @commands.command(aliases=['lockchannel','lockc','clock','lc'],name='channellock',description='Locks the channel.')
    @has_permissions(manage_channels=True)
    async def channellock(self, ctx, channel: discord.TextChannel=None):
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass
        
        #This bit of code came from https://stackoverflow.com/questions/62706813/how-do-i-lock-a-channel-that-is-mentioned-discord-py 
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        try:
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        except discord.Forbidden:
            botPermEmbed = discord.Embed(title='ERROR',description=f'{self.client.user.name} is missing the required permission(s) to run this command.',color=0x992D22)
            botPermEmbed.set_author(
                name=ctx.message.author.display_name,
                icon_url=ctx.message.author.display_avatar.url
            )
            botPermEmbed.set_thumbnail(url=self.client.user.display_avatar.url)
            try:
                await ctx.reply(embed=botPermEmbed)
            except:
                await ctx.send(embed=botPermEmbed)
            return
        try:
            await ctx.reply('Channel locked.')
        except:
            await ctx.send('Channel locked.')

    @commands.command(aliases=['unlockchannel','unlockc','cunlock','ulc'],name='channelunlock',description='Unlocks a channel.')
    @has_permissions(manage_channels=True)
    async def channelunlock(self,ctx, channel: discord.TextChannel=None):
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass
        
        #This bit of code came from https://stackoverflow.com/questions/62706813/how-do-i-lock-a-channel-that-is-mentioned-discord-py 
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = True
        try:
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        except discord.Forbidden:
            botPermEmbed = discord.Embed(title='ERROR',description=f'{self.client.user.name} is missing the required permission(s) to run this command.',color=0x992D22)
            botPermEmbed.set_author(
                name=ctx.message.author.display_name,
                icon_url=ctx.message.author.display_avatar.url
            )
            botPermEmbed.set_thumbnail(url=self.client.user.display_avatar.url)
            try:
                await ctx.reply(embed=botPermEmbed)
            except:
                await ctx.send(embed=botPermEmbed)
            return
        try:
            await ctx.reply('Channel unlocked.')
        except:
            await ctx.send('Channel unlocked.')

    @commands.command(name='mute',description='Mutes the user you ping.')
    @has_permissions(manage_roles=True)
    async def mute(self,ctx, user: commands.MemberConverter=None,*,reason=None):
        if user == None:
            await ctx.reply("Please provide a user!")
            return
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass
        guild = ctx.message.guild 
        roles = await guild.fetch_roles()
        channels = await guild.fetch_channels()
        for discord.Role in roles:
            if discord.Role.name.upper() == "MUTED":
                try:
                    await user.add_roles(discord.Role)
                except discord.Forbidden:
                    botPermEmbed = discord.Embed(title='ERROR',description=f'{self.client.user.name} is missing the required permission(s) to run this command.',color=0x992D22)
                    botPermEmbed.set_author(
                        name=ctx.message.author.display_name,
                        icon_url=ctx.message.author.display_avatar.url
                    )
                    botPermEmbed.set_thumbnail(url=self.client.user.display_avatar.url)
                    try:
                        await ctx.reply(embed=botPermEmbed)
                    except:
                        await ctx.send(embed=botPermEmbed)
                    return
                muteEmbed = discord.Embed(title='Mute',description=f'Muted {user.mention}.',color=discord.Colour.random())
                muteEmbed.set_thumbnail(url=user.display_avatar.url)
                muteEmbed.set_author(
                        name=ctx.message.author.display_name,
                        icon_url=ctx.message.author.display_avatar.url
                    )
                muteEmbed.add_field(name='Reason:',value=reason)
                try:
                    await ctx.reply(embed=muteEmbed)
                except:
                    await ctx.send(embed=muteEmbed)
                muteEmbed = discord.Embed(title='Mute',description=f'Muted {user.mention}.',color=discord.Colour.random())
                muteEmbed.set_thumbnail(url=ctx.guild.icon_url)
                muteEmbed.set_author(
                        name=ctx.message.author.display_name,
                        icon_url=ctx.message.author.display_avatar.url
                    )
                muteEmbed.add_field(name='Reason:',value=reason)
                muteEmbed.add_field(name='Server:',value=ctx.guild.name)
                await user.send(embed=muteEmbed)
                return
        permissions=discord.Permissions(permissions=0,send_messages=False,speak=False)
        try:
            role = await guild.create_role(name="Muted",reason="Muted role did not exist.",permissions=permissions)
        except discord.Forbidden:
            botPermEmbed = discord.Embed(title='ERROR',description=f'{self.client.user.name} is missing the required permission(s) to run this command.',color=0x992D22)
            botPermEmbed.set_author(
                name=ctx.message.author.display_name,
                icon_url=ctx.message.author.display_avatar.url
            )
            botPermEmbed.set_thumbnail(url=self.client.user.display_avatar.url)
            try:
                await ctx.reply(embed=botPermEmbed)
            except:
                await ctx.send(embed=botPermEmbed)
            return
        try:
            msg = await ctx.reply("Please wait while I setup the Muted role.")
        except:
            msg = await ctx.send("Please wait while I setup the Muted role.")
        for discord.TextChannel in channels:
            await discord.TextChannel.set_permissions(role,send_messages=False)
        for discord.VoiceChannel in channels:
            await discord.VoiceChannel.set_permissions(role,speak=False) 
        try:
            await msg.delete()
        except discord.Forbidden:
            pass
        try:
            await user.add_roles(role)
        except discord.Forbidden:
            botPermEmbed = discord.Embed(title='ERROR',description=f'{self.client.user.name} is missing the required permission(s) to run this command.',color=0x992D22)
            botPermEmbed.set_author(
                name=ctx.message.author.display_name,
                icon_url=ctx.message.author.display_avatar.url
            )
            botPermEmbed.set_thumbnail(url=self.client.user.display_avatar.url)
            try:
                await ctx.reply(embed=botPermEmbed)
            except:
                await ctx.send(embed=botPermEmbed)
            return
        muteEmbed = discord.Embed(title='Mute',description=f'Muted {user.mention}.',color=discord.Colour.random())
        muteEmbed.set_thumbnail(url=user.display_avatar.url)
        muteEmbed.set_author(
                name=ctx.message.author.display_name,
                icon_url=ctx.message.author.display_avatar.url
            )
        muteEmbed.add_field(name='Reason:',value=reason)
        try:
            await ctx.reply(embed=muteEmbed)
        except:
            await ctx.send(embed=muteEmbed)
        muteEmbed = discord.Embed(title='Mute',description=f'Muted {user.mention}.',color=discord.Colour.random())
        muteEmbed.set_thumbnail(url=ctx.guild.icon_url)
        muteEmbed.set_author(
                name=ctx.message.author.display_name,
                icon_url=ctx.message.author.display_avatar.url
            )
        muteEmbed.add_field(name='Reason:',value=reason)
        muteEmbed.add_field(name='Server:',value=ctx.guild.name)
        await user.send(embed=muteEmbed)
    
    @commands.command(name='unmute',description='Unmutes the user you ping.')
    @has_permissions(manage_roles=True)
    async def unmute(self,ctx,user: commands.MemberConverter=None):
        if user == None:
            await ctx.reply("Please provide a user!")
            return
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass
        roles = user.roles
        for discord.Role in roles:
            if discord.Role.name.upper() == "MUTED":
                try:
                    await user.remove_roles(discord.Role,reason="Unmuting the user.")
                except discord.Forbidden:
                    botPermEmbed = discord.Embed(title='ERROR',description=f'{self.client.user.name} is missing the required permission(s) to run this command.',color=0x992D22)
                    botPermEmbed.set_author(
                        name=ctx.message.author.display_name,
                        icon_url=ctx.message.author.display_avatar.url
                    )
                    botPermEmbed.set_thumbnail(url=self.client.user.display_avatar.url)
                    try:
                        await ctx.reply(embed=botPermEmbed)
                    except:
                        await ctx.send(embed=botPermEmbed)
                    return
                unmuteEmbed = discord.Embed(title='Unmute',description=f'Unmuted {user.mention}',color=discord.Colour.random())
                unmuteEmbed.set_thumbnail(url=user.display_avatar.url)
                unmuteEmbed.set_author(
                        name=ctx.message.author.display_name,
                        icon_url=ctx.message.author.display_avatar.url
                    )
                try:
                    await ctx.reply(embed=unmuteEmbed)
                except:
                    await ctx.send(embed=unmuteEmbed)
                unmuteEmbed = discord.Embed(title='Unmute',description=f'Unmuted {user.mention}',color=discord.Colour.random())
                unmuteEmbed.set_thumbnail(url=ctx.guild.icon_url)
                unmuteEmbed.set_author(
                        name=ctx.message.author.display_name,
                        icon_url=ctx.message.author.display_avatar.url
                    )
                unmuteEmbed.add_field(name='Server:',value=ctx.guild.name)
                await user.send(embed=unmuteEmbed)
                return
        try:
            await ctx.reply(f"{user.mention} is not muted!")
        except:
            await ctx.send(f"{user.mention} is not muted!")

    @commands.command(aliases=['comeback', 'revive', 'oops', 'pardon'], permissions=["ban_members"], name='unban', description='Unbans a banned user')
    @has_permissions(ban_members=True)    
    async def unban(self, ctx, *, user: discord.User=None):

        if user == None:
            try:
                await ctx.reply("User not found!")
            except:
                await ctx.send("User not found!")        

        try:
            bans = tuple(ban_entry.user for ban_entry in await ctx.guild.bans())
            if user in bans:
                await ctx.guild.unban(user)
            else:
                try:
                    await ctx.reply("User not banned!")
                except:
                    await ctx.send("User not banned!")
                return
        except discord.Forbidden:
            botPermEmbed = discord.Embed(title='ERROR',description=f'{self.client.user.name} is missing the required permission(s) to run this command.',color=0x992D22)
            botPermEmbed.set_author(
                name=ctx.message.author.display_name,
                icon_url=ctx.message.author.display_avatar.url
            )
            botPermEmbed.set_thumbnail(url=self.client.user.display_avatar.url)
            try:
                await ctx.reply(embed=botPermEmbed)
            except:
                await ctx.send(embed=botPermEmbed)
            return

        except:
            try:
                await ctx.reply("Unbanning failed!")
            except:
                await ctx.send("Unbanning failed!")
            return
    
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass
        unbanEmbed = discord.Embed(title='Unban',description=f'{user.mention} has been unbanned.',color=discord.Colour.random())
        unbanEmbed.set_thumbnail(url=user.display_avatar.url)
        unbanEmbed.set_author(
                name=ctx.message.author.display_name,
                icon_url=ctx.message.author.display_avatar.url
            )
        try:
            await ctx.reply(embed=unbanEmbed)
        except:
            await ctx.send(embed=unbanEmbed)
        unbanEmbed = discord.Embed(title='Unban',description=f'{user.mention} has been unbanned.',color=discord.Colour.random())
        unbanEmbed.set_thumbnail(url=ctx.guild.icon_url)
        unbanEmbed.set_author(
                name=ctx.message.author.display_name,
                icon_url=ctx.message.author.display_avatar.url
            )
        unbanEmbed.add_field(name='Server:',value=ctx.guild.name)
        await user.send(embed=unbanEmbed)


    
    @commands.command(aliases=['goawayforever'], name='ban', description='Bans a user')
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member : commands.MemberConverter, *, reason=None):
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass
        try:
            await member.ban(reason=reason)
        except discord.Forbidden:
            botPermEmbed = discord.Embed(title='ERROR',description=f'{self.client.user.name} is missing the required permission(s) to run this command.',color=0x992D22)
            botPermEmbed.set_author(
                name=ctx.message.author.display_name,
                icon_url=ctx.message.author.display_avatar.url
            )
            botPermEmbed.set_thumbnail(url=self.client.user.display_avatar.url)
            try:
                await ctx.reply(embed=botPermEmbed)
            except:
                await ctx.send(embed=botPermEmbed)
            return
        banEmbed = discord.Embed(title='Ban',description=f'{member.mention} has been banned.', color=discord.Colour.random())
        banEmbed.set_author(
            name=ctx.message.author.display_name,
            icon_url=ctx.message.author.display_avatar.url
        )
        banEmbed.set_thumbnail(url=member.display_avatar.url)
        banEmbed.add_field(name='Reason:',value=reason)
        try:
            await ctx.reply(embed=banEmbed)
        except:
            await ctx.send(embed=banEmbed)
        banEmbed = discord.Embed(title='Ban',description=f'{member.mention} has been banned.', color=discord.Colour.random())
        banEmbed.set_author(
            name=ctx.message.author.display_name,
            icon_url=ctx.message.author.display_avatar.url
        )
        banEmbed.set_thumbnail(url=ctx.guild.icon_url)
        banEmbed.add_field(name='Reason:',value=reason)
        banEmbed.add_field(name='Server:',value=ctx.guild.name)
        await member.send(embed=banEmbed)

    @commands.command(aliases=['goaway','dickkick'], name='kick', description='Kicks a user')
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member : commands.MemberConverter, *, reason=None):
        
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass
        try:
            await member.kick(reason=reason)
        except discord.Forbidden:
            botPermEmbed = discord.Embed(title='ERROR',description=f'{self.client.user.name} is missing the required permission(s) to run this command.',color=0x992D22)
            botPermEmbed.set_author(
                name=ctx.message.author.display_name,
                icon_url=ctx.message.author.display_avatar.url
            )
            botPermEmbed.set_thumbnail(url=self.client.user.display_avatar.url)
            await ctx.send(embed=botPermEmbed)
            return
        kickEmbed = discord.Embed(title='Kick',description=f'{member.mention} has been kicked.',color=discord.Colour.random())
        kickEmbed.set_author(
            name=ctx.message.author.display_name,
            icon_url=ctx.message.author.display_avatar.url
        )
        kickEmbed.set_thumbnail(url=member.display_avatar.url)
        kickEmbed.add_field(name='Reason:',value=reason)
        await ctx.reply(embed=kickEmbed)
        kickEmbed = discord.Embed(title='Kick',description=f'{member.mention} has been kicked.',color=discord.Colour.random())
        kickEmbed.set_author(
            name=ctx.message.author.display_name,
            icon_url=ctx.message.author.display_avatar.url
        )
        kickEmbed.set_thumbnail(url=ctx.guild.icon_url)
        kickEmbed.add_field(name='Reason:',value=reason)
        kickEmbed.add_field(name='Server:',value=ctx.guild.name)
        await member.send(embed=kickEmbed)

    @commands.command(aliases=["toggletickets","toggleticket","ticketstoggle"],name='tickettoggle',description='Toggles tickets.')
    @has_permissions(manage_channels=True)
    async def tickettoggle(self,ctx):
        with open("json/data.json","r") as f:
            ticketToggle = json.load(f)
        

        if f"{ctx.message.guild.id} Ticket" not in ticketToggle:
            ticketToggle[f"{ctx.message.guild.id} Ticket"] = False
            with open("json/data.json","w") as f:
                json.dump(ticketToggle, f,indent=4)
            return await ctx.reply("Tickets are now off.")
        elif ticketToggle[f"{ctx.message.guild.id} Ticket"] == True:
            ticketToggle[f"{ctx.message.guild.id} Ticket"] = False
            with open("json/data.json","w") as f:
                json.dump(ticketToggle,f,indent=4)
            return await ctx.reply("Tickets are now off.")
        elif ticketToggle[f"{ctx.message.guild.id} Ticket"] == False:
            ticketToggle[f"{ctx.message.guild.id} Ticket"] = True
            with open("json/data.json","w") as f:
                json.dump(ticketToggle,f,indent=4)
            return await ctx.reply("Tickets are now on.")
        

    @commands.command(aliases=['ticket_create','create_ticket','createticket'],name='ticketcreate',description='Creates a ticket.')
    #@has_permissions(administrator=True)
    async def ticketcreate(self, ctx,*,reason=None):
        if reason == None:
            def check(ms):
                return ms.channel == ctx.message.channel and ms.author == ctx.message.author
            try:
                askMessage = await ctx.reply("What's your messaage?")
            except:
                askMessage = await ctx.send("What's your message?")
            OtherMessage = await self.client.wait_for('message', check=check)
            reason = OtherMessage.content
            try:
                await askMessage.delete()
                await OtherMessage.delete()
            except discord.Forbidden:
                pass
        with open("json/data.json","r") as f:
            ticketCheck = json.load(f)

        if f"{ctx.message.guild.id} Ticket" not in ticketCheck:
            ticketCheck[f"{ctx.message.guild.id} Ticket"] = False
            return await ctx.reply("Tickets are off.")
        elif ticketCheck[f"{ctx.message.guild.id} Ticket"] == False:
            return await ctx.reply("Tickets are off.")


        def check(reaction, user):
            return str(reaction) == "🔒" and user != self.client.user

        guild = ctx.message.guild
        overwrites={
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
            ctx.message.author: discord.PermissionOverwrite(manage_channels=True),
            ctx.message.author: discord.PermissionOverwrite(read_messages=True),
        }
        try:
            channel = await guild.create_text_channel(f'ticket-{ctx.author}', overwrites=overwrites, reason="ticket system")
        except discord.Forbidden:
            botPermEmbed = discord.Embed(title='ERROR',description=f'{self.client.user.name} is missing the required permission(s) to run this command.',color=0x992D22)
            botPermEmbed.set_author(
                name=ctx.message.author.display_name,
                icon_url=ctx.message.author.display_avatar.url
            )
            botPermEmbed.set_thumbnail(url=self.client.user.display_avatar.url)
            try:
                await ctx.reply(embed=botPermEmbed)
            except:
                await ctx.send(embed=botPermEmbed)
            return
        pingMessage = await channel.send(f"<@!{ctx.message.author.id}>")
        try:
            await pingMessage.delete()
        except discord.Forbidden:
            pass
        infoEmbed = discord.Embed(title='Ticket',description=f'Created by <@!{ctx.message.author.id}>',color=discord.Colour.random())
        infoEmbed.add_field(name='Reason',value=reason)
        await channel.send(embed=infoEmbed)
        message = await channel.send("React with :lock: to close the ticket.")
        await message.add_reaction("🔒")
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass

        await self.client.wait_for("reaction_add", check=check)
        try:
            await channel.set_permissions(ctx.message.author,reason="Closing the ticket.", send_messages=False)
        except discord.Forbidden:
            botPermEmbed = discord.Embed(title='ERROR',description=f'{self.client.user.name} is missing the required permission(s) to run this command.',color=0x992D22)
            botPermEmbed.set_author(
                name=ctx.message.author.display_name,
                icon_url=ctx.message.author.display_avatar.url
            )
            botPermEmbed.set_thumbnail(url=self.client.user.display_avatar.url)
            try:
                await ctx.reply(embed=botPermEmbed)
            except:
                await ctx.send(embed=botPermEmbed)
            return
        await channel.send("Ticket Closed.")
        
        #def check2(reaction, user):  
        #    return str(reaction) == "⛔" and user == user
        #message = await channel.send(":no_entry: to delete this channel.")
        #await message.add_reaction("⛔")
        #await self.client.wait_for("reaction_add",check=check2)

        
    @commands.command(name='slowmode', description='Adds slowmode to a channel, limit is 21600')
    @has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int):
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass
        
        try:
            await ctx.channel.edit(slowmode_delay=seconds)
        except discord.Forbidden:
            botPermEmbed = discord.Embed(title='ERROR',description=f'{self.client.user.name} is missing the required permission(s) to run this command.',color=0x992D22)
            botPermEmbed.set_author(
                name=ctx.message.author.display_name,
                icon_url=ctx.message.author.display_avatar.url
            )
            botPermEmbed.set_thumbnail(url=self.client.user.display_avatar.url)
            try:
                await ctx.reply(embed=botPermEmbed)
            except:
                await ctx.send(embed=botPermEmbed)
            return
        slowEmbed = discord.Embed(title='Slowmode',description=f'Slowmode is now on **{seconds}** seconds.',color=discord.Colour.random())
        slowEmbed.set_author(
            name=ctx.message.author.display_name,
            icon_url=ctx.message.author.display_avatar.url
        )
        slowEmbed.set_thumbnail(url=self.client.user.display_avatar.url)
        try:
            await ctx.reply(embed=slowEmbed)
        except:
            await ctx.send(embed=slowEmbed)


    @commands.command(name='clear', description='Clears the amount of messages you want')
    @has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=2):
        try:
            await ctx.channel.purge(limit=amount)
        except discord.Forbidden:
            botPermEmbed = discord.Embed(title='ERROR',description=f'{self.client.user.name} is missing the required permission(s) to run this command.',color=0x992D22)
            botPermEmbed.set_author(
                name=ctx.message.author.display_name,
                icon_url=ctx.message.author.display_avatar.url
            )
            botPermEmbed.set_thumbnail(url=self.client.user.display_avatar.url)
            try:
                await ctx.reply(embed=botPermEmbed)
            except:
                await ctx.send(embed=botPermEmbed)
            return

def setup(client):
    client.add_cog(Moderation(client))