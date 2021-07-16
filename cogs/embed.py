from discord.ext import commands
import discord
import random

# These color constants are taken from discord.js library
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


class Embed(commands.Cog):

    def __init__(self, client):
        self.client = client

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
        await ctx.send(content='What would you like the title to be?')

        # Wait for a response and get the title
        msg = await self.client.wait_for('message', check=check)
        title = msg.content # Set the title

        # Next, ask for the content
        await ctx.send(content='What would you like the Description to be?')
        msg = await self.client.wait_for('message', check=check)
        desc = msg.content

        # Finally make the embed and send it
        msg = await ctx.send(content='Now generating the embed...')

        color_list = [c for c in colors.values()]
        # Convert the colors into a list
        # To be able to use random.choice on it

        embed = discord.Embed(
            title=title,
            description=desc,
            color=random.choice(color_list)
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

    @commands.command(name='test', description='Tests if embeds are working')
    async def test(self, ctx):
        title="test"
        desc="test"
        color_list = [c for c in colors.values()]
        msg = await ctx.send("one seccc")
        embed=discord.Embed(
            title=title,
            desc=desc,
            color=random.choice(color_list)
        )
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url
        )
        await msg.edit(
            embed=embed,
            content=None
        )


    @commands.command(
    name='help',
    description='The help command!',
    aliases=['commands', 'command'],
    usage='cog'
    )
    async def help(self, ctx, cog='all'):
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
                    inline=False
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
                    help_text += f'Format: `@{self.client.user.name}#{self.client.user.discriminator}' \
                        f' {command.name} {command.usage if command.usage is not None else ""}`\n\n\n\n'

                help_embed.description = help_text
            else:
                # Notify the user of invalid cog and finish the command
                await ctx.send('Invalid cog specified.\nUse `help` command to list all cogs.')
                return

        await ctx.send(embed=help_embed)
        
        return

def setup(client):
    client.add_cog(Embed(client))
    # Adds the Basic commands to the bot
    # Note: The "setup" function has to be there in every cog file