from abc import ABC, abstractmethod

class AiClientBase(ABC):
    """AI客户端基础抽象类"""
    # 定义抽象基类的核心属性
    # model: 模型名称
    # client: AI客户端实例
    model: str
    client: object

    @abstractmethod
    async def chat_without_stream(self, system_prompt: str, user_message: str) -> str:
        """
        定义聊天接口，子类需要实现具体调用逻辑
        """
        pass 