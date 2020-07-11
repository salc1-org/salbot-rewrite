"""
Created by Epic at 7/8/20
"""
from random import choice

import discord
from aiohttp import ClientSession, client_exceptions
from discord.ext import commands
import logging

import config


class NicknamePolicy(commands.Cog):
    """Removes nwords from names"""

    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("salbot.cogs.nicknamepolicy")
        self.session = ClientSession()
        self.threshold = .8
        f = open("data/random-names.txt")
        self.random_names = [i.strip() for i in f.readlines()]
        f.close()

    async def predict(self, text):
        payload = {
            "text": [text]
        }
        response = await self.session.post(config.MAX_URL + "/model/predict", json=payload)
        return (await response.json())["results"][0]["predictions"]

    def is_ascii(self, name: str):
        return len(name) == len(name.encode())

    async def is_allowed_nickname(self, member: discord.Member):
        try:
            prediction = await self.predict(member.display_name)
            for name, value in prediction.items():
                if value >= self.threshold:
                    return False, name
        except client_exceptions.ClientConnectionError as e:
            self.logger.warning("Can't connect to MAX")
        if not self.is_ascii(member.display_name):
            return False, "unmentionable name"

        return True, None

    async def process_name(self, member: discord.Member):
        is_allowed, reason = await self.is_allowed_nickname(member)
        if not is_allowed:
            try:
                await member.edit(nick=choice(self.random_names), reason=f"NicknamePolicy [{reason}]")
                await member.send(
                    f"Your nickname in SalC1's discord has been changed. Reason: '{reason}'. Please DM a moderator to appeal this nickname change.")
            except discord.errors.Forbidden:
                pass
            return

    @commands.Cog.listener()
    async def on_member_add(self, member: discord.Member):
        await self.process_name(member)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        await self.process_name(after)


def setup(bot):
    bot.add_cog(NicknamePolicy(bot))
