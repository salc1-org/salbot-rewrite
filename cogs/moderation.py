"""
Created by Epic at 7/2/20
"""
import logging
import typing

from helpers.converters import UserFriendlyTime
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

    @commands.command(aliases=["tb"])
    @has_any_role("Administrator", "Moderator")
    async def tempban(self, ctx, users: commands.Greedy[typing.Union[discord.Member, discord.User]],
                      time: UserFriendlyTime, *, reason: str = None):
        for user in users:
            await ctx.guild.ban(user, reason=reason)
            await ctx.message.delete()
            embed = discord.Embed()
            embed.colour = 0xFF0000
            embed.description = f"Banned {user.mention}!"
            await ctx.send(embed=embed)
            await self.api.create_punishment(punishment_type="ban", punished_id=user.id, moderator_id=ctx.author.id,
                                             expires_at=time, reason=reason)
        await ctx.send("Done")

    @commands.command()
    @has_any_role("Administrator", "Moderator")
    async def mute(self, ctx, users: commands.Greedy[typing.Union[discord.Member, discord.User]],
                   time: UserFriendlyTime, *, reason: str = None):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        for user in users:
            await user.add_roles(muted_role, reason="Muted")
            await self.api.create_punishment(punishment_type="mute", punished_id=user.id, moderator_id=ctx.author.id,
                                             expires_at=time, reason=reason)
        await ctx.send("Done")

    @commands.command()
    @has_any_role("Administrator", "Moderator")
    async def pardon(self, ctx: commands.Context, users: commands.Greedy[typing.Union[discord.Member, discord.User]]):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        for user in users:
            for punishment in self.api.get_punishments(user.id):
                punishment_type = punishment["punishment_type"]
                if punishment_type == "ban":
                    try:
                        await ctx.guild.unban(user)
                    except:
                        pass
                    await self.api.mark_punishment_as_expired()
                elif punishment_type == "unmute":
                    if isinstance(user, discord.Member):
                        try:
                            await user.remove_roles(muted_role, reason="Pardoned")
                        except:
                            pass
                    await self.api.mark_punishment_as_expired()
        await ctx.send("Done")


def setup(bot):
    bot.add_cog(Moderation(bot))
