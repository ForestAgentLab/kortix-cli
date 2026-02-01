# Kortix CLI - Docker 镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    docker.io \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY core/ ./core/
COPY run.py .
COPY config.yaml .
COPY .env.example .

# 创建数据目录
RUN mkdir -p /app/data/conversations /app/data/workspace

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV WORKSPACE_DIR=/app/data/workspace

# 暴露端口（如果将来需要 Web UI）
# EXPOSE 8000

# 启动脚本
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["python", "run.py"]
