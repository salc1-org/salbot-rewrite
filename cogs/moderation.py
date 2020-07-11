"""
Created by Epic at 7/2/20
"""
import logging
import typing

import discord
from discord.ext import commands
from discord.ext.commands import has_any_role

from helpers.roles import add_role, remove_role


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("salbot.cogs.moderation")

    @commands.command(aliases=["b", "plonk"])
    @has_any_role("Administrator", "Moderator")
    async def ban(self, ctx, user: typing.Union[discord.Member, discord.User], reason=None):
        await ctx.guild.ban(user, reason=reason)
        await ctx.message.delete()
        embed = discord.Embed()
        embed.colour = 0xFF0000
        embed.description = f"Banned {user.mention}!"
        await ctx.send(embed=embed)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.errors.BadUnionArgument):
            await ctx.send("User not found")
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("Invalid syntax")
        elif isinstance(error, discord.HTTPException):
            await ctx.send("I don't have permission to ban this user!")
        else:
            self.logger.error("Error during ban command", exc_info=error)

    @commands.command(aliases=["k", "yeet"])
    @has_any_role("Administrator", "Moderator")
    async def kick(self, ctx, user: discord.Member, reason=None):
        await user.kick(reason=reason)
        await ctx.message.delete()
        embed = discord.Embed()
        embed.colour = 0xFFFF00
        embed.description = f"Kicked {user.mention}!"
        await ctx.send(embed=embed)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.errors.BadArgument):
            await ctx.send("User not found")
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("Invalid syntax")
        elif isinstance(error, discord.HTTPException):
            await ctx.send("I don't have permission to kick this user!")
        else:
            self.logger.error("Error during kick command", exc_info=error)

    # Temporary mute command filler, will be replaced with a more comprehensive system soon
    @commands.command(name="mute", aliases=["silence"])
    @has_any_role("Administrator", "Moderator")
    async def mute(self, ctx, member: discord.Member):
        success = await add_role(member, "Muted", reason="This user has been muted by staff")

        if success:
            await ctx.channel.send(f"Successfully muted {member}")
        else:
            await ctx.channel.send(f"Couldn't mute {member}")

    # Temporary unmute command filler, will be replaced with a more comprehensive system soon
    @commands.command(name="unmute")
    @has_any_role("Administrator", "Moderator")
    async def unmute(self, ctx, member: discord.Member):
        success = await remove_role(member, "Muted", reason="This user has been unmuted by staff")

        if success:
            await ctx.channel.send(f"Successfully unmuted {member}")
        else:
            await ctx.channel.send(f"Couldn't unmute {member}")

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.errors.BadArgument):
            await ctx.send("User not found")
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("Invalid syntax")
        else:
            self.logger.error("Error during mute command", exc_info=error)

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.errors.BadArgument):
            await ctx.send("User not found")
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("Invalid syntax")
        else:
            self.logger.error("Error during unmute command", exc_info=error)


def setup(bot):
    bot.add_cog(Moderation(bot))
