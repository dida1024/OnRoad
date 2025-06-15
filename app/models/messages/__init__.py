from pydantic import BaseModel, Field
from datetime import datetime

class BaseMessage(BaseModel):
    """
    基础消息模型。
    - createAt: 消息创建时间，自动设置为当前时间。
    """
    createAt: datetime = Field(default_factory=datetime.now)