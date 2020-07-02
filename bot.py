"""
Created by Epic at 7/2/20
"""
import discord
from discord.ext import commands
import config
import logging
import os

client = commands.Bot("!", allowed_mentions=discord.AllowedMentions(everyone=False, roles=False, users=True))
logger = logging.getLogger("salbot.core")

client.remove_command("help")


@client.event
async def on_ready():
    logger.info("Salbot launched")
    client.help_command = commands.MinimalHelpCommand()

    for cog in os.listdir("cogs/"):
        if not cog.endswith(".py"):
            continue
        cog = cog[:-3]
        logger.debug(f"Loading {cog}")
        client.load_extension("cogs." + cog)

try:
    client.run(config.TOKEN)
except RuntimeError:
    pass
raise ConnectionAbortedError
