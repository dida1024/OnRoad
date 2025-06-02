
from app.core.config import settings
from app.core.telegram.bot_base import TelegramBase


class OnRoadBot(TelegramBase):
    def get_token(self) -> str:
        print(settings.TELEGRAM_BOT_ROAD_TOKEN)
        return settings.TELEGRAM_BOT_ROAD_TOKEN

    def get_chat_id(self) -> str:
        print(settings.TELEGRAM_BOT_ROAD_CHAT_ID)
        return settings.TELEGRAM_BOT_ROAD_CHAT_ID
