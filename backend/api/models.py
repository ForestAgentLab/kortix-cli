"""API 模块 - Pydantic 数据模型"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Literal
from datetime import datetime


class ChatRequest(BaseModel):
    """对话请求模型"""
    message: str = Field(..., min_length=1, max_length=10000, description="用户消息内容")
    stream: Optional[bool] = Field(True, description="是否流式响应")
    
    @validator("message")
    def validate_message(cls, v):
        if not v.strip():
            raise ValueError("消息不能为空")
        return v.strip()


class ChatResponse(BaseModel):
    """对话响应模型"""
    content: str = Field(..., description="助手回复内容")
    tool_calls: Optional[List[dict]] = Field(None, description="工具调用信息")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())


class ToolExecuteRequest(BaseModel):
    """工具执行请求"""
    function: str = Field(..., description="函数名")
    parameters: dict = Field(default_factory=dict, description="函数参数")


class ToolExecuteResponse(BaseModel):
    """工具执行响应"""
    success: bool
    output: Optional[str] = None
    error: Optional[str] = None


class FunctionDefinition(BaseModel):
    """函数定义"""
    name: str
    description: str
    parameters: dict


class ToolInfo(BaseModel):
    """工具信息"""
    name: str
    description: str
    functions: List[FunctionDefinition]


class HistoryMessage(BaseModel):
    """历史消息"""
    role: Literal["system", "user", "assistant", "tool"]
    content: str
    timestamp: Optional[str] = None
    tool_calls: Optional[List[dict]] = None
    tool_call_id: Optional[str] = None
    name: Optional[str] = None


class HistoryResponse(BaseModel):
    """历史响应"""
    messages: List[HistoryMessage]
    total: int


class HistoryLoadRequest(BaseModel):
    """加载历史请求"""
    filepath: str = Field(..., description="历史文件路径")


class SuccessResponse(BaseModel):
    """通用成功响应"""
    success: bool = True
    message: Optional[str] = None
    data: Optional[dict] = None


class HealthResponse(BaseModel):
    """健康检查响应"""
    status: str
    timestamp: str
    tools_enabled: List[str]
