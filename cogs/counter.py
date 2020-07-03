"""
Created by Epic at 7/3/20
"""
from discord.ext import commands
import logging


class AutoResponder(commands.Cog):
    def __init__(self, client):
        self.client = client
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


def setup(client):
    client.add_cog(AutoResponder(client))
