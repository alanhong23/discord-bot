from discord.ext import commands
import discord
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("url") + "channel_role"

def setup(bot):
    bot.add_cog( Commands(bot=bot) )

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction_event):

        param = { "message_id": str(reaction_event.message_id) }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=param) as res:

                if res.status != 400 and reaction_event.member.bot is not True:
                    channel_roles = await res.json()
                    guild = self.bot.get_guild(reaction_event.guild_id)

                    for channel_role in channel_roles:
                        if str(reaction_event.emoji) == channel_role["emoji"]:
                            role = guild.get_role( int(channel_role["channel_role_id"]) )

                            await reaction_event.member.add_roles(role)


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, reaction_event):
        param = { "message_id": str(reaction_event.message_id) }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=param) as res:

                if res.status != 400:
                    channel_roles = await res.json()
                    guild = self.bot.get_guild(reaction_event.guild_id)

                    for channel_role in channel_roles:
                        if str(reaction_event.emoji) == channel_role["emoji"]:

                            role = guild.get_role( int(channel_role["channel_role_id"]) )
                            user = await guild.fetch_member(reaction_event.user_id)

                            await user.remove_roles(role)


    @commands.Cog.listener()
    async def on_raw_message_delete(self, message_event):

        param = { "message_id": str(message_event.message_id) }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=param) as res:

                if res.status != 400:
                    channel_roles = await res.json()
                    guild = self.bot.get_guild(message_event.guild_id)

                    for channel_role in channel_roles:

                        role = guild.get_role( int(channel_role["channel_role_id"]) )
                        channel = guild.get_channel( int(channel_role["channel_id"]) )

                        await role.delete()
                        await channel.set_permissions(guild.default_role, view_channel=True)

            await session.delete(url, params=param)


    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        for role in before.guild.roles:
            if role.name == before.name and before.name != after.name:
                await role.edit(name=after.name)


    @commands.command(help='``/create_channel_role <emoji> <channel> ...``')
    async def create_channel_role(self, ctx, *channel):
        emoji_channel = dict( zip(channel[::2], channel[1::2]) )
        message_list = [ f"React with {emoji} to access {channel_id}" for emoji, channel_id in emoji_channel.items() ]

        embed = discord.Embed(

            title="Reaction roles",
            description="\n".join(message_list),
            color=discord.Color.from_rgb(135,225,209)

        ).set_footer(text="* cancel anytime")

        message = await ctx.send(embed=embed)

        for emoji in emoji_channel.keys():
            await message.add_reaction(emoji)

        await ctx.message.delete()

        for emoji, channel_id in emoji_channel.items():
            channel_id = channel_id.replace("<#", "").replace(">", "")

            channel = ctx.guild.get_channel( int(channel_id) )
            channel_role = await ctx.guild.create_role(name=channel.name)

            information = {
                "message_id": str(message.id),
                "channel_role_id": str(channel_role.id),
                "channel_id": channel_id,
                "emoji": emoji
            }

            async with aiohttp.ClientSession() as session:
                await session.post(url, json=information)

            await channel.set_permissions(channel_role, view_channel=True)
            await channel.set_permissions(ctx.guild.default_role, view_channel=False)


    @commands.command(help='``/clear <amount>``')
    async def clear(self, ctx, number):
        amount = int(number) + 1

        async for message in ctx.history(limit=amount):
            await message.delete()
