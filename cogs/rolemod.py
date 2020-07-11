"""
Created by vcokltfre at 2020-07-11
"""
import logging

from discord.ext import commands
from discord.ext.commands import has_any_role
import discord
from helpers.roles import add_role, remove_role


class RoleMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("salbot.rolemod")
        
    @commands.group(name="rolemod")
    @has_any_role("Moderator", "Administrator")
    async def rolemod(self, ctx):
        pass

    @rolemod.command(name="add")
    async def rm_add(self, ctx, member: discord.Member, *rolename):
        name = " ".join(rolename)
        await add_role(member, name, "rolemod")

    @rolemod.command(name="remove", aliases=["rm", "delete"])
    async def rm_remove(self, ctx, member: discord.Member, *rolename):
        name = " ".join(rolename)
        await remove_role(member, name, "rolemod")


def setup(bot):
    bot.add_cog(RoleMod(bot))
