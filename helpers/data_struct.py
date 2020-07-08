import discord

class MessageQueue:
    def __init__(self, length: int):
        self.maxlen = length
        self.messages = []

    def add(self, message: discord.Message):
        self.messages.insert(0, message)

    def pop(self) -> discord.Message:
        return self.messages.pop()