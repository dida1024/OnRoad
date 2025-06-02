from app.core.ai.ai_base import AiClientBase
from app.core.ai.utils.prompt_helper import PromptHelper, PromptType

class AiHelper:
    """AI助手服务类"""
    def __init__(self, client: AiClientBase) -> None:
        self.client = client
        self.model = client.model
    
    async def chat(self, user_prompt: str) -> str:
        """
        聊天功能
        """
        prompt = PromptHelper.get_prompt(PromptType.CHAT)
        response = await self.client.chat_without_stream(prompt, user_prompt)
        return response
    
    async def analyze_document(self, document: str) -> str:
        """
        文档分析功能
        
        Args:
            document: 需要分析的文档内容
            
        Returns:
            str: 分析结果
        """
        try:
            prompt = PromptHelper.get_prompt(PromptType.SUMMARY)
            response = await self.client.chat_without_stream(prompt, document)
            return response
        except Exception as e:
            # logger.error("文档分析时发生错误: %s", e)
            raise
            
    def get_model(self) -> str:
        """
        获取当前使用的模型名称
        """
        return self.model 