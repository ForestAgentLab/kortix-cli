#!/bin/bash
# Kortix CLI - Docker 一键部署脚本

set -e

echo "=========================================="
echo "Kortix CLI - Docker 一键部署"
echo "=========================================="
echo ""

# 检查 Docker
if ! command -v docker &> /dev/null; then
    echo "❌ 错误: 未检测到 Docker"
    echo "请先安装 Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

echo "✅ Docker 已安装: $(docker --version)"

# 检查 Docker Compose
if ! command -v docker compose &> /dev/null; then
    echo "⚠️  警告: docker compose 不可用，将使用 docker-compose"
    COMPOSE_CMD="docker-compose"
else
    COMPOSE_CMD="docker compose"
fi

# 检查 .env 文件
if [ ! -f backend/.env ]; then
    echo ""
    echo "📝 首次使用，需要配置 API Key"
    echo "请输入阿里云百炼 API Key:"
    read -r DASHSCOPE_KEY
    
    echo "DASHSCOPE_API_KEY=$DASHSCOPE_KEY" > backend/.env
    
    echo ""
    echo "（可选）是否配置 Tavily 搜索 API Key? (y/N)"
    read -r USE_TAVILY
    if [ "$USE_TAVILY" = "y" ] || [ "$USE_TAVILY" = "Y" ]; then
        echo "请输入 Tavily API Key:"
        read -r TAVILY_KEY
        echo "TAVILY_API_KEY=$TAVILY_KEY" >> backend/.env
    fi
    
    echo "✅ 配置已保存到 backend/.env 文件"
fi

echo ""
echo "=========================================="
echo "开始部署..."
echo "=========================================="

# 创建数据目录
mkdir -p data/conversations data/workspace

# 预拉取沙箱镜像（后台）
echo "📦 预拉取 Python 沙箱镜像（后台进行）..."
docker pull python:3.11-slim &

# 构建并启动
echo "🔨 构建镜像..."
$COMPOSE_CMD build

echo "🚀 启动容器..."
$COMPOSE_CMD up -d

echo ""
echo "=========================================="
echo "✅ 部署成功！"
echo "=========================================="
echo ""
echo "使用方法："
echo "  1. 进入交互式终端:"
echo "     docker attach kortix-cli"
echo ""
echo "  2. 查看日志:"
echo "     $COMPOSE_CMD logs -f"
echo ""
echo "  3. 停止服务:"
echo "     $COMPOSE_CMD stop"
echo ""
echo "  4. 重启服务:"
echo "     $COMPOSE_CMD restart"
echo ""
echo "详细文档: DOCKER_DEPLOY.md"
echo ""
echo "🎉 开始使用 Kortix CLI!"
echo "=========================================="

# 等待容器启动
sleep 2

# 询问是否立即进入
echo ""
echo "是否立即进入交互式终端? (Y/n)"
read -r ENTER_NOW
if [ "$ENTER_NOW" != "n" ] && [ "$ENTER_NOW" != "N" ]; then
    echo ""
    echo "进入 Kortix CLI..."
    echo "（退出请按 Ctrl+P Ctrl+Q 或 exit）"
    sleep 1
    docker attach kortix-cli
fi
