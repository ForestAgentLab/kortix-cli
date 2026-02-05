@echo off
REM Kortix CLI Windows 一键启动脚本 - 完全自动化版本
SETLOCAL EnableDelayedExpansion

echo ==========================================
echo   Kortix AI Agent CLI - 一键启动
echo ==========================================
echo.

REM 步骤 1: 检查 Python
echo [1/5] 检查 Python 环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [X] Python 未安装或未添加到 PATH
    echo.
    echo 请先安装 Python 3.8+:
    echo   https://www.python.org/downloads/
    echo.
    echo 安装时请勾选 "Add Python to PATH"
    pause
    exit /b 1
)
python --version
echo [✓] Python 已安装
echo.

REM 步骤 2: 自动安装依赖
echo [2/5] 检查和安装依赖...
python -c "import dashscope" >nul 2>&1
if errorlevel 1 (
    echo [!] 依赖未安装，正在自动安装...
    echo    这可能需要几分钟，请稍候...
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [X] 依赖安装失败
        echo.
        echo 请检查网络连接或手动执行:
        echo   pip install -r requirements.txt
        pause
        exit /b 1
    )
    echo [✓] 依赖安装成功
) else (
    echo [✓] 依赖已安装
)
echo.

REM 步骤 3: 配置 API Key
echo [3/5] 配置 API Key...
if not exist backend\.env (
    echo [!] 首次使用，需要配置 API Key
    echo.
    
    REM 交互式输入 API Key
    set /p DASHSCOPE_KEY="请输入阿里云百炼 API Key (sk-开头): "
    
    REM 验证输入
    if "!DASHSCOPE_KEY!"=="" (
        echo [X] API Key 不能为空
        echo.
        echo 请访问获取: https://dashscope.console.aliyun.com/
        pause
        exit /b 1
    )
    
    REM 创建 .env 文件
    echo DASHSCOPE_API_KEY=!DASHSCOPE_KEY!> backend\.env
    
    REM 询问是否配置 Tavily (可选)
    echo.
    set /p USE_TAVILY="是否配置 Tavily 搜索 API Key? (可选，直接回车跳过): "
    if not "!USE_TAVILY!"=="" (
        echo TAVILY_API_KEY=!USE_TAVILY!>> backend\.env
        echo [✓] Tavily Key 已配置
    )
    
    echo.
    echo [✓] API Key 已保存到 backend\.env 文件
) else (
    echo [✓] backend\.env 文件已存在
)
echo.

REM 步骤 4: 检查 Docker
echo [4/5] 检查 Docker 环境...
docker version >nul 2>&1
if errorlevel 1 (
    echo [!] Docker 未运行
    echo.
    echo 建议:
    echo   1. 安装 Docker Desktop: https://www.docker.com/products/docker-desktop/
    echo   2. 或启动 Docker 服务
    echo.
    echo 没有 Docker 仍可使用，但代码执行功能将不可用
    echo.
    set /p CONTINUE="是否继续启动? (Y/n): "
    if /i "!CONTINUE!"=="n" (
        echo 已取消启动
        pause
        exit /b 0
    )
) else (
    docker version
    echo [✓] Docker 已就绪
    
    REM 预拉取 Python 沙箱镜像（后台）
    echo [!] 正在后台预拉取 Python 沙箱镜像...
    start /b docker pull python:3.11-slim >nul 2>&1
)
echo.

REM 步骤 5: 创建必要目录
echo [5/5] 初始化数据目录...
if not exist data\conversations mkdir data\conversations
if not exist data\workspace mkdir data\workspace
echo [✓] 数据目录已创建
echo.

REM 显示配置信息
echo ==========================================
echo   环境准备完成!
echo ==========================================
echo.
echo 配置信息:
echo   Python: 已安装
echo   依赖包: 已安装
echo   API Key: 已配置
docker version >nul 2>&1
if errorlevel 1 (
    echo   Docker: 未运行 (代码执行不可用)
) else (
    echo   Docker: 已就绪
)
echo.

REM 启动程序
echo ==========================================
echo   启动 Kortix AI Agent...
echo ==========================================
echo.
echo 使用提示:
echo   - 输入 "exit" 或 "quit" 退出
echo   - 输入 "help" 查看帮助
echo   - 按 Ctrl+C 强制退出
echo.
echo ------------------------------------------
echo.

python run.py %*

echo.
echo ------------------------------------------
echo 感谢使用 Kortix AI Agent!
pause
