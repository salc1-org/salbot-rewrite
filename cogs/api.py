"""
Created by Epic at 7/14/20
"""

import logging

import discord
from discord.ext import commands
from aiohttp import ClientSession
import config
from datetime import datetime, timedelta


class Api(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("salbot.cogs.api")
        self.authentication_headers = {"Authorization": config.API_TOKEN}
        self.session = ClientSession()

    class ApiException(BaseException):
        def __init__(self, message):
            pass

    async def get_bans(self, *, banned=None, moderator=None):
        query = {
            "banned": banned,
            "moderator": moderator
        }
        params = query.copy()
        for key, value in query.items():
            if value is None:
                del params[key]

        response = await self.session.get(f"{config.API_URL}/bans/get", params=params)
        return await response.json()

    async def add_ban(self, banned, moderator, expires_in: timedelta = None, reason=None):
        current_time = datetime.utcnow()
        data = {
            "id": banned,
            "moderator": moderator,
            "banned_at": current_time.timestamp(),
            "expires_at": (current_time + expires_in).timestamp() if expires_in is not None else None
        }
        if data["expires_at"] is None:
            del data["expires_at"]
        response = await self.session.put(f"{config.API_URL}/bans/edit", json=data, headers=self.authentication_headers)
        data = await response.json()
        if not data["success"]:
            raise self.ApiException(data["message"])
        return await response.json()


def setup(bot):
    bot.add_cog(Api(bot))
