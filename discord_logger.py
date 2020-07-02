"""
Created by Epic at 7/2/20
"""
import logging
from discord import Webhook, RequestsWebhookAdapter, Embed
import config


class DiscordFormatter(logging.Handler):
    colors = {
        "debug": 0x00FFFF,
        "info": 0x0000FF,
        "warning": 0xFFFF00,
        "error": 0xFF4444,
        "critical": 0xFF0000
    }

    def __init__(self):
        super().__init__(logging.DEBUG)
        self.webhook = Webhook.from_url(config.WEBHOOK_URL, adapter=RequestsWebhookAdapter())

    def emit(self, record: logging.LogRecord) -> None:
        message = self.format(record)
        embed = Embed(title="Logging", color=self.colors[record.levelname.lower()], description=message)
        self.webhook.send(embed=embed)
