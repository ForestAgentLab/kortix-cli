"""API 依赖注入模块

避免循环导入，统一管理全局 Agent 实例
"""

from fastapi import HTTPException, status
from core.agent import Agent
from core.utils.logger import get_logger

logger = get_logger(__name__)

# 全局 Agent 实例
_agent: Agent = None


def get_agent() -> Agent:
    """
    获取全局 Agent 实例（依赖注入）
    
    Returns:
        Agent 实例
        
    Raises:
        HTTPException: Agent 初始化失败时
    """
    global _agent
    if _agent is None:
        try:
            _agent = Agent()
            logger.info("Agent 实例初始化成功")
        except ValueError as e:
            # API Key 配置错误
            logger.error(f"Agent 初始化失败 (配置错误): {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"配置错误: {str(e)}。请检查 DASHSCOPE_API_KEY 是否正确配置。"
            )
        except Exception as e:
            # 其他初始化错误
            logger.error(f"Agent 初始化失败: {e}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Agent 初始化失败: {str(e)}"
            )
    return _agent


def reset_agent():
    """重置全局 Agent 实例（用于测试）"""
    global _agent
    _agent = None
