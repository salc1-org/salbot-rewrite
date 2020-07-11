"""
Created by Epic at 7/2/20
"""
import logging

from discord.ext import commands


class Faq(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("salbot.cogs.faq")
        self.questions = [
            {
                "aliases": ["tos", "terms", "termsofservice"],
                "text": "Read the discord terms of service at https://discord.com/terms"
            },
            {
                "aliases": ["dgl", "guidelines", "discordguidelines"],
                "text": "Read the discord guidelines at https://discord.com/guidelines"
            },
            {
                "aliases": ["dupe"],
                "text": "Please do not mention duping on servers that do not allow it as it's against Discord's ToS."
            }
        ]
        self.mappped_questions = {}

        for question in self.questions:
            for alias in question["aliases"]:
                self.mappped_questions[alias] = question["text"]

    @commands.command(aliases=["dgl", "tos"])
    async def faq(self, ctx, entry=None):
        if entry is None:
            description = ""
            description += "**FAQ Commands:**\n```md\n"
            for question in self.questions:
                description += f"+ {question['aliases'][0]}\n"
            description += "```"
            await ctx.send(description)
            return
        text = ""
        if entry not in self.mappped_questions.keys():
            return await ctx.send("Not found.")
        for splitted in self.mappped_questions[entry].split("\n"):
            text += f"> {splitted}\n"
        await ctx.send(text)


def setup(bot):
    bot.add_cog(Faq(bot))
