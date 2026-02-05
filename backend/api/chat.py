"""对话接口路由"""

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse
import json
import asyncio
from typing import AsyncIterator

from backend.api.models import ChatRequest, ChatResponse, SuccessResponse
from backend.api.dependencies import get_agent
from backend.core.agent import Agent  # 用于类型注解
from backend.core.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(tags=["chat"])


async def chat_event_generator(agent: Agent, message: str) -> AsyncIterator[str]:
    """
    生成 SSE 事件流
    
    Args:
        agent: Agent 实例
        message: 用户消息
    
    Yields:
        SSE 格式的字符串
    """
    try:
        # 流式生成回复
        for chunk in agent.chat(message, stream=True):
            # SSE 格式: data: {json}\n\n
            event_data = {
                "type": "content",
                "content": chunk
            }
            yield f"data: {json.dumps(event_data, ensure_ascii=False)}\n\n"
            await asyncio.sleep(0)  # 让出控制权
        
        # 发送完成事件
        yield f"data: {json.dumps({'type': 'done'})}\n\n"
    
    except Exception as e:
        logger.error(f"对话生成失败: {e}", exc_info=True)
        error_data = {
            "type": "error",
            "error": str(e)
        }
        yield f"data: {json.dumps(error_data, ensure_ascii=False)}\n\n"


@router.post(
    "/",
    summary="流式对话",
    description="发送消息给 AI Agent，使用 Server-Sent Events (SSE) 返回流式响应",
    response_class=StreamingResponse
)
async def chat_stream(request: ChatRequest):
    """
    流式对话接口（推荐）
    
    返回 SSE 格式的流式响应，实时显示 AI 的思考和回复过程。
    
    Example:
        curl -N -X POST http://localhost:8000/v1/chat \\
          -H "Content-Type: application/json" \\
          -d '{"message": "你好"}'
    """
    try:
        agent = get_agent()
        
        logger.info(
            "收到流式对话请求",
            message_preview=request.message[:50],
            message_length=len(request.message)
        )
        
        return StreamingResponse(
            chat_event_generator(agent, request.message),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no",  # 禁用 nginx 缓冲
                "Connection": "keep-alive"
            }
        )
    
    except Exception as e:
        logger.error(f"流式对话失败: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post(
    "/completion",
    response_model=ChatResponse,
    summary="非流式对话",
    description="发送消息给 AI Agent，等待完整响应后一次性返回"
)
async def chat_completion(request: ChatRequest) -> ChatResponse:
    """
    非流式对话接口
    
    等待 AI 完成回复后，一次性返回完整内容。
    适合不需要实时显示的场景。
    
    Example:
        curl -X POST http://localhost:8000/v1/chat/completion \\
          -H "Content-Type: application/json" \\
          -d '{"message": "你好"}'
    """
    try:
        agent = get_agent()
        
        logger.info(
            "收到非流式对话请求",
            message_preview=request.message[:50]
        )
        
        # 收集所有响应片段
        full_response = ""
        for chunk in agent.chat(request.message, stream=False):
            full_response += chunk
        
        return ChatResponse(
            content=full_response,
            tool_calls=None  # TODO: 从 agent 获取 tool_calls
        )
    
    except Exception as e:
        logger.error(f"非流式对话失败: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post(
    "/reset",
    response_model=SuccessResponse,
    summary="重置对话",
    description="清除当前对话历史，开始新的对话"
)
async def reset_chat() -> SuccessResponse:
    """
    重置对话历史
    
    清除所有对话历史记录，Agent 会重新开始。
    
    Example:
        curl -X POST http://localhost:8000/v1/chat/reset
    """
    try:
        agent = get_agent()
        agent.reset()
        
        logger.info("对话历史已重置")
        
        return SuccessResponse(
            success=True,
            message="对话历史已重置"
        )
    
    except Exception as e:
        logger.error(f"重置对话失败: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
