from discord.ext import commands

from discordbot.utils.helpers import get_f1, get_f1team, get_motogp, get_motogpteam, get_seriea


class SportCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def seriea(self, ctx):
        text = get_seriea()
        await ctx.send(text)

    @commands.command()
    async def f1(self, ctx):
        text = get_f1()
        await ctx.send(text)

    @commands.command()
    async def f1team(self, ctx):
        text = get_f1team()
        await ctx.send(text)

    @commands.command()
    async def motogp(self, ctx):
        text = get_motogp()
        await ctx.send(text)

    @commands.command()
    async def motogpteam(self, ctx):
        text = get_motogpteam()
        await ctx.send(text)


async def setup(bot):
    await bot.add_cog(SportCommands(bot))
