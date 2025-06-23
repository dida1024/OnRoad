from typing import List, TypeVar, Generic, Optional, Any
from pydantic import BaseModel, ConfigDict
# 定义泛型类型变量
T = TypeVar('T')

class PaginatedResults(BaseModel):
    total: int
    results: List[BaseModel]

# 通用API响应模型
class ApiResponse(BaseModel, Generic[T]):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    success: bool = True
    code: int = 200
    message: str = "操作成功"
    data: Optional[T] = None
    meta: Optional[dict] = None
    
    @classmethod
    def success_response(cls, data: T = None, message: str = "操作成功", code: int = 200, meta: dict = None) -> "ApiResponse[T]":
        """创建成功响应"""
        return cls(
            success=True,
            code=code,
            message=message,
            data=data,
            meta=meta
        )
    
    @classmethod
    def error_response(cls, message: str = "操作失败", code: int = 400, data: Any = None) -> "ApiResponse[T]":
        """创建错误响应
        
        Args:
            message: 错误消息
            code: 错误码
            data: 额外数据，如果是异常对象会被转换为字典
        """
        # 处理异常对象
        if isinstance(data, Exception):
            data = {
                "error_type": type(data).__name__,
                "error_detail": str(data)
            }
        
        # 确保 message 是字符串
        if isinstance(message, Exception):
            message = str(message)
            
        return cls(
            success=False,
            code=code,
            message=message,
            data=data
        )

# 分页数据响应包装器
class PaginatedResponse(ApiResponse, Generic[T]):
    data: List[T]
    meta: dict = {"total": 0, "page": 1, "page_size": 10}
    
    @classmethod
    def create(cls, items: List[T], total: int, page: int = 1, page_size: int = 10) -> "PaginatedResponse[T]":
        """创建分页响应"""
        return cls(
            data=items, 
            meta={
                "total": total,
                "page": page,
                "page_size": page_size
            }
        )

# 保留兼容性
class MessageResponse(BaseModel):
    detail: str 