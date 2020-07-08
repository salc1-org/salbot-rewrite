"""
Created by vcokltfre at 2020-07-08
"""
import discord
import functools
from discord.ext import commands


def is_mod_or_dev():
    developer_ids = [397745647723216898, 297045071457681409, 151347084602245120]
    moderator_roles = ["Administrator", "Moderator"]

    async def check(ctx):
        if any([i.name in moderator_roles for i in ctx.author.roles]) or ctx.author.id in developer_ids:
            return True
        raise commands.errors.MissingPermissions(["MODERATOR"])

    return commands.check(check)

def is_dev():
    developer_ids = [397745647723216898, 297045071457681409, 151347084602245120]

    async def check(ctx):
        if ctx.author.id in developer_ids:
            return True
        raise commands.errors.MissingPermissions(["DEVELOPER"])

    return commands.check(check)