"""
Created by Epic at 7/2/20
"""

# Not sure if we are going to be using docker, if we are we can throw away most of this script

import logging
from color_format import basicConfig
import discord

core_logger = logging.getLogger("salbot")
core_logger.setLevel(logging.DEBUG)
basicConfig(core_logger)

launcher_logger = logging.getLogger("salbot.launcher")

launcher_logger.info("Starting salbot")
while True:
    try:
        import bot
    except Exception as e:
        launcher_logger.error("Salbot failed to load")
        raise e
    launcher_logger.info("Salbot crashed, restarting")
