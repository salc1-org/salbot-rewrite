"""
Created by Epic at 7/14/20
"""

import logging

from discord.ext import commands
from aiohttp import ClientSession
import config
from httputils import Route
from datetime import datetime


class Api(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("salbot.cogs.api")
        self.authentication_headers = {"Authorization": config.API_TOKEN}
        self.session = ClientSession()

    class ApiException(BaseException):
        def __init__(self, message):
            super().__init__(message)

    async def request(self, route: Route, **kwargs):
        full_route = config.API_URL + route.route
        method = route.method

        kwargs["headers"] = self.authentication_headers

        r = await self.session.request(method, full_route, **kwargs)
        return await r.json()

    async def get_punishments(self):
        route = Route("GET", "/punishments/get")
        return await self.request(route)

    async def create_punishment(self, punishment_type: str, punished_id: int, moderator_id: int, expires_at: datetime,
                                reason=""):
        if expires_at is not None:
            expires_at_timestamp = expires_at.timestamp()
        else:
            expires_at_timestamp = 0

        data = {
            "punishment_type": punishment_type,

            "punished_id": punished_id,
            "moderator_id": moderator_id,

            "punished_at": datetime.utcnow().timestamp(),
            "expires_at": expires_at_timestamp,

            "reason": reason
        }

        route = Route("PUT", "/punishments/add")
        return await self.request(route, json=data)


def setup(bot):
    bot.add_cog(Api(bot))
