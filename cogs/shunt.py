"""
Created by vcokltfre at 2020-07-08
"""
from discord.ext import commands
from discord.ext.commands import has_any_role
import discord
import logging
from datetime import datetime


class Shunt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("salbot.shunt")

    @commands.command(name="shunt", aliases=["clownpull"])
    @has_any_role("Administrator", "Moderator")
    async def shunt(self, ctx, channel_to, *channels_from):
        ''' Move users from many channels to one '''
        to = self.bot.get_channel(int(channel_to))
        members = []
        for channel in channels_from:
                for member in self.bot.get_channel(int(channel)).members:
                    members.append(member)
        for member in members:
            await member.move_to(to, reason="Shunting")
        await ctx.channel.send(f"Moved {len(members)} members to {to}")
        self.logger.info(f"Moved {len(members)} members to {to}")


def setup(bot):
    bot.add_cog(Shunt(bot))
