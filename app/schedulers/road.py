from app.models.messages.commute import CommuteType, SendType
from app.schemas.road import RoadInfo
from app.services.road import get_road_service

class RoadScheduler:
    @staticmethod
    async def send_morning_message():
        road_info = RoadInfo(
            type=CommuteType.WORK,
            send_type=SendType.TELEGRAM
        )
        road_service = await get_road_service()
        await road_service.send_road_info(road_info)
    
    @staticmethod
    async def send_evening_message():
        road_info = RoadInfo(
            type=CommuteType.HOME,
            send_type=SendType.TELEGRAM
        )
        road_service = await get_road_service()
        await road_service.send_road_info(road_info)