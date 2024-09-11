# events/message_events.py

from discord.ext import commands


class MessageEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == self.bot.user.id:
            return
        if "hello" == message.content.lower():
            await message.channel.send(f"Hello {message.author.mention}!")


async def setup(bot):
    await bot.add_cog(MessageEvents(bot))
