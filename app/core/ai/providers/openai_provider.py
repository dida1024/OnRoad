from openai import AsyncOpenAI
from app.core.ai.ai_base import AiClientBase

class OpenAiChat(AiClientBase):
    """OpenAI聊天实现类"""
    def __init__(self, api_key: str, url: str, model: str) -> None:
        self.model = model
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url=url
        )
        
    async def chat_without_stream(self, system_prompt: str, user_message: str) -> str:        
        """
        发送非流式聊天请求，返回聊天结果
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
            )
            return response.choices[0].message.content
        except Exception as e:
            # logger.error("调用 OpenAI API 时发生异常: %s", e)
            raise 