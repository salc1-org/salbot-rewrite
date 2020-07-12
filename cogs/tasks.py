import discord
from discord.ext import commands, tasks

import time

from api import api
from helpers.roles import remove_role

class Tasks(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.cached_guilds = {}
        self.unmute_loop.start()

    @tasks.loop(seconds=180)
    async def unmute_loop(self):
        mutes = api.getmutes()
        for muted_user in mutes:
            if muted_user["end"] < round(time.time()):
                if muted_user["guild"] not in self.cached_guilds:
                    self.cached_guilds[muted_user["guild"]] = self.bot.get_guild(muted_user["guild"])
                member = self.cached_guilds[muted_user["guild"]].get_member(muted_user["uid"])
                await remove_role(member, "Muted", "Automatic unmute: Mute expired")
                api.unmute(muted_user["uid"])


def setup(bot: commands.Bot):
    bot.add_cog(Tasks(bot))