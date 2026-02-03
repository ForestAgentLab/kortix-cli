# Kortix CLI - Makefile

.PHONY: help build up down restart logs shell clean

# 默认目标
help:
	@echo "Kortix CLI - Docker 命令"
	@echo ""
	@echo "使用方法: make [target]"
	@echo ""
	@echo "可用命令:"
	@echo "  make deploy   - 一键部署（首次使用）"
	@echo "  make build    - 构建镜像"
	@echo "  make up       - 启动容器"
	@echo "  make down     - 停止并删除容器"
	@echo "  make restart  - 重启容器"
	@echo "  make logs     - 查看日志"
	@echo "  make shell    - 进入终端"
	@echo "  make attach   - 附加到运行中的容器"
	@echo "  make clean    - 清理所有容器和镜像"
	@echo "  make setup    - 预拉取沙箱镜像"
	@echo "  make test     - 运行测试"
	@echo ""

# 一键部署
deploy:
	@echo "🚀 开始一键部署..."
	@bash docker-deploy.sh || cmd /c docker-deploy.bat

# 构建镜像
build:
	@echo "🔨 构建镜像..."
	docker compose build

# 启动容器
up:
	@echo "🚀 启动容器..."
	docker compose up -d
	@echo "✅ 容器已启动"

# 停止并删除容器
down:
	@echo "🛑 停止容器..."
	docker compose down

# 重启容器
restart:
	@echo "🔄 重启容器..."
	docker compose restart

# 查看日志
logs:
	docker compose logs -f

# 进入 bash shell
shell:
	docker compose exec kortix-cli bash

# 附加到运行中的容器
attach:
	@echo "进入 Kortix CLI..."
	@echo "（退出: Ctrl+P Ctrl+Q 或 exit）"
	docker attach kortix-cli

# 预拉取沙箱镜像
setup:
	@echo "📦 预拉取沙箱镜像..."
	docker pull python:3.11-slim
	docker pull node:20-slim
	@echo "✅ 沙箱镜像已就绪"

# 运行测试
test:
	docker compose exec kortix-cli python -m pytest tests/ -v

# 清理
clean:
	@echo "🧹 清理容器和镜像..."
	docker compose down -v
	docker rmi kortix-cli || true
	@echo "✅ 清理完成"

# 重建（不使用缓存）
rebuild:
	@echo "🔨 重建镜像（无缓存）..."
	docker compose build --no-cache
	docker compose up -d

# 查看状态
status:
	@echo "容器状态:"
	@docker compose ps
	@echo ""
	@echo "资源占用:"
	@docker stats kortix-cli --no-stream || echo "容器未运行"

# 备份数据
backup:
	@echo "📦 备份数据..."
	@mkdir -p backups
	@tar -czf backups/kortix-data-$$(date +%Y%m%d-%H%M%S).tar.gz data/
	@echo "✅ 备份完成"

# 恢复数据
restore:
	@echo "请指定备份文件，例如: make restore FILE=backups/kortix-data-20260201-120000.tar.gz"
	@if [ -z "$(FILE)" ]; then \
		echo "❌ 错误: 未指定 FILE 参数"; \
		exit 1; \
	fi
	@tar -xzf $(FILE)
	@echo "✅ 恢复完成"
