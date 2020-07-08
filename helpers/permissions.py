"""
Created by vcokltfre at 2020-07-08
"""
import discord
import functools


class PermissionsError(Exception):
    pass


devs = [397745647723216898, 297045071457681409, 151347084602245120]


def developer(func):
    @functools.wraps(func)
    async def wrap_int(*args, **kwargs):
        author = args[1].author
        usroles = [role.name for role in author.roles]
        if not "Administrator" in usroles or "Moderator" in usroles or author.id in devs:
            raise PermissionsError(f"{author} is not a mod, admin, or dev.")
        return await func(*args, **kwargs)

    return wrap_int
