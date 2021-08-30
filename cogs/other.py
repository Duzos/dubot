from operator import truediv
import discord
from discord import guild
from discord.ext import commands
import random
import json
from discord.ext.commands.converter import MessageConverter
from discord.ext.commands.core import has_permissions


# le cog of le other
class Other(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['rcolour','rcolor','randomcolor'],name='randomcolour',description='Gives you a random colour.')
    async def randomcolour(self, ctx):
        colour=discord.Color.random()
        await ctx.message.delete()
        colourEmbed=discord.Embed(title=colour,description='The colour is the colour of this embed.',color=colour)
        colourEmbed.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url
            )
        colourEmbed.set_thumbnail(url=self.client.user.avatar_url)
        await ctx.send(embed=colourEmbed)
    
    #@commands.command()
    #async def cum(self, ctx):
    #    await ctx.send("no im not adding this command this is getting removed after.")

    @commands.command(aliases=['reportbug', 'bug', 'error'],name='bug_report',description='Reports a bug.')
    async def bug_report(self, ctx, *, message=None):
        await ctx.message.delete()
        duzo = self.client.get_user(327807253052653569)
        await duzo.send(f'Bug: "{message}"')
        await duzo.send(f'Bug reported by {ctx.message.author}')
        msg = await ctx.send("Bug reported.")
        await msg.delete()

    
    @commands.command(aliases=['welcomeoption','woption'],name='welcome_option', description='Turn welcome messages on and off.')
    @has_permissions(manage_channels=True)
    async def welcome_option(self, ctx):
        def check(ms):
            return ms.channel == ctx.message.channel and ms.author == ctx.message.author
        with open('json/data.json', 'r') as f:
            welcome = json.load(f)
        
        await ctx.message.delete()


        msg = await ctx.send("Do you want it to be on or off?")
        Msg = await self.client.wait_for('message', check=check)
        welcomeChoice = Msg.content
        await msg.delete()
        await Msg.delete()


        idGuild = str(ctx.guild.id)

        if welcomeChoice == "on":
            welcomeChoice = True
        elif welcomeChoice == "off":
            welcomeChoice = False
            return
        elif welcomeChoice == "Off":
            welcomeChoice = False
            return
        elif welcomeChoice == "On":
            welcomeChoice = True
        else:
            msg = await ctx.send("Invalid choice, please choose on or off")
            await msg.delete()
            return

        msg = await ctx.send("What is the channel you want the message to be sent in?")
        ChannelMsg = await self.client.wait_for('message',check=check)
        welcomeChannel = await commands.TextChannelConverter().convert(ctx, Msg.content)
        await msg.delete()
        await Msg.delete()

        welcomeChannelID = welcomeChannel.id


        welcome[f"{idGuild} welcome"] = welcomeChoice
        welcome[f"{idGuild} welcomeChannel"] = welcomeChannelID

        msg = await ctx.send("Done.")
        await msg.delete()

        with open('json/data.json', 'w') as f:
            json.dump(welcome, f , indent=4)

    @commands.command(aliases=['leaveoption','loption'],name='leave_option', description='Turn leave messages on and off.')
    @has_permissions(manage_channels=True)
    async def leave_option(self, ctx):
        def check(ms):
            return ms.channel == ctx.message.channel and ms.author == ctx.message.author
        with open('json/data.json', 'r') as f:
            leave = json.load(f)
        
        await ctx.message.delete()

        idGuild = str(ctx.guild.id)
        
        msg = await ctx.send("Do you want it to be on or off?")
        Msg = await self.client.wait_for('message', check=check)
        leaveChoice = Msg.content
        await msg.delete()
        await Msg.delete()

        if leaveChoice == "on":
            leaveChoice = True
        elif leaveChoice == "off":
            leaveChoice = False
            return
        elif leaveChoice == "Off":
            leaveChoice = False
            return
        elif leaveChoice == "On":
            leaveChoice = True
        else:
            msg = await ctx.send("Invalid choice, please choose on or off")
            await msg.delete()
            return

        msg = await ctx.send("What is the channel you want the message to be sent in?")
        Msg = await self.client.wait_for('message',check=check)
        leaveChannel = await commands.TextChannelConverter().convert(ctx, Msg.content)
        await msg.delete()
        await Msg.delete()

        leaveChannelID = leaveChannel.id


        leave[f"{idGuild} leave"] = leaveChoice
        leave[f"{idGuild} leaveChannel"] = leaveChannelID

        msg = await ctx.send("Done.")
        await msg.delete()

        with open('json/data.json', 'w') as f:
            json.dump(leave, f , indent=4)

    @commands.command(aliases=['changeprefix'],name='prefix',description='Changes the bots prefix.')
    @has_permissions(manage_channels=True)
    async def prefix(self, ctx):

        await ctx.message.delete()
    
        def check(ms):
            return ms.channel == ctx.message.channel and ms.author == ctx.message.author
        #await ctx.channel.purge(limit=1)
        with open('json/data.json', 'r') as f:
            prefixes = json.load(f)

        msgRequest = await ctx.send("What is the new prefix?")
        msg1 = await self.client.wait_for('message', check=check)
        await msgRequest.delete()
        await msg1.delete()
        prefixList = []
        prefixList.append(msg1.content)
        prefixList.append(f"<@!{self.client.user.id}> ")
        msgRequest = await ctx.send("Would you like to add an extra prefix?")
        msg2 = await self.client.wait_for('message', check=check)
        await msgRequest.delete()
        await msg2.delete()
        if msg2.content == "Yes" or msg2.content == "yes":
            msgRequest = await ctx.send("What is the extra prefix?")
            msg3 = await self.client.wait_for('message',check=check)
            await msgRequest.delete()
            await msg3.delete()
            prefixList.append(msg3.content)

        guildID = str(ctx.guild.id)
        prefixes[f"{guildID} prefix"] = prefixList

        with open('json/data.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
        await ctx.send(f'Changed the Prefixes to **{prefixList}**')

        
    @commands.command(
    name='help',
    description='This command.',
    aliases=['commands', 'command'],
    usage='cog'
    )
    async def help(self, ctx, cog='all'):
        await ctx.message.delete()
        help_embed = discord.Embed(
            title='Help',
            color=discord.Colour.random()
        )
        help_embed.set_thumbnail(url=self.client.user.avatar_url)
        help_embed.set_footer(
            text=f'Requested by {ctx.message.author.name}',
            icon_url=self.client.user.avatar_url
        )

        # Get a list of all cogs
        cogs = [c for c in self.client.cogs.keys()]

        # If cog is not specified by the user, we list all cogs and commands

        if cog == 'all':
            for cog in cogs:
                # Get a list of all commands under each cog

                cog_commands = self.client.get_cog(cog).get_commands()
                commands_list = ''
                for comm in cog_commands:
                    commands_list += f'**{comm.name}** - {comm.description}\n'

                # Add the cog's details to the embed.

                help_embed.add_field(
                    name=cog,
                    value=commands_list,
                    inline=True
                ).add_field(
                    name='\u200b', value='\u200b', inline=False
                )

                # Also added a blank field '\u200b' is a whitespace character.
            pass
        else:

            # If the cog was specified

            lower_cogs = [c.lower() for c in cogs]

            # If the cog actually exists.
            if cog.lower() in lower_cogs:

                # Get a list of all commands in the specified cog
                commands_list = self.client.get_cog(cogs[ lower_cogs.index(cog.lower()) ]).get_commands()
                help_text=''

                # Add details of each command to the help text
                # Command Name
                # Description
                # [Aliases]
                #
                # Format
                for command in commands_list:
                    help_text += f'```{command.name}```\n' \
                        f'**{command.description}**\n\n'

                    # Also add aliases, if there are any
                    if len(command.aliases) > 0:
                        help_text += f'**Aliases :** `{"`, `".join(command.aliases)}`\n\n\n'
                    else:
                        # Add a newline character to keep it pretty
                        # That IS the whole purpose of custom help
                        help_text += '\n'

                    # Finally the format
                    help_text += f'Format: `d.' \
                        f' {command.name}{command.usage if command.usage is not None else ""}`\n\n\n\n'

                help_embed.description = help_text
            else:
                # Notify the user of invalid cog and finish the command
                await ctx.send('Invalid cog specified.\nUse `help` command to list all cogs.')
                return


        await ctx.send(embed=help_embed)
        
        return


def setup(client):
    client.add_cog(Other(client))