"""
Created by Epic at 7/2/20
"""
from discord.ext import commands
import discord
import logging
import googletrans


class AutoTranslation(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.logger = logging.getLogger("salbot.autotranslation")
        self.translator = googletrans.Translator()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not message.guild:
            return
        detected = self.translator.detect(message.content)
        if detected.confidence < .5:
            return

        translated = self.translator.translate(message.content)
        if translated.src == "en" or translated.text == message.content:
            return
        await message.channel.send(translated.text)



def setup(client):
    client.add_cog(AutoTranslation(client))
