"""
Created by Epic at 7/2/20
"""

# Not sure if we are going to be using docker, if we are we can throw away most of this script

import logging
import subprocess

import sentry_sdk

from color_format import colorFormat
from config import SENTRY_URL
from discord_logger import DiscordFormatter

core_logger = logging.getLogger("salbot")
core_logger.setLevel(logging.DEBUG)
colorFormat(core_logger)
core_logger.addHandler(DiscordFormatter())

launcher_logger = logging.getLogger("salbot.launcher")

launcher_logger.info("Starting salbot")

# Sentry
if SENTRY_URL:
    commit_hash = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode("utf-8").strip()
    sentry_sdk.init(SENTRY_URL, release=commit_hash)
    launcher_logger.debug(f"Started sentry with commit hash {commit_hash}")

while True:
    try:
        import bot
    except Exception as e:
        if isinstance(e, ConnectionAbortedError):
            launcher_logger.info("Shutting down SalBot")
            break
        launcher_logger.critical("Salbot failed to load", exc_info=e)
        break
    launcher_logger.info("Salbot crashed, restarting!")
