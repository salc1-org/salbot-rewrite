"""
Created by Epic at 7/8/20
"""
from random import choice

import discord
from aiohttp import ClientSession
from discord.ext import commands

import config


class AntiOffend(commands.Cog):
    """Removes nwords from names"""

    def __init__(self, bot):
        self.bot = bot
        self.session = ClientSession()
        self.threshold = .5
        f = open("data/random-names.txt")
        self.random_names = [i.strip() for i in f.readlines()]
        f.close()

    async def predict(self, text):
        payload = {
            "text": [text]
        }
        response = await self.session.post(config.MAX_URL + "/model/predict", json=payload)
        return (await response.json())["results"][0]["predictions"]

    async def process_name(self, member: discord.Member):
        prediction = await self.predict(member.display_name)
        role = discord.utils.get(member.guild.roles, name="Muted")
        if role in member.roles:
            return

        for name, value in prediction.items():
            if value >= self.threshold:
                await member.edit(nick=choice(self.random_names), reason=f"AntiOffend [{name}]")
                await member.add_roles(role, reason=f"AntiOffend [{name}]")
                try:
                    await member.send(
                        f"Your nickname in Salc1's discord has been changed. Reason: '{name}'. Please DM a moderator to appeal this nickname change.")
                except discord.errors.Forbidden:
                    pass
                return
        if member.display_name[0].lower() < "0":
            await member.edit(nick=choice(self.random_names), reason=f"AntiHoisting")
            try:
                await member.send(
                    f"Your nickname in Salc1's discord has been changed. Reason: 'hoisting'. Please DM a moderator to appeal this nickname change.")
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
    bot.add_cog(AntiOffend(bot))
