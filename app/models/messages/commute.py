from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field
from app.models.messages import BaseMessage


class CommuteType(Enum):
    """
    通勤类型
    """
    WORK = "work"
    HOME = "home"
    

# 黄历数据
class YellowCalendar(BaseModel):
    """
    黄历数据
    """
    lunar: Optional[str] = Field(default=None, description="农历")
    time: str = Field(description="时辰")
    festivals: Optional[list[str]] = Field(default=None, description="节日")
    date: str = Field(description="日期", example="2025-06-23")
    week: str = Field(description="星期", example="星期一")
    hour: str = Field(description="小时", example="21")
    yi: str = Field(description="宜")
    ji: str = Field(description="忌")
    chong: str = Field(description="冲煞")
    sha: str = Field(description="煞")

# 天气
class Weather(BaseModel):
    """
    天气数据
    """
    weather: str = Field(description="天气描述")
    temperature: float = Field(description="温度")
    feel_temperature: float = Field(description="体感温度")
    humidity: float = Field(description="湿度")


class SendType(Enum):
    """
    发送方式
    """
    EMAIL = "email"
    TELEGRAM = "telegram"

class CommuteMessage(BaseMessage):
    """
    通勤消息
    """
    type: CommuteType = Field(default=CommuteType.WORK, description="通勤类型")
    send_type: SendType = Field(default=SendType.EMAIL, description="发送方式")
    weather: Weather = Field(description="天气")
    yellow_calendar: YellowCalendar = Field(description="黄历")