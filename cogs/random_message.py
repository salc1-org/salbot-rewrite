"""
Created by vcokltfre at 2020-07-08
"""
from discord.ext import commands
from discord.ext.commands import has_any_role
import discord
import logging
from random import randint


class RandomMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("salbot.random_message")
        self.ids = {
            "maze":373946864531144726,
            "vco":297045071457681409
        }

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        author = message.author.id
        mention = f"<@{author}>"
        rnd_int = randint(0,150)

        if author == self.ids["maze"]:
            if rnd_int == 75:
                await message.channel.send(f"Fuck you {mention}")
            elif rnd_int == 123:
                await message.channel.send(f"Do you like Alex Dillinger, {mention}?")

        elif author == self.ids["vco"]:
            if rnd_int == 65:
                await message.channel.send(f"Tired of pinging everyone yet, {mention}?")


def setup(bot):
    bot.add_cog(RandomMessage(bot))
