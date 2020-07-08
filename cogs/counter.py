"""
Created by Epic at 7/3/20
"""
import logging

from discord.ext import commands


class AutoResponder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("salbot.faq")
        self.counters = {}

    @commands.command()
    @commands.has_any_role("Administrator", "Moderator")
    async def startcounter(self, ctx, startvalue: int = 1):
        await ctx.message.delete()
        self.counters[ctx.channel.id] = startvalue

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id not in self.counters.keys():
            return
        try:
            val = int(message.content.split(" ")[0])
        except ValueError:
            await message.delete()
            return

        if val != self.counters[message.channel.id]:
            await message.delete()
            return
        self.counters[message.channel.id] += 1


def setup(bot):
    bot.add_cog(AutoResponder(bot))
