"""工具管理接口路由"""

from fastapi import APIRouter, HTTPException, status
from typing import List

from backend.api.models import ToolInfo, ToolExecuteRequest, ToolExecuteResponse, FunctionDefinition
from backend.api.dependencies import get_agent
from backend.core.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(tags=["tools"])


@router.get(
    "/",
    response_model=dict,
    summary="获取工具列表",
    description="获取所有可用工具及其函数定义"
)
async def get_tools() -> dict:
    """
    获取所有可用工具
    
    Returns:
        包含所有工具信息的字典
    
    Example:
        curl http://localhost:8000/v1/tools
    """
    try:
        agent = get_agent()
        tool_registry = agent.tool_registry
        
        # 获取所有工具信息
        tools_data = []
        for tool_name in tool_registry.list_tools():
            tool = tool_registry.get_tool(tool_name)
            if tool:
                functions = []
                for func_def in tool.get_functions():
                    functions.append(FunctionDefinition(
                        name=func_def["name"],
                        description=func_def["description"],
                        parameters=func_def["parameters"]
                    ))
                
                tools_data.append(ToolInfo(
                    name=tool.name,
                    description=tool.description,
                    functions=functions
                ).model_dump())  # Pydantic v2 使用 model_dump() 而不是 dict()
        
        logger.info(f"返回 {len(tools_data)} 个工具信息")
        
        return {"tools": tools_data}
    
    except Exception as e:
        logger.error(f"获取工具列表失败: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get(
    "/{tool_name}",
    response_model=ToolInfo,
    summary="获取特定工具信息",
    description="获取指定工具的详细信息和函数定义"
)
async def get_tool(tool_name: str) -> ToolInfo:
    """
    获取特定工具信息
    
    Args:
        tool_name: 工具名称（如: calculator, file_manager）
    
    Returns:
        工具的详细信息
    
    Example:
        curl http://localhost:8000/v1/tools/calculator
    """
    try:
        agent = get_agent()
        tool = agent.tool_registry.get_tool(tool_name)
        
        if not tool:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"工具 '{tool_name}' 不存在"
            )
        
        functions = []
        for func_def in tool.get_functions():
            functions.append(FunctionDefinition(
                name=func_def["name"],
                description=func_def["description"],
                parameters=func_def["parameters"]
            ))
        
        logger.info(f"返回工具信息: {tool_name}")
        
        return ToolInfo(
            name=tool.name,
            description=tool.description,
            functions=functions
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取工具信息失败: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post(
    "/{tool_name}/execute",
    response_model=ToolExecuteResponse,
    summary="执行工具函数",
    description="直接调用指定工具的函数（不通过 AI Agent）"
)
async def execute_tool(tool_name: str, request: ToolExecuteRequest) -> ToolExecuteResponse:
    """
    直接执行工具函数
    
    Args:
        tool_name: 工具名称
        request: 包含函数名和参数的请求
    
    Returns:
        工具执行结果
    
    Example:
        curl -X POST http://localhost:8000/v1/tools/calculator/execute \\
          -H "Content-Type: application/json" \\
          -d '{"function": "calculate", "parameters": {"expression": "2+2"}}'
    """
    try:
        agent = get_agent()
        tool = agent.tool_registry.get_tool(tool_name)
        
        if not tool:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"工具 '{tool_name}' 不存在"
            )
        
        logger.info(
            f"执行工具函数",
            tool=tool_name,
            function=request.function,
            parameters=request.parameters
        )
        
        # 执行工具函数
        result = agent.tool_registry.execute(
            request.function,
            **request.parameters
        )
        
        return ToolExecuteResponse(
            success=result.success,
            output=result.output if result.success else None,
            error=result.error if not result.success else None
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"执行工具失败: {e}", exc_info=True)
        return ToolExecuteResponse(
            success=False,
            output=None,
            error=str(e)
        )
