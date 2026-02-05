#!/usr/bin/env python3
"""
Kortix API 服务启动脚本

使用 Uvicorn 启动 FastAPI 应用。

使用方法:
    python start_api.py              # 开发模式（热重载）
    python start_api.py --prod       # 生产模式（多进程）
    python start_api.py --port 9000  # 自定义端口
"""

import click
import uvicorn
import sys
from pathlib import Path

# 添加当前目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))


@click.command()
@click.option('--host', default='0.0.0.0', help='监听地址')
@click.option('--port', default=8000, help='监听端口')
@click.option('--prod', is_flag=True, help='生产模式（多进程）')
@click.option('--workers', default=4, help='Worker 进程数（生产模式）')
def main(host: str, port: int, prod: bool, workers: int):
    """启动 Kortix API 服务"""
    
    if prod:
        # 生产模式：多进程，无热重载
        print(f"🚀 启动 Kortix API (生产模式)")
        print(f"   地址: {host}:{port}")
        print(f"   进程数: {workers}")
        print(f"   文档: http://{host}:{port}/docs")
        
        uvicorn.run(
            "main:app",  # 修复：使用 main:app 而不是 api:app
            host=host,
            port=port,
            workers=workers,
            loop="asyncio",
            reload=False,
            log_level="info",
            access_log=True
        )
    else:
        # 开发模式：单进程，热重载
        print(f"🚀 启动 Kortix API (开发模式)")
        print(f"   地址: {host}:{port}")
        print(f"   热重载: 启用")
        print(f"   文档: http://{host}:{port}/docs")
        print(f"\n💡 提示: 使用 --prod 参数启用生产模式\n")
        
        uvicorn.run(
            "main:app",  # 修复：使用 main:app 而不是 api:app
            host=host,
            port=port,
            reload=True,
            log_level="debug"
        )


if __name__ == "__main__":
    main()
