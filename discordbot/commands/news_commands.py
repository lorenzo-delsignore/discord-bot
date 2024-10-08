from discord.ext import commands

from discordbot.utils.news import get_gamenews


class NewsCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def gamenews(self, ctx):
        news = await get_gamenews()
        await ctx.send(news)


async def setup(bot):
    await bot.add_cog(NewsCommands(bot))
