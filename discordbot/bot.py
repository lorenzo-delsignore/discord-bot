import asyncio
from configparser import ConfigParser

import discord
from discord.ext import commands


async def main():
    intents = discord.Intents.all()
    client = commands.Bot(command_prefix="]", intents=intents)
    config = ConfigParser()
    config.read("config.ini")
    token = config["bot"]["token"]
    initial_extensions = [
        "discordbot.commands.game_commands",
        "discordbot.commands.admin_commands",
        "discordbot.commands.news_commands",
        "discordbot.commands.search_commands",
        "discordbot.commands.sport_commands",
        "discordbot.events.bot_events",
        "discordbot.events.message_events",
        "discordbot.events.member_events",
    ]
    async with client:
        for extension in initial_extensions:
            try:
                await client.load_extension(extension)
            except Exception as e:
                print(f"Failed to load extension {extension}: {e}")
        await client.start(token)


if __name__ == "__main__":
    asyncio.run(main())
