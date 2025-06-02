import enum
from typing import Dict
from enum import Enum


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


class PromptType(Enum):
    CHAT = "chat"
    SUMMARY = "summary"

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

    @staticmethod
    def get_prompt(prompt_type: PromptType) -> str:
        prompts = {
            PromptType.CHAT: "你是一个AI助手，请回答用户的问题。",
            PromptType.SUMMARY: "请分析并总结以下文档内容："
        }
        return prompts[prompt_type]
