import enum
from typing import Dict
from enum import Enum
from app.models.messages.commute import CommuteMessage,CommuteType



class PromptStrategy:
    """提示词策略基类"""
    def generate(self, **kwargs) -> str:
        raise NotImplementedError

class SummaryStrategy(PromptStrategy):
    """摘要生成策略"""
    def generate(self) -> str:
        prompt = "你是一个专业的AI总结助手。请遵循以下要求：\n1. 提取文本的核心观点和关键信息\n2. 保持客观准确的表述\n3. 按照主要内容-核心观点-关键细节的结构组织\n4. 总结必须简明扼要，控制在300字以内\n5. 确保内容完整、连贯、易懂\n6. 使用书面语，保持专业性"
        return prompt
    
class ChatStrategy(PromptStrategy):
    """聊天策略"""
    def generate(self) -> str:
        prompt = "你是DC模型，一个专业、友善、有帮助的AI助手。请用简洁清晰的语言回答问题。回答问题时，请不要换行，不要使用markdown格式，我希望你每次返回的内容不要超过500字，请使用用户输入的语言语种回答问题"
        return prompt

class PapersSummaryStrategy(PromptStrategy):
    """多文档整理策略"""
    def generate(self) -> str:
        prompt = """你是一个专业的文档分析助手。请遵循以下要求对文档进行分析：
                    1. 文档结构分析：
                    - 识别文档的主要章节和层级结构
                    - 提取每个部分的核心主题

                    2. 关键信息提取：
                    - 识别并列出关键概念、术语和定义
                    - 提取重要的数据点和参数
                    - 标注关键的API接口和功能点

                    3. 逻辑关系分析：
                    - 分析各部分之间的逻辑关联
                    - 识别依赖关系和流程
                    - 标注重要的条件和约束

                    4. 输出要求：
                    - 使用结构化的方式组织信息
                    - 保持专业的技术文档语言风格
                    - 确保分析的完整性和准确性
                    - 重点突出实用性信息
                    - 适当添加技术建议和注意事项

                    请以JSON格式返回分析结果，包含以下字段：
                    {
                        "document_structure": [],    // 文档结构概览
                        "key_concepts": [],         // 关键概念列表
                        "api_endpoints": [],        // API接口信息
                        "dependencies": [],         // 依赖关系
                        "important_notes": [],      // 重要注意事项
                        "recommendations": []       // 技术建议
                    }
                """
        return prompt
    
class CommuteStrategy(PromptStrategy):
    """通勤消息生成策略"""
    def generate(self, message: 'CommuteMessage') -> str:
        prompt = f"""请根据以下信息生成一条通勤提醒消息，就像是一个普通朋友在和你聊天：
                1. 通勤类型：{'上班' if message.type == CommuteType.WORK else '回家'}
                2. 天气信息：
                - 天气状况：{message.weather.weather}
                - 温度：{message.weather.temperature}°C
                - 体感温度：{message.weather.feel_temperature}°C
                - 湿度：{message.weather.humidity}%

                3. 黄历信息：
                - 农历：{message.yellow_calendar.lunar or '未知'}
                - 时辰：{message.yellow_calendar.time}
                - 宜：{message.yellow_calendar.yi}
                - 忌：{message.yellow_calendar.ji}
                - 冲煞：{message.yellow_calendar.chong}
                - 煞：{message.yellow_calendar.sha}
                - 节日：{', '.join(message.yellow_calendar.festivals) if message.yellow_calendar.festivals else '无'}

                请用自然的语气生成一条通勤提醒，要求：
                1. 用简单的问候语开头，就像跟朋友打招呼一样
                2. 用日常用语描述天气，比如"今天天气不错"这样的简单表达
                3. 如果黄历信息有意思，可以简单提一下，但不要过度解读
                4. 如果是节日，用普通的方式送上祝福
                5. 给出实用的着装建议，用日常对话的方式
                6. 最后用一句简单的安全提示结尾
                7. 可以适当用1-2个表情，但不要太多
                8. 用词要自然，避免过度修饰

                请用中文回复，字数控制在200字以内，要像真人说话一样自然。"""
        return prompt


class PromptType(Enum):
    CHAT = "chat"
    SUMMARY = "summary"
    COMMUTE = "commute"

class PromptHelper:
    """提示词管理核心类
    
    职责：
    1. 管理不同场景的提示词策略
    2. 提供统一的提示词获取接口
    3. 确保提示词类型的有效性验证
    """
    _strategies: Dict[PromptType, PromptStrategy] = {
        PromptType.SUMMARY: SummaryStrategy(),
        PromptType.CHAT: ChatStrategy(),
        PromptType.COMMUTE: CommuteStrategy(),
    }

    @classmethod
    def get_prompt(cls, prompt_type: PromptType, **kwargs) -> str:
        """
        获取提示词（带参数验证）
        
        Args:
            prompt_type: 提示词类型 (translation|summary|...)
            kwargs: 各策略需要的参数
            
        Returns:
            str: 生成的提示词
        """
        strategy = cls._strategies.get(prompt_type)
        if not strategy:
            raise ValueError(f"无效的提示词类型: {prompt_type}")
        
        return strategy.generate(**kwargs)