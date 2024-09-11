from discord.ext import commands

from discordbot.utils.helpers import get_metacritic


class GameCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def metacritic(self, ctx, *, game):
        text = get_metacritic(game)
        await ctx.send(text)


async def setup(bot):
    await bot.add_cog(GameCommands(bot))
