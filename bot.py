"""
Created by Epic at 7/2/20
"""
import discord
from discord.ext import commands
import config

client = commands.Bot("!", allowed_mentions=discord.AllowedMentions(everyone=False, roles=False, users=True))

client.run(config.token)