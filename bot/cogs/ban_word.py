from discord.ext import commands
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("url") + "words/"

def setup(bot):
    bot.add_cog( Words(bot=bot) )

class Words(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self, message):
        mes = message.content.lower().strip().replace(" ", "")

        params = { "amount": "all" }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as res:

                data = await res.json()
                words = [ i["word"] for i in data ]

                for word in words:
                    if word in mes and "/ban_word" not in mes:
                        user = ""

                        if word == "sohai":
                            user = os.getenv("secret_user")

                        if message.author.bot is not True:
                            await message.delete()
                            await message.channel.send(f"{user}shut the fuck up", delete_after=3)


    @commands.group(invoke_without_command=True)
    async def ban_word(self, ctx):
        params = { "amount": "all" }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as res:
                data = await res.json()

                if res.status == 400:
                    await ctx.message.delete(delay=2)
                    await ctx.send(data["message"], delete_after=3)

                else:
                    words = [ i["word"] for i in data ]
                    organised_words = "\n".join(words)

                    await ctx.send(organised_words)


    @ban_word.command(help='``/ban_word create word``')
    async def create(self, ctx, *, raw_word):
        word = raw_word.lower().strip().replace(" ", "")

        w = {
            "word": word,
            "author": {
                "name": f"{ctx.author}",
                "id": ctx.author.id
            }
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=w) as res:
                data = await res.json()

                if res.status == 400:
                    await ctx.message.delete(delay=2)
                    await ctx.send(data["message"], delete_after=3)

                else:
                    await ctx.send(f'ban word"{raw_word}" added')


    @ban_word.command(help='``/ban_word delete word``')
    async def delete(self, ctx, *, raw_word):
        word = raw_word.lower().strip().replace(" ", "")
        word_url = url + word

        async with aiohttp.ClientSession() as session:
            async with session.delete(word_url) as res:
                data = await res.json()

                if res.status == 400:
                    await ctx.message.delete(delay=2)
                    await ctx.send(data["message"], delete_after=3)

                else:
                    await ctx.send(f'deleted ban word "{raw_word}"')


    @ban_word.command(help='``/ban_word edit "old_word" new_word``')
    async def edit(self, ctx, raw_old_word, *, raw_new_word):
        old_word = raw_old_word.lower().strip().replace(" ", "")
        new_word = raw_new_word.lower().strip().replace(" ", "")
        old_word_url = url + old_word

        wor = { "word": new_word }

        async with aiohttp.ClientSession() as session:
            async with session.put(old_word_url, json=wor) as res:
                data = await res.json()

                if res.status == 400:
                    await ctx.message.delete(delay=2)
                    await ctx.send(data["message"], delete_after=3)

                else:
                    await ctx.send(f'edited ban word "{raw_old_word}" to "{raw_new_word}"')