from discord.ext import commands
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("url") + "tags/"

def setup(bot):
    bot.add_cog( Tags(bot=bot) )

class Tags(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.group(invoke_without_command=True)
    async def tag(self, ctx, *, name):
        params = {
            "amount": "one",
            "tag_name": name
            }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as res:

                data = await res.json()

                if res.status == 400:
                    await ctx.message.delete(delay=2)
                    await ctx.send(data["message"], delete_after=3)

                else:
                    await ctx.send(data["data"])


    @tag.command(help="``/tag all``")
    async def all(self, ctx):
        params = { "amount": "all" }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as res:
                data = await res.json()

                if res.status == 400:
                    await ctx.message.delete(delay=2)
                    await ctx.send(data["message"], delete_after=3)

                else:
                    tag_names = [i["tag_name"] for i in data]
                    organised_names = "\n".join(tag_names)

                    await ctx.send(organised_names)


    @tag.command(help='``/tag create "name" data``')
    async def create(self, ctx, name, *, data):
        t = {
            "tag_name": name,
            "data": data,
            "author": {
                "name": f"{ctx.author}",
                "id": ctx.author.id
            }
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=t) as res:
                data = await res.json()

                if res.status == 400:
                    await ctx.message.delete(delay=2)
                    await ctx.send(data["message"], delete_after=3)

                else:
                    await ctx.send(f'tag "{name}" created')


    @tag.command(help='``/tag edit "name" new_data``')
    async def edit(self, ctx, name, *, data):
        old_tag = url + name

        y = { "data": data }

        async with aiohttp.ClientSession() as session:
            async with session.put(old_tag, json=y) as res:
                data = await res.json()

                if res.status == 400:
                    await ctx.message.delete(delay=2)
                    await ctx.send(data["message"], delete_after=3)

                else:
                    await ctx.send(f'edited tag "{name}"')


    @tag.command(help='``/tag rename "old_name" new_name``')
    async def rename(self, ctx, old_name, new_name):
        old_tag = url + old_name

        com = { "tag_name": new_name }

        async with aiohttp.ClientSession() as session:
            async with session.put(old_tag, json=com) as res:
                data = await res.json()

                if res.status == 400:
                    await ctx.message.delete(delay=2)
                    await ctx.send(data["message"], delete_after=3)

                else:
                    await ctx.send(f'rename tag "{old_name}" to "{new_name}"')


    @tag.command(help='``/tag delete name``')
    async def delete(self, ctx, *, name):
        tag_url = url + name

        async with aiohttp.ClientSession() as session:
            async with session.delete(tag_url) as res:
                data = await res.json()

                if res.status == 400:
                    await ctx.message.delete(delay=2)
                    await ctx.send(data["message"], delete_after=3)

                else:
                    await ctx.send(f'deleted tag "{name}"')
