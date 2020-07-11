"""
Created by Epic at 7/2/20
"""
import logging
import typing

import discord
from discord.ext import commands


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("salbot.cogs.info")

    @commands.command(name="userinfo", aliases=["ui", "user"])
    async def user_info(self, ctx, user: typing.Union[discord.Member, discord.User]):
        embed = discord.Embed(color=0x00FFFF)
        embed.set_author(name=str(user), icon_url=user.avatar_url)
        embed.add_field(name="UserID", value=user.id, inline=True)
        embed.add_field(name="In server", value="yes" if isinstance(user, discord.Member) else "no")
        embed.add_field(name="Created at", value=user.created_at.strftime('%A, %d. %B %Y @ %H:%M:%S'), inline=True)
        if isinstance(user, discord.Member):
            embed.add_field(name="Joined at", value=user.joined_at.strftime('%A, %d. %B %Y @ %H:%M:%S'), inline=True)
        await ctx.send(embed=embed)

    @user_info.error
    async def userinfo_error(self, ctx, error):
        if isinstance(error, commands.errors.BadUnionArgument):
            await ctx.send("User not found")
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await self.user_info(ctx, user=ctx.author)


def setup(bot):
    bot.add_cog(Info(bot))
