"""
Created by Epic at 7/2/20
"""

# Not sure if we are going to be using docker, if we are we can throw away most of this script

import logging

import sentry_sdk
import subprocess

from color_format import colorFormat
from discord_logger import DiscordFormatter

core_logger = logging.getLogger("salbot")
core_logger.setLevel(logging.DEBUG)
colorFormat(core_logger)
core_logger.addHandler(DiscordFormatter())

launcher_logger = logging.getLogger("salbot.launcher")

launcher_logger.info("Starting salbot")

# Sentry
commit_hash = subprocess.check_output(["/usr/bin/git", "rev-parse", "--short", "HEAD"]).decode("utf-8").strip()
sentry_sdk.init("https://4440e793db8c4d4b810adb8f161980e1@sentry.farfrom.world/2", release=commit_hash)
launcher_logger.debug(f"Started sentry with commit hash {commit_hash}")


while True:
    try:
        import bot
    except Exception as e:
        if isinstance(e, ConnectionAbortedError):
            launcher_logger.info("Shutting down salbot")
            break
        launcher_logger.critical("Salbot failed to load", exc_info=e)
        break
    launcher_logger.info("Salbot crashed, restarting!")
