"""
Created by vcokltfre at 2020-07-08
"""
import discord


class MessageQueue:
    def __init__(self, length: int):
        self.maxlen = length
        self.messages = []

    def add(self, message: discord.Message):
        if len(self.messages) + 1 > self.maxlen:
            self.messages.pop(0)
        self.messages.append(message)

    def pop(self) -> discord.Message:
        return self.messages.pop()
