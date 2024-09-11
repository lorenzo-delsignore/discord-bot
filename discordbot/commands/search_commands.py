from discord.ext import commands

from discordbot.utils.helpers import get_googlesearch


class SearchCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def google(ctx, *, question):
        text = get_googlesearch(question)
        await ctx.send(text)


async def setup(bot):
    await bot.add_cog(SearchCommands(bot))
