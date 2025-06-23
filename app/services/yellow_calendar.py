from datetime import datetime
from typing import Protocol

from app.core.api_request import ApiRequest, MethodType
from app.exceptions.base import YellowCalendarException
from app.models.messages.commute import YellowCalendar

class YellowCalendarProtocol(Protocol):
    """Yellow calendar protocol for dependency injection"""
    async def get_yellow_calendar(self, date: str) -> YellowCalendar:
        ...

class YellowCalendarService:
    """Yellow calendar service"""
    async def get_yellow_calendar(self, date: str = datetime.now().strftime("%Y-%m-%d")) -> YellowCalendar:
        # 获取黄历
        yellow_calendar_url = "https://api.timelessq.com/time/shichen"
        # 万年历
        wan_nian_calendar_url = "https://api.timelessq.com/time"
        yellow_calendar_response = await ApiRequest(yellow_calendar_url, MethodType.GET, data={"date": date}).send()
        wan_nian_calendar_response = await ApiRequest(wan_nian_calendar_url, MethodType.GET, data={"date": date}).send()
        return await self.generate_yellow_calendar(yellow_calendar_response, wan_nian_calendar_response)

    
    async def generate_yellow_calendar(self, yellow_calendar_response: dict, wan_nian_calendar_response: dict) -> YellowCalendar:
        if not (data_list := yellow_calendar_response.get("data", [])):
            raise YellowCalendarException
        if not (wan_nian_data := wan_nian_calendar_response.get("data", [])):
            raise YellowCalendarException
        now_hour = datetime.now().strftime("%H:%M") # 当前小时+分钟，如21:00，则now_hour为2100
        lunar_dict = wan_nian_data.get("lunar", {})
        lunar_date = lunar_dict.get("cyclicalYear", "") + "年" + lunar_dict.get("cyclicalMonth", "") + "月" + lunar_dict.get("cyclicalDay", "") + "日"
        for data in data_list:
            hours = data.get("hours", "")
            hours_list = hours.split("-") if "-" in hours else [hours]
            # 处理时间段匹配
            is_match = False
            if hours_list[0] > hours_list[1]:  # 跨午夜情况
                is_match = now_hour >= hours_list[0] or now_hour <= hours_list[1]
            else:
                is_match = now_hour >= hours_list[0] and now_hour <= hours_list[1]
                
            if is_match:
                return YellowCalendar(
                    lunar=lunar_date,
                    date=datetime.now().strftime("%Y-%m-%d"),
                    week=wan_nian_data.get("cnWeek", ""),
                    hour=str(wan_nian_data.get("hour", "")),
                    festivals=wan_nian_data.get("festivals", None),
                    time=data.get("hour", ""),
                    yi=data.get("yi", ""),
                    ji=data.get("ji", ""),
                    chong=data.get("chong", ""),
                    sha=data.get("sha", ""),
                )
        raise YellowCalendarException
    
async def get_yellow_calendar_service() -> YellowCalendarProtocol:
    return YellowCalendarService()

# 测试
if __name__ == "__main__":
    async def test():
        yellow_calendar_service = await get_yellow_calendar_service()
        yellow_calendar = await yellow_calendar_service.get_yellow_calendar("2025-06-15")

    import asyncio
    asyncio.run(test())