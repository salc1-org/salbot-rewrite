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
        client.load_extension("cogs." + cog)


client.run(config.token)
