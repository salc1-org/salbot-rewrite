"""
Created by Epic at 8/17/20
"""

import logging
import discord
from discord.ext import commands


class MemberRankup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("salbot.cogs.memberrankup")

    @commands.command()
    @commands.has_any_role("Administrator", "Moderator", "Private Chat Access")
    async def addmember(self, ctx, user: discord.Member):
        member_role = discord.utils.get(ctx.guild.roles, name="Member")
        await user.add_roles(member_role, reason=f"[Command] Add member requested by {ctx.author}")
        await ctx.send("👌")
        self.logger.info(f"Added member to {user}. Requested by {ctx.author}")

    @commands.command()
    @commands.has_any_role("Administrator", "Moderator", "Private Chat Access")
    async def removemember(self, ctx, user: discord.Member):
        member_role = discord.utils.get(ctx.guild.roles, name="Member")
        await user.remove_roles(member_role, reason=f"[Command] Remove member requested by {ctx.author}")
        await ctx.send("👌")
        self.logger.info(f"Removed member from {user}. Requested by {ctx.author}")


def setup(bot):
    bot.add_cog(MemberRankup(bot))
