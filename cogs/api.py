"""
Created by Epic at 7/14/20
"""

import logging

from discord.ext import commands
from aiohttp import ClientSession
import config
from httputils import Route


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

        r = await self.session.request(method, full_route, **kwargs)
        return await r.json()





def setup(bot):
    bot.add_cog(Api(bot))
