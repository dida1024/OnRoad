import asyncio
from app.core.config import settings
from app.core.ai.ai_helper import AiHelper
from app.core.ai.providers.openai_provider import OpenAiChat

async def main():
    # 创建AI客户端
    deepseek_client = OpenAiChat(
        settings.DEEPSEEK_API, 
        settings.DEEPSEEK_URL, 
        settings.DEEPSEEK_MODEL
    )
    
    # 创建AI助手
    ai_helper = AiHelper(deepseek_client)
    
    # 获取并打印当前使用的模型
    model_name = ai_helper.get_model()
    print(f"使用的模型: {model_name}")
    

if __name__ == "__main__":
    asyncio.run(main()) 