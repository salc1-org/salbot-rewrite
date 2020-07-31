"""
Created by Epic at 7/2/20
"""
import logging
import typing

import discord
from discord.ext import commands
from discord.ext.commands import has_any_role


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("salbot.cogs.moderation")
        self.api = self.bot.get_cog("Api")

    @commands.command(aliases=["b", "plonk"])
    @has_any_role("Administrator", "Moderator")
    async def ban(self, ctx, users: commands.Greedy[typing.Union[discord.Member, discord.User]], *, reason: str = None):
        for user in users:
            await ctx.guild.ban(user, reason=reason)
            await ctx.message.delete()
            embed = discord.Embed()
            embed.colour = 0xFF0000
            embed.description = f"Banned {user.mention}!"
            await ctx.send(embed=embed)
            await self.api.create_punishment(punishment_type="ban", punished_id=user.id, moderator_id=ctx.author.id,
                                             expires_at=None, reason=reason)


def setup(bot):
    bot.add_cog(Moderation(bot))
