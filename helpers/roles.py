import discord
from discord import Forbidden, HTTPException

def get_role_by_name(name, guild: discord.Guild):
    for role in guild.roles:
        if role.name == name:
            return role

async def add_role(member: discord.Member, rolename: str, reason=None) -> bool:
    guild = member.guild
    try:
        await member.add_roles(get_role_by_name(rolename, guild), reason=reason)
        return True
    except HTTPException:
        return False
    except Forbidden:
        return False

async def remove_role(member: discord.Member, rolename: str, reason=None) -> bool:
    guild = member.guild
    try:
        await member.remove_roles(get_role_by_name(rolename, guild), reason=reason)
        return True
    except HTTPException:
        return False
    except Forbidden:
        return False