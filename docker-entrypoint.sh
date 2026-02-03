#!/bin/bash
set -e

echo "=========================================="
echo "Kortix CLI - Docker 容器启动"
echo "=========================================="

# 检查 Docker socket
if [ ! -S /var/run/docker.sock ]; then
    echo "⚠️  警告: Docker socket 未挂载"
    echo "   沙箱功能将无法使用"
    echo "   请使用: -v /var/run/docker.sock:/var/run/docker.sock"
fi

# 检查 API Key
if [ -z "$DASHSCOPE_API_KEY" ]; then
    echo "❌ 错误: 缺少 DASHSCOPE_API_KEY 环境变量"
    echo ""
    echo "请设置阿里云百炼 API Key:"
    echo "  docker run -e DASHSCOPE_API_KEY=sk-xxxxx ..."
    echo "  或在 .env 文件中设置"
    exit 1
fi

# 检查 .env 文件（如果存在）
if [ -f .env ]; then
    echo "✅ 加载 .env 文件"
    export $(cat .env | grep -v '^#' | xargs)
fi

# 创建必要目录
mkdir -p /app/data/conversations
mkdir -p /app/data/workspace

echo ""
echo "✅ 环境配置完成"
echo "   API Key: ${DASHSCOPE_API_KEY:0:10}..."
echo "   工作区: $WORKSPACE_DIR"
echo ""
echo "🚀 启动 Kortix CLI..."
echo "=========================================="
echo ""

# 预拉取常用沙箱镜像（后台进行）
{
    echo "📦 预拉取沙箱镜像..."
    docker pull python:3.11-slim 2>/dev/null || true
    echo "✅ Python 沙箱镜像就绪"
} &

# 执行传入的命令
exec "$@"
