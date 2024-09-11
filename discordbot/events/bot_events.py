import asyncio
import datetime
import json

import discord
from discord.ext import commands, tasks

from discordbot.utils.news import get_gamesnews


class BotEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=discord.Game("Superleague"))
        print(f"We have logged in as {self.bot.user}")
        self.get_gamesnews.start()
        await asyncio.sleep(50)
        self.delete_news.start()

    @tasks.loop(minutes=60)
    async def gamesnews(self):
        await get_gamesnews(self.bot)

    @tasks.loop(hours=24)
    async def delete_news(self):
        with open("dictionary_news.json", "r") as f:
            dict_newsa = json.load(f)
        for site, dict in list(dict_newsa.items()):
            for site_news, news in list(dict.items()):
                date = news[1]
                date_news = datetime.datetime.strptime(date, "%Y-%m-%d")
                current_date = datetime.date.today()
                date_difference = current_date - date_news.date()
                if date_difference.days == 10:
                    del dict[site_news]
                    with open("dictionary_news.json", "w") as f:
                        json.dump(dict_newsa, f)

async def setup(bot):
    await bot.add_cog(BotEvents(bot))
