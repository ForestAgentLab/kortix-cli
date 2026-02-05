#!/usr/bin/env python3
"""
Kortix API 服务启动脚本（简化版）

委托给 backend/start_api.py 执行
"""

import sys
from pathlib import Path

# 确保项目根目录在 Python 路径中
sys.path.insert(0, str(Path(__file__).parent))

# 导入并运行 backend 的启动脚本
if __name__ == "__main__":
    # 方式1: 直接使用 uvicorn 命令行
    import uvicorn
    import click
    
    @click.command()
    @click.option('--host', default='0.0.0.0', help='监听地址')
    @click.option('--port', default=8000, help='监听端口')
    @click.option('--prod', is_flag=True, help='生产模式（多进程）')
    @click.option('--workers', default=4, help='Worker 进程数（生产模式）')
    def main(host: str, port: int, prod: bool, workers: int):
        """启动 Kortix API 服务"""
        
        if prod:
            print(f"🚀 启动 Kortix API (生产模式)")
            print(f"   地址: {host}:{port}")
            print(f"   进程数: {workers}")
            print(f"   文档: http://{host}:{port}/docs")
            
            uvicorn.run(
                "backend.main:app",
                host=host,
                port=port,
                workers=workers,
                loop="asyncio",
                reload=False,
                log_level="info",
                access_log=True
            )
        else:
            print(f"🚀 启动 Kortix API (开发模式)")
            print(f"   地址: {host}:{port}")
            print(f"   热重载: 启用")
            print(f"   文档: http://{host}:{port}/docs")
            print(f"\n💡 提示: 使用 --prod 参数启用生产模式\n")
            
            uvicorn.run(
                "backend.main:app",
                host=host,
                port=port,
                reload=True,
                log_level="debug"
            )
    
    main()
