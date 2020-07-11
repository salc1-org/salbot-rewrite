"""
Created by Epic at 7/2/20
"""
import logging
import os

import discord
from discord.ext import commands
from discord.ext.commands import ExtensionAlreadyLoaded, ExtensionNotFound, NoEntryPointError, ExtensionFailed

import config
from helpers.permissions import is_dev

bot = commands.Bot("!", allowed_mentions=discord.AllowedMentions(everyone=False, roles=False, users=True))
logger = logging.getLogger("salbot.core")

bot.remove_command("help")


@bot.event
async def on_ready():
    logger.info("Launching SalBot")
    bot.help_command = commands.MinimalHelpCommand()

    #bot.load_extension("jishaku")
    cog_count = [0, 0]
    for cog in os.listdir("cogs/"):
        if not cog.endswith(".py"):
            continue
        cog = cog[:-3]
        logger.debug(f"Loading {cog}")
        try:
            bot.load_extension("cogs." + cog)
            cog_count[1] += 1
        except ExtensionNotFound:
            logger.error(f"Failed to load cog {cog} - Not Found", exc_info=True)
        except ExtensionAlreadyLoaded:
            logger.error(f"Failed to load cog {cog} - Already Loaded", exc_info=True)
        except NoEntryPointError:
            logger.error(f"Failed to load cog {cog} - No Setup Function", exc_info=True)
        except ExtensionFailed:
            logger.error(f"Failed to load cog {cog}", exc_info=True)
        finally:
            cog_count[0] += 1

    logger.info(f"Successfully loaded {cog_count[1]} cogs ({cog_count[0]} total)")


@bot.command(name="reload")
@is_dev()
async def reload(ctx):
    logger.info("Reloading SalBot")

    for cog in os.listdir("cogs/"):
        if not cog.endswith(".py"):
            continue
        cog = cog[:-3]
        logger.debug(f"Reloading {cog}")
        try:
            bot.reload_extension("cogs." + cog)
        except ExtensionNotFound:
            logger.error(f"Failed to load cog {cog} - Not Found", exc_info=True)
        except ExtensionAlreadyLoaded:
            logger.error(f"Failed to load cog {cog} - Already Loaded", exc_info=True)
        except NoEntryPointError:
            logger.error(f"Failed to load cog {cog} - No Setup Function", exc_info=True)
        except ExtensionFailed:
            logger.error(f"Failed to load cog {cog}", exc_info=True)


try:
    bot.run(config.TOKEN)
except RuntimeError:
    pass
raise ConnectionAbortedError
