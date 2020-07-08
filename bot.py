"""
Created by Epic at 7/2/20
"""
import discord
from discord.ext import commands
from discord.ext.commands import has_any_role
import config
import logging
import os
from helpers.permissions import developer

bot = commands.Bot("!", allowed_mentions=discord.AllowedMentions(everyone=False, roles=False, users=True))
logger = logging.getLogger("salbot.core")

bot.remove_command("help")


@bot.event
async def on_ready():
    logger.info("Launching SalBot")
    bot.help_command = commands.MinimalHelpCommand()

    for cog in os.listdir("cogs/"):
        if not cog.endswith(".py"):
            continue
        cog = cog[:-3]
        logger.debug(f"Loading {cog}")
        try:
            bot.load_extension("cogs." + cog)
        except:
            logger.error(f"Failed to load cog {cog}", exc_info=True)

@bot.command(name="reload")
@developer
async def reload(ctx):
    logger.info("Reloading SalBot")

    for cog in os.listdir("cogs/"):
        if not cog.endswith(".py"):
            continue
        cog = cog[:-3]
        logger.debug(f"Reloading {cog}")
        try:
            bot.reload_extension("cogs." + cog)
        except:
            logger.error(f"Failed to reload cog {cog}", exc_info=True)

try:
    bot.run(config.TOKEN)
except RuntimeError:
    pass
raise ConnectionAbortedError
