@echo off
REM Kortix CLI - Docker 一键部署脚本 (Windows)

echo ==========================================
echo Kortix CLI - Docker 一键部署
echo ==========================================
echo.

REM 检查 Docker
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未检测到 Docker
    echo 请先安装 Docker Desktop: https://docs.docker.com/desktop/install/windows-install/
    pause
    exit /b 1
)

echo ✅ Docker 已安装
docker --version

REM 检查 .env 文件
if not exist .env (
    echo.
    echo 📝 首次使用，需要配置 API Key
    set /p DASHSCOPE_KEY="请输入阿里云百炼 API Key: "
    echo DASHSCOPE_API_KEY=%DASHSCOPE_KEY%> .env
    
    echo.
    set /p USE_TAVILY="（可选）是否配置 Tavily 搜索 API Key? (y/N): "
    if /i "%USE_TAVILY%"=="y" (
        set /p TAVILY_KEY="请输入 Tavily API Key: "
        echo TAVILY_API_KEY=%TAVILY_KEY%>> .env
    )
    
    echo ✅ 配置已保存到 .env 文件
)

echo.
echo ==========================================
echo 开始部署...
echo ==========================================

REM 创建数据目录
if not exist data\conversations mkdir data\conversations
if not exist data\workspace mkdir data\workspace

REM 预拉取沙箱镜像（后台）
echo 📦 预拉取 Python 沙箱镜像...
start /b docker pull python:3.11-slim

REM 构建并启动
echo 🔨 构建镜像...
docker compose build

echo 🚀 启动容器...
docker compose up -d

echo.
echo ==========================================
echo ✅ 部署成功！
echo ==========================================
echo.
echo 使用方法：
echo   1. 进入交互式终端:
echo      docker attach kortix-cli
echo.
echo   2. 查看日志:
echo      docker compose logs -f
echo.
echo   3. 停止服务:
echo      docker compose stop
echo.
echo   4. 重启服务:
echo      docker compose restart
echo.
echo 详细文档: DOCKER_DEPLOY.md
echo.
echo 🎉 开始使用 Kortix CLI!
echo ==========================================

REM 等待容器启动
timeout /t 2 /nobreak >nul

REM 询问是否立即进入
echo.
set /p ENTER_NOW="是否立即进入交互式终端? (Y/n): "
if /i not "%ENTER_NOW%"=="n" (
    echo.
    echo 进入 Kortix CLI...
    echo （退出请按 Ctrl+P Ctrl+Q 或输入 exit）
    timeout /t 1 /nobreak >nul
    docker attach kortix-cli
)

pause
