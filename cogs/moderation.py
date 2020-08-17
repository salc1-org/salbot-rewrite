"""
Created by Epic at 7/2/20
"""
import logging
import typing

from helpers.converters import UserFriendlyTime
import discord
from discord.ext import commands, tasks
from discord.ext.commands import has_any_role
import config
from datetime import datetime
from jishaku.paginators import PaginatorEmbedInterface
from discord.ext.commands import Paginator


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("salbot.cogs.moderation")
        self.api = self.bot.get_cog("Api")

        self.autopardon_loop.start()

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
                      time: UserFriendlyTime(commands.clean_content, default='\u2026'), *, reason: str = None):
        time = time.dt
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
                   time: UserFriendlyTime(commands.clean_content, default='\u2026'), *, reason: str = None):
        time = time.dt
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
            for punishment in await self.api.get_punishments(user.id):
                punishment_type = punishment["punishment_type"].lower()
                if punishment_type == "ban":
                    try:
                        await ctx.guild.unban(user)
                    except:
                        pass
                    await self.api.mark_punishment_as_expired()
                elif punishment_type == "mute":
                    if isinstance(user, discord.Member):
                        try:
                            await user.remove_roles(muted_role, reason="Pardoned")
                        except:
                            pass
                    await self.api.mark_punishment_as_expired(punishment["punishment_id"])
        await ctx.send("Done")

    @commands.command()
    async def history(self, ctx, user: discord.User):
        punishments = await self.api.get_punishments(user_id=user.id)
        paginator = PaginatorEmbedInterface(self.bot, paginator=Paginator(prefix="", suffix=""))

        for punishment in punishments:
            # TODO: This code is awful, please shorten it.
            formatted = f"**{punishment['punishment_type']}** " \
                        f"({punishment['punishment_id']}) - {punishment['reason']} by <@{punishment['moderator_id']}>"
            await paginator.add_line(formatted)
        if paginator.page_count == 0:
            await paginator.add_line("This user doesn't have any punishments!")
        await paginator.send_to(ctx)

    @tasks.loop(seconds=10)
    async def autopardon_loop(self):
        guild = await self.bot.fetch_guild(config.GUILD_ID)
        muted_role = discord.utils.get(guild.roles, name="Muted")
        current_time = datetime.now()
        punishments = await self.api.get_punishments()
        for punishment in punishments:
            expires_at = datetime.fromtimestamp(punishment["expires_at"])
            if current_time > expires_at and not punishment["expired"]:
                punishment_type = punishment["punishment_type"].lower()
                if punishment_type == "ban":
                    try:
                        await self.bot.http.unban(punishment["punished_id"], guild.id,
                                                  reason="[Auto] Punishment expired")
                    except:
                        pass
                    await self.api.mark_punishment_as_expired()
                elif punishment_type == "mute":
                    try:
                        await self.bot.http.remove_role(guild.id, punishment["punished_id"], muted_role.id,
                                                        reason="[Auto] Punishment expired")
                    except:
                        pass
                    await self.api.mark_punishment_as_expired(punishment["punishment_id"])


def setup(bot):
    bot.add_cog(Moderation(bot))
