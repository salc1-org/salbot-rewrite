"""
Created by Epic at 7/2/20
"""
import logging

from discord.ext import commands


class Faq(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("salbot.cogs.faq")
        self.api = self.bot.get_cog("Api")

    @commands.command(aliases=["dgl", "tos"])
    async def faq(self, ctx, entry):
        answer = await self.api.get_faq(entry)
        if answer is None:
            return await ctx.send("Not found.")
        await ctx.send("> " + answer)

    @commands.command()
    @commands.has_any_role("Moderator", "Administrator")
    async def createfaq(self, ctx, name, *, description):
        await self.api.create_faq(name, description)
        await ctx.send("Done")


def setup(bot):
    bot.add_cog(Faq(bot))
