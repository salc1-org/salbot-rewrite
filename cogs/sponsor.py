"""
Created by Epic at 8/18/20
"""
import logging

from discord.ext import commands
import discord


class Sponsor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("salbot.cogs.sponsor")

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if before.roles == after.roles:
            return
        before_role_names = [i.name for i in before.roles]
        if "YouTube Member" in before_role_names and "YouTube Sponsor" not in before_role_names:
            sponsor_role = discord.utils.get(before.guild.roles, name="YouTube Sponsor")
            await before.add_roles(sponsor_role, reason="AutoSponsor")
            self.logger.info(f"Gave YouTube sponsor role to {before} ({before.id})")


def setup(bot):
    bot.add_cog(Sponsor(bot))