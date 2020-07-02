"""
Created by Epic at 7/2/20
"""
from discord.ext import commands
import discord
import typing
import logging


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.logger = logging.getLogger("salbot.moderation")

    @commands.command(aliases=["b", "plonk"])
    @commands.has_any_role("Administrator", "Moderator")
    async def ban(self, ctx, user: typing.Union[discord.Member, discord.User], reason=None):
        await ctx.guild.ban(user, reason=reason)
        await ctx.message.delete()
        embed = discord.Embed()
        embed.colour = 0xFF0000
        embed.description = f"Banned {user.mention}!"
        await ctx.send(embed=embed)

    @ban.error
    async def userinfo_error(self, ctx, error):
        if isinstance(error, commands.errors.BadUnionArgument):
            await ctx.send("User not found")
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("Invalid syntax")
        elif isinstance(error, discord.HTTPException):
            await ctx.send("I don't have permission to ban this user!")
        else:
            self.logger.error("Error during ban command", exc_info=error)

    @commands.command(aliases=["k", "yeet"])
    @commands.has_any_role("Administrator", "Moderator")
    async def kick(self, ctx, user: discord.Member, reason=None):
        await user.kick(reason=reason)
        await ctx.message.delete()
        embed = discord.Embed()
        embed.colour = 0xFFFF00
        embed.description = f"Kicked {user.mention}!"
        await ctx.send(embed=embed)

    @kick.error
    async def userinfo_error(self, ctx, error):
        if isinstance(error, commands.errors.BadArgument):
            await ctx.send("User not found")
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("Invalid syntax")
        elif isinstance(error, discord.HTTPException):
            await ctx.send("I don't have permission to ban this user!")
        else:
            self.logger.error("Error during ban command", exc_info=error)


def setup(client):
    client.add_cog(Moderation(client))
