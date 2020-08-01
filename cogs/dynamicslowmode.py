"""
Created by Epic at 8/1/20
"""
import logging
import asyncio
import discord
from discord.ext import commands
from aiohttp import client_exceptions


class DynamicSlowmode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("salbot.cogs.faq")
        self.api = self.bot.get_cog("Api")
        self.toxicity_threshold = .7

        self.normal_cooldown_mapping = commands.CooldownMapping.from_cooldown(3, 5, commands.BucketType.channel)
        self.toxicity_cooldown_mapping = commands.CooldownMapping.from_cooldown(2, 5, commands.BucketType.channel)
        self.normal_cooldown = 10
        self.toxicity_cooldown = 20
        self.default_cooldown = 0

        self.cooldown_time = 60

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        try:
            toxicity_result = await self.api.predict_toxicity(message.content)
            is_toxic = False
            for value in toxicity_result.values():
                if value > self.toxicity_threshold:
                    is_toxic = True
                    break
        except client_exceptions.ClientConnectionError:
            self.logger.warning("Could not connect to MAX")
            is_toxic = False
        if is_toxic:
            rate_limit = self.toxicity_cooldown_mapping.update_rate_limit(message)

            if rate_limit and message.channel.slowmode_delay < self.toxicity_cooldown:
                embed = discord.Embed(title="[Auto] Chat suspended",
                                      description="The chat has been automatically suspended for toxicity.", color=0xFF0000)
                await message.channel.send(embed=embed, delete_after=10)
                await message.channel.edit(slowmode_delay=self.toxicity_cooldown)
                await asyncio.sleep(self.cooldown_time)
                await message.channel.edit(slowmode_delay=self.cooldown_time)
        else:
            rate_limit = self.normal_cooldown_mapping.update_rate_limit(message)

            if rate_limit and message.channel.slowmode_delay < self.normal_cooldown:
                embed = discord.Embed(title="[Auto] Chat suspended",
                                      description="The chat has been automatically suspended.", color=0xFF0000)
                await message.channel.send(embed=embed, delete_after=10)
                await message.channel.edit(slowmode_delay=self.normal_cooldown)
                await asyncio.sleep(self.cooldown_time)
                await message.channel.edit(slowmode_delay=self.cooldown_time)


def setup(bot):
    bot.add_cog(DynamicSlowmode(bot))
