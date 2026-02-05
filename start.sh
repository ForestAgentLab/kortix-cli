#!/bin/bash
# Kortix CLI Linux/macOS 一键启动脚本 - 完全自动化版本

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "=========================================="
echo "  Kortix AI Agent CLI - 一键启动"
echo "=========================================="
echo ""

# 步骤 1: 检查 Python
echo -e "${BLUE}[1/5] 检查 Python 环境...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[✗] Python3 未安装${NC}"
    echo ""
    echo "请先安装 Python 3.8+:"
    echo "  macOS: brew install python3"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "  CentOS/RHEL: sudo yum install python3 python3-pip"
    exit 1
fi

python3 --version
echo -e "${GREEN}[✓] Python 已安装${NC}"
echo ""

# 步骤 2: 自动安装依赖
echo -e "${BLUE}[2/5] 检查和安装依赖...${NC}"
if ! python3 -c "import dashscope" &> /dev/null; then
    echo -e "${YELLOW}[!] 依赖未安装，正在自动安装...${NC}"
    echo "   这可能需要几分钟，请稍候..."
    echo ""
    pip3 install -r requirements.txt
    echo -e "${GREEN}[✓] 依赖安装成功${NC}"
else
    echo -e "${GREEN}[✓] 依赖已安装${NC}"
fi
echo ""

# 步骤 3: 配置 API Key
echo -e "${BLUE}[3/5] 配置 API Key...${NC}"
if [ ! -f backend/.env ]; then
    echo -e "${YELLOW}[!] 首次使用，需要配置 API Key${NC}"
    echo ""
    
    # 交互式输入 API Key
    read -p "请输入阿里云百炼 API Key (sk-开头): " DASHSCOPE_KEY
    
    # 验证输入
    if [ -z "$DASHSCOPE_KEY" ]; then
        echo -e "${RED}[✗] API Key 不能为空${NC}"
        echo ""
        echo "请访问获取: https://dashscope.console.aliyun.com/"
        exit 1
    fi
    
    # 创建 .env 文件
    echo "DASHSCOPE_API_KEY=$DASHSCOPE_KEY" > backend/.env
    
    # 询问是否配置 Tavily (可选)
    echo ""
    read -p "是否配置 Tavily 搜索 API Key? (可选，直接回车跳过): " USE_TAVILY
    if [ ! -z "$USE_TAVILY" ]; then
        echo "TAVILY_API_KEY=$USE_TAVILY" >> backend/.env
        echo -e "${GREEN}[✓] Tavily Key 已配置${NC}"
    fi
    
    echo ""
    echo -e "${GREEN}[✓] API Key 已保存到 backend/.env 文件${NC}"
else
    echo -e "${GREEN}[✓] backend/.env 文件已存在${NC}"
fi
echo ""

# 步骤 4: 检查 Docker
echo -e "${BLUE}[4/5] 检查 Docker 环境...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}[!] Docker 未安装${NC}"
    echo ""
    echo "建议安装 Docker:"
    echo "  macOS: brew install --cask docker"
    echo "  Ubuntu: sudo apt install docker.io"
    echo ""
    echo "没有 Docker 仍可使用，但代码执行功能将不可用"
    echo ""
else
    docker version | head -3 || echo -e "${YELLOW}[!] Docker 未运行${NC}"
    echo -e "${GREEN}[✓] Docker 已检查${NC}"
fi
echo ""

# 步骤 5: 创建必要目录
echo -e "${BLUE}[5/5] 初始化数据目录...${NC}"
mkdir -p data/conversations
mkdir -p data/workspace
echo -e "${GREEN}[✓] 数据目录已创建${NC}"
echo ""

# 显示配置信息
echo "=========================================="
echo "  环境准备完成!"
echo "=========================================="
echo ""

# 启动程序
echo "启动 Kortix AI Agent..."
echo ""
python3 run.py "$@"
