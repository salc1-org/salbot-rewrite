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
        if r.status != 200:
            raise self.ApiException(await r.text())
        return await r.json()

    async def get_punishments(self, user_id=None):
        route = Route("GET", "/punishments/get")
        punishments = await self.request(route)
        if user_id is not None:
            new_punishments = []
            for punishment in punishments:
                if punishment["punished_id"] == user_id:
                    new_punishments.append(punishment)
            return new_punishments
        return punishments

    async def create_punishment(self, punishment_type: str, punished_id: int, moderator_id: int, expires_at: datetime,
                                reason=""):
        if expires_at is not None:
            expires_at_timestamp = expires_at.timestamp()
        else:
            expires_at_timestamp = 0

        data = {
            "punishment_type": punishment_type.upper(),

            "punished_id": punished_id,
            "moderator_id": moderator_id,

            "punished_at": datetime.now().timestamp(),
            "expires_at": expires_at_timestamp,

            "reason": reason
        }

        route = Route("PUT", "/punishments/add")
        return await self.request(route, json=data)

    async def mark_punishment_as_expired(self, punishment_id):
        route = Route("POST", "/punishments/expire")
        await self.request(route, json={"punishment_id": punishment_id})

    async def get_faq(self, name: str):
        route = Route("GET", "/faq/")
        return await self.request(route, json={"search": name})

    async def create_faq(self, name: str, description: str):
        route = Route("PUT", "/faq/")
        await self.request(route, json={"name": name, "description": description})


def setup(bot):
    bot.add_cog(Api(bot))
