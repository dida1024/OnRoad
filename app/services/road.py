from typing import Protocol
from app.core.ai.ai_helper import AiHelper
from app.core.ai.providers.openai_provider import OpenAiChat
from app.core.ai.utils.prompt_helper import PromptHelper, PromptType
from app.core.weather.qweather import Qweather
from app.models.messages.commute import CommuteMessage, CommuteType, SendType, Weather
from app.schemas.road import RoadInfo
from app.services.yellow_calendar import YellowCalendarProtocol, get_yellow_calendar_service
from app.core.config import settings
from app.core.telegram.providers.road_provider import OnRoadBot

class RoadServiceProtocol(Protocol):
    """Road service protocol for dependency injection"""
    async def send_road_info(self, road_info: RoadInfo) -> bool:
        ...

class RoadService:
    def __init__(self, yellow_calendar_service: YellowCalendarProtocol):
        self.yellow_calendar_service = yellow_calendar_service

    """Concrete implementation of road service"""
    async def send_road_info(self, road_info: RoadInfo) -> bool:
        try:
            yellow_calendar = await self.yellow_calendar_service.get_yellow_calendar()
            weather = await self.get_weather(road_info.location)
            message = CommuteMessage(
                type=road_info.type,
                send_type=road_info.send_type,
                weather=weather,
                yellow_calendar=yellow_calendar
            )
            # 发送消息
            await self.send_message(message)
            return True
        except Exception as e:
            raise e
    async def send_message(self, message: CommuteMessage) -> bool:
        match message.send_type:
            case SendType.EMAIL:
                pass
            case SendType.TELEGRAM:
                async with OnRoadBot() as bot:
                    ai_message = await self.generate_ai_message(message)
                    await bot.send_message(ai_message)
            case _:
                    raise ValueError(f"不支持的send_type: {message.send_type}")

    async def generate_ai_message(self, message: CommuteMessage) -> str:
        ai_helper = AiHelper(OpenAiChat(
            settings.DEEPSEEK_API, 
            settings.DEEPSEEK_URL, 
            settings.DEEPSEEK_MODEL
        ))
        return await ai_helper.chat(PromptHelper.get_prompt(PromptType.COMMUTE, message=message))

    async def get_weather(self, location: str) -> Weather:
        async with Qweather() as qweather:
            location_response = await qweather.get_location(location)
            weather_response = await qweather.get_weather(location_response.get("location")[0].get("id"))
            return Weather(
                weather=weather_response.get("now").get("text"),
                temperature=float(weather_response.get("now").get("temp")),
                feel_temperature=float(weather_response.get("now").get("feelsLike")),
                humidity=float(weather_response.get("now").get("humidity")),
            )

async def get_road_service() -> RoadServiceProtocol:
    return RoadService(yellow_calendar_service=await get_yellow_calendar_service())

# 测试
if __name__ == "__main__":
    async def test():
        road_service = await get_road_service()
        await road_service.send_road_info(RoadInfo(type=CommuteType.HOME, send_type=SendType.TELEGRAM))

    import asyncio
    asyncio.run(test())