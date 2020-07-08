"""
Created by vcokltfre at 2020-07-08
"""
from discord.ext import commands
from discord.ext.commands import has_any_role
import discord
import logging
import time
from datetime import timedelta, datetime
import json


class BotInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("salbot.botinfo")
        self.uptime_start = round(time.time())
        self.socket_stats = {}
        self.opcodes = {
            10: "Hello",
            11: "HEARTBEAT",
            9: "HI",
            7: "RECONNECT"
        }

    @commands.Cog.listener()
    async def on_socket_response(self, data):
        t = data["t"]
        if not t:
            try:
                t = self.opcodes[data["op"]]
            except KeyError:
                self.logger.warning(f"Unknown opcode. Received: {data['op']}")
        self.socket_stats[t] = self.socket_stats.get(t, 0) + 1

    @commands.command(name="stats")
    @has_any_role("Administrator", "Moderator")
    async def stats_bot(self, ctx, typ="raw"):
        if typ == "raw":
            jsd = json.dumps(self.socket_stats, indent=4)
            desc = f"```json\n{jsd}```"
            embed = discord.Embed(title="Raw Socket Stats", color=0xFF0000, description=desc, timestamp=datetime.now())
            await ctx.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(BotInfo(bot))
