"""对话历史管理接口路由"""

from fastapi import APIRouter, HTTPException, status, Query
from typing import Optional

from api.models import (
    HistoryResponse, 
    HistoryMessage, 
    HistoryLoadRequest,
    SuccessResponse
)
from api.dependencies import get_agent
from core.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(tags=["history"])


@router.get(
    "/",
    response_model=HistoryResponse,
    summary="获取对话历史",
    description="获取当前会话的对话历史记录"
)
async def get_history(limit: Optional[int] = Query(50, description="返回的最大消息数")) -> HistoryResponse:
    """
    获取对话历史
    
    Args:
        limit: 返回的最大消息数
    
    Returns:
        对话历史列表
    
    Example:
        curl http://localhost:8000/v1/history?limit=10
    """
    try:
        agent = get_agent()
        messages = agent.messages
        
        # 限制返回数量
        if limit and len(messages) > limit:
            messages = messages[-limit:]
        
        # 转换为响应格式
        history_messages = []
        for msg in messages:
            history_messages.append(HistoryMessage(
                role=msg.role,
                content=msg.content,
                timestamp=None,  # TODO: 添加时间戳
                tool_calls=getattr(msg, 'tool_calls', None),
                tool_call_id=getattr(msg, 'tool_call_id', None),
                name=getattr(msg, 'name', None)
            ))
        
        logger.info(f"返回 {len(history_messages)} 条历史消息")
        
        return HistoryResponse(
            messages=history_messages,
            total=len(history_messages)
        )
    
    except Exception as e:
        logger.error(f"获取历史失败: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post(
    "/save",
    response_model=SuccessResponse,
    summary="保存对话历史",
    description="将当前对话历史保存到文件"
)
async def save_history() -> SuccessResponse:
    """
    保存对话历史到文件
    
    Returns:
        保存结果和文件路径
    
    Example:
        curl -X POST http://localhost:8000/v1/history/save
    """
    try:
        agent = get_agent()
        
        # 保存历史
        agent.save_history()
        
        logger.info("对话历史已保存")
        
        return SuccessResponse(
            success=True,
            message="对话历史已保存",
            data={"directory": "./conversations"}
        )
    
    except Exception as e:
        logger.error(f"保存历史失败: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post(
    "/load",
    response_model=SuccessResponse,
    summary="加载对话历史",
    description="从文件加载对话历史"
)
async def load_history(request: HistoryLoadRequest) -> SuccessResponse:
    """
    从文件加载对话历史
    
    Args:
        request: 包含文件路径的请求
    
    Returns:
        加载结果
    
    Example:
        curl -X POST http://localhost:8000/v1/history/load \\
          -H "Content-Type: application/json" \\
          -d '{"filepath": "./conversations/conversation_20260205.json"}'
    """
    try:
        agent = get_agent()
        
        # 加载历史
        agent.load_history(request.filepath)
        
        logger.info(f"加载历史文件: {request.filepath}")
        
        return SuccessResponse(
            success=True,
            message=f"已加载 {len(agent.messages)} 条历史消息",
            data={"message_count": len(agent.messages)}
        )
    
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"文件不存在: {request.filepath}"
        )
    except Exception as e:
        logger.error(f"加载历史失败: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.delete(
    "/",
    response_model=SuccessResponse,
    summary="清除对话历史",
    description="清除当前会话的对话历史"
)
async def clear_history() -> SuccessResponse:
    """
    清除对话历史
    
    与 /chat/reset 功能相同，提供 RESTful 风格的接口。
    
    Example:
        curl -X DELETE http://localhost:8000/v1/history
    """
    try:
        agent = get_agent()
        agent.reset()
        
        logger.info("对话历史已清除")
        
        return SuccessResponse(
            success=True,
            message="对话历史已清除"
        )
    
    except Exception as e:
        logger.error(f"清除历史失败: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
