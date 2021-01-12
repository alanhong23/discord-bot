from discord.ext import commands
import discord

def setup(bot):
    bot.add_cog( Help(bot=bot) )

class Help_command(commands.HelpCommand):

    @staticmethod
    def embed(title, description=discord.Embed.Empty):
        return discord.Embed(

            title=title,
            description=description,
            colour=discord.Colour.dark_teal()

        )


    async def send_bot_help(self, mapping):
        embed = self.embed("Help")

        mapping.pop(None)

        for cog, commds in mapping.items():
            value = ""

            for commd in commds:
                if len(commds) >= 2:
                    value = f"{value}\n{commd.name}"
                else:
                    value = commd.name

                if commds.index(commd) + 1 == len(commds):
                    embed.add_field(name=cog.qualified_name, value=value, inline=False)

        await self.context.send(embed=embed)


    async def send_cog_help(self, cog):
        commds = [ commd.name for commd in cog.get_commands() ]
        embed = self.embed(cog.qualified_name, "\n".join(commds))

        await self.context.send(embed=embed)


    async def send_group_help(self, group):
        embed = self.embed(group.qualified_name)

        for commd in group.commands:
            embed.add_field(name=commd.name, value=commd.help, inline=False)

        await self.context.send(embed=embed)


    async def send_command_help(self, command):
        embed = self.embed(command.name, command.help)

        await self.context.send(embed=embed)

class Help(commands.Cog):
    def __init__(self, bot):
        self._original_help_command = bot.help_command
        bot.help_command = Help_command()
        bot.help_command.cog = self
        self.bot = bot

    def cog_unload(self):
        self.bot.help_command = self._original_help_command
