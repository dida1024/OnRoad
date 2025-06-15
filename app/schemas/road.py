from pydantic import BaseModel, Field

from app.models.messages.commute import CommuteType, SendType

class RoadInfo(BaseModel):
    type: CommuteType = Field(description="类型")
    # 发送方式
    send_type: SendType = Field(description="发送方式")
    location: str = Field(default="shenzhen", description="位置")