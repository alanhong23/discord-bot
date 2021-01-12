from discord.ext import commands
import discord
import datetime
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("url") + "delete_message"


def setup(bot):
    bot.add_cog( Deleted_message(bot=bot) )


class Deleted_message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot is not True:
            guild = message.guild
            params = { "guild_id": str(guild.id) }

            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as res:

                    if res.status != 400:
                        data = await res.json()

                        delete_channel = guild.get_channel( int(data["channel_id"]) )

                        if message.attachments:
                            description = discord.Embed.Empty
                            files = []
                            for attachment in message.attachments:
                                files.append(await attachment.to_file(use_cached=True))
                            message_type = "attachment"

                        else:
                            files = None
                            description = message.content
                            message_type = "text"

                        embed = discord.Embed(

                            description=description,
                            color=discord.Color.random(),
                            timestamp=datetime.datetime.now(tz=datetime.timezone.utc)

                        ).set_author(name=message.author.name, icon_url=message.author.avatar_url)\
                         .set_footer(text=message_type)

                        await delete_channel.send( embed=embed, files=files )


    @commands.command(help="``/set_delete_channel``")
    async def set_delete_channel(self, ctx):

        channel_id = {
            "channel_id": str(ctx.channel.id),
            "guild_id": str(ctx.guild.id)
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=channel_id) as res:
                data = await res.json()
                await ctx.message.delete(delay=2)

                if res.status == 400:
                    await ctx.send(data["message"], delete_after=3)
                else:
                    await ctx.send(f"**{ctx.channel.name}** set as deleted message channel", delete_after=3)
                    await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=False)


    @commands.command(help="``/cancel_delete_channel``")
    async def cancel_delete_channel(self, ctx):
        information = {
            "channel_id": str(ctx.channel.id),
            "guild_id": str(ctx.guild.id)
        }

        async with aiohttp.ClientSession() as session:
            async with session.delete(url, params=information) as res:
                data = await res.json()
                await ctx.message.delete(delay=2)

                if res.status == 400:
                    await ctx.send(data["message"], delete_after=3)
                else:
                    await ctx.send(f"**{ctx.channel.name}** set as normal channel", delete_after=3)
                    await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=True)