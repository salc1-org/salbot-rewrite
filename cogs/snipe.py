"""
Created by vcokltfre at 2020-07-08
"""
import logging

import discord
from discord.ext import commands
from discord.ext.commands import has_any_role

from helpers.data_struct import MessageQueue


class Snipe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("salbot.cogs.botinfo")
        self.deletes = {}

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        mid = message.channel.id
        if str(mid) in self.deletes:
            self.deletes[str(mid)].add(message)
        else:
            self.deletes[str(mid)] = MessageQueue(10)
            self.deletes[str(mid)].add(message)

    @commands.command(name="snipe")
    @has_any_role("Administrator", "Moderator")
    async def snipe(self, ctx, amount=1):
        mid = ctx.channel.id
        if not str(mid) in self.deletes:
            await ctx.channel.send("There is nothing to snipe here!")
            return

        if len(self.deletes[str(mid)].messages) < amount:
            amount = len(self.deletes[str(mid)].messages)

        embed = discord.Embed(title=f"Snipe of last {amount} messages", color=0xFFFF00)
        for i in range(amount):
            item = self.deletes[str(mid)].pop()
            embed.add_field(name=f"{item.author}",
                            value=f"{item.content}", inline=False)

        await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Snipe(bot))
