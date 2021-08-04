from operator import truediv
import discord
from discord import guild
from discord.ext import commands
import random
import json
from discord.ext.commands.converter import MessageConverter

from discord.ext.commands.core import has_permissions

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

# le cog of le other
class Other(commands.Cog):

    def __init__(self, client):
        self.client = client

    
    #@commands.command()
    #async def cum(self, ctx):
    #    await ctx.send("no im not adding this command this is getting removed after.")

    @commands.command(aliases=['reportbug', 'bug', 'error'],name='bug_report',description='Reports a bug.')
    async def bug_report(self, ctx, *, message=None):
        with open('json/bugs.json', 'r') as f:
            bug = json.load(f)
        
        await ctx.message.delete()

        duzo = self.client.get_user(327807253052653569)
        await duzo.send(f'Bug: "{message}"')
        await duzo.send(f'Bug reported by {ctx.message.author}')

        bugMessageNumber = random.randint(1,100)
        bugMessageAuthor = str(ctx.message.author)
        bug[f"{bugMessageAuthor} {bugMessageNumber} "] = message

        with open('json/bugs.json', 'w') as f:
            json.dump(bug, f, indent=4)

        msg = await ctx.send("Bug reported.")
        await msg.delete()

    
    @commands.command(name='welcome_option', description='Turn welcome messages on and off.')
    @has_permissions(manage_channels=True)
    async def welcome_option(self, ctx, welcomeChannel: commands.TextChannelConverter, welcomeChoice = False):
        with open('json/welcome.json', 'r') as f:
            welcome = json.load(f)
        
        await ctx.message.delete()


        idGuild = str(ctx.guild.id)

        if welcomeChoice == "true":
            welcomeChoice = True
        elif welcomeChoice == "false":
            welcomeChoice = False
            return
        elif welcomeChoice == False:
            welcomeChoice = False
        elif welcomeChoice == True:
            welcomeChoice = True
        else:
            msg = await ctx.send("Invalid choice, please choose True or False")
            await msg.delete()
            return

        welcomeChannelID = welcomeChannel.id


        welcome[str(ctx.guild.id)] = welcomeChoice
        welcome[f"{idGuild} Channel"] = welcomeChannelID

        msg = await ctx.send("Done.")
        await msg.delete()

        with open('json/welcome.json', 'w') as f:
            json.dump(welcome, f , indent=4)

    @commands.command(name='leave_option', description='Turn leave messages on and off.')
    @has_permissions(manage_channels=True)
    async def leave_option(self, ctx, leaveChannel: commands.TextChannelConverter, leaveChoice = False):
        with open('json/leave.json', 'r') as f:
            leave = json.load(f)
        
        await ctx.message.delete()

        idGuild = str(ctx.guild.id)


        if leaveChoice == "true":
            leaveChoice = True
        elif leaveChoice == "false":
            leaveChoice = False
            return
        elif leaveChoice == False:
            leaveChoice = False
        elif leaveChoice == True:
            leaveChoice = True
        else:
            msg = await ctx.send("Invalid choice, please choose True or False")
            await msg.delete()
            return

        leaveChannelID = leaveChannel.id


        leave[str(ctx.guild.id)] = leaveChoice
        leave[f"{idGuild} Channel"] = leaveChannelID

        msg = await ctx.send("Done.")
        await msg.delete()

        with open('json/leave.json', 'w') as f:
            json.dump(leave, f , indent=4)


    @commands.command(aliases=['changeprefix'],name='prefix',description='Changes the bots prefix.')
    @has_permissions(manage_channels=True)
    async def prefix(self, ctx, newprefix):
        #await ctx.channel.purge(limit=1)
        with open('json/prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = [f'{newprefix},']

        with open('json/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
        await ctx.send(f'Changed the Prefix to **{newprefix}**')
        
    @commands.command(
    name='help',
    description='This command.',
    aliases=['commands', 'command'],
    usage='cog'
    )
    async def help(self, ctx, cog='all'):
        await ctx.message.delete()
        color_list=[c for c in colors.values()]
        help_embed = discord.Embed(
            title='Help',
            color=random.choice(color_list)
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