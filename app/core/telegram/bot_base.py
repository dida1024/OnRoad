from abc import ABC, abstractmethod

from telegram import Bot


class TelegramBase(ABC):

    def __init__(self):
        self.name: str = self.__class__.__name__
        self.bot: Bot | None = None
        self.chat_id: str = self.get_chat_id()

    @abstractmethod
    def get_token(self) -> str:
        """子类提供 TOKEN"""
        pass

    @abstractmethod
    def get_chat_id(self) -> str:
        """子类提供 Chat ID"""
        pass

    async def __aenter__(self):
        self.bot = Bot(self.get_token())
        await self.bot.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.bot.close()

    async def send_message(self, message: str) -> str:
        await self.bot.send_message(chat_id=self.chat_id, text=message)
        return "success"
