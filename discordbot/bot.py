import asyncio
from configparser import ConfigParser

import discord
from discord.ext import commands

intents = discord.Intents.all()
client = commands.Bot(command_prefix="]", intents=intents)


config = ConfigParser()
config.read("config.ini")
token = config["bot"]["token"]

# Load extensions (commands and events)
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


async def load_extensions():
    for extension in initial_extensions:
        try:
            await client.load_extension(extension)
        except Exception as e:
            print(f"Failed to load extension {extension}: {e}")


async def main():
    async with client:
        await load_extensions()
        await client.start(token)

if __name__ == "__main__":
    asyncio.run(main())
