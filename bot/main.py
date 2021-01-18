import discord
from discord.ext import commands

import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

cogs = [
    "cogs.tags",
    "cogs.ban_word",
    "cogs.channel_role",
    "cogs.help_command",
    "cogs.deleted_message",
    "cogs.music"
]

class Main(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix="/")

    async def on_ready(self):
        activity = discord.Activity(name=" you | /help", type=discord.ActivityType.watching)
        await self.change_presence(activity=activity, status=discord.Status.idle)

        print("on ready")

        for cog in cogs:
            self.load_extension(cog)

    async def on_command_error(self, ctx, exception):

        await ctx.send(exception, delete_after=3)
        await ctx.message.delete(delay=2)

    @classmethod
    async def setup(cls):
        bot = cls()
        token = os.getenv("token")

        await bot.start(token, bot=True)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Main.setup())