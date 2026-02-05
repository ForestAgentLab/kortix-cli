#!/usr/bin/env python3
"""
Kortix FastAPI 后端服务

基于 FastAPI 的 Web API 服务，为前端提供 AI Agent 能力。

参考: https://github.com/kortix-ai/suna
"""

import sys
from pathlib import Path

# 添加当前目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import time

from api.chat import router as chat_router
from api.tools import router as tools_router
from api.history import router as history_router
from api.models import HealthResponse
from core.utils import init_config, setup_logging
from core.utils.logger import get_logger
from core.utils.config import get_config

# 初始化配置和日志
init_config()
setup_logging()

logger = get_logger(__name__)

# 创建 FastAPI 应用
app = FastAPI(
    title="Kortix API",
    description="Kortix AI Agent API - 基于阿里云百炼的智能助手",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    swagger_ui_parameters={
        "persistAuthorization": True,
    },
)


# CORS 中间件配置
# 参考 suna 的配置方式
config = get_config()
allowed_origins = ["http://localhost:3000", "http://127.0.0.1:3000"]

# 根据环境添加更多允许的域名
if config.get('api.cors_origins'):
    allowed_origins.extend(config.get('api.cors_origins'))

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins if allowed_origins else ["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Project-Id"],
)


# 请求日志中间件
@app.middleware("http")
async def log_requests_middleware(request: Request, call_next):
    """记录所有请求的日志"""
    start_time = time.time()
    client_ip = request.client.host if request.client else "unknown"
    method = request.method
    path = request.url.path
    
    logger.debug(f"请求开始: {method} {path} from {client_ip}")
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        
        logger.debug(
            f"请求完成: {method} {path} | "
            f"状态: {response.status_code} | "
            f"耗时: {process_time:.2f}s"
        )
        
        # 添加处理时间到响应头
        response.headers["X-Process-Time"] = f"{process_time:.2f}"
        
        return response
    
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(
            f"请求失败: {method} {path} | "
            f"错误: {str(e)} | "
            f"耗时: {process_time:.2f}s"
        )
        raise


# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理器"""
    logger.error(f"未处理的异常: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "内部服务器错误",
            "detail": str(exc),
            "timestamp": datetime.now().isoformat()
        }
    )


# 健康检查端点
@app.get(
    "/health",
    response_model=HealthResponse,
    summary="健康检查",
    description="检查 API 服务状态",
    tags=["system"]
)
async def health_check() -> HealthResponse:
    """
    健康检查接口
    
    返回服务状态和启用的工具列表。
    
    Example:
        curl http://localhost:8000/health
    """
    try:
        from api.dependencies import get_agent
        agent = get_agent()
        
        # 获取启用的工具
        tools_enabled = agent.tool_registry.list_tools()
        
        return HealthResponse(
            status="ok",
            timestamp=datetime.now().isoformat(),
            tools_enabled=tools_enabled
        )
    
    except Exception as e:
        logger.error(f"健康检查失败: {e}")
        raise HTTPException(status_code=503, detail=f"服务不可用: {str(e)}")


# 根路径
@app.get("/", tags=["system"])
async def root():
    """根路径，返回基本信息"""
    return {
        "name": "Kortix API",
        "version": "2.0.0",
        "description": "Kortix AI Agent API - 轻量级智能助手",
        "docs": "/docs",
        "health": "/health"
    }


# 注册路由
# 参考 suna 的路由结构，使用 /v1 前缀
app.include_router(chat_router, prefix="/v1/chat", tags=["chat"])
app.include_router(tools_router, prefix="/v1/tools", tags=["tools"])
app.include_router(history_router, prefix="/v1/history", tags=["history"])


logger.info("Kortix API 应用初始化完成")


if __name__ == "__main__":
    import uvicorn
    
    # 开发模式配置
    uvicorn.run(
        "main:app",  # 修复：使用 main:app
        host="0.0.0.0",
        port=8000,
        reload=True,  # 开发模式启用热重载
        log_level="info"
    )
