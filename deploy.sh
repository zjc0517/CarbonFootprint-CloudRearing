#!/bin/bash

# ==============================================================================
# CarbonFootprint-CloudRearing 自动化部署脚本
# 功能：环境检查、代码更新、镜像构建、容器重启、清理冗余
# ==============================================================================

# 设置严格模式：遇到错误立即停止
set -e

# 定义终端颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # 无颜色

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[WARN] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
}

# 1. 环境检查：Docker
log "开始环境预检..."
if ! [ -x "$(command -v docker)" ]; then
    error "错误: 未安装 Docker。请先安装 Docker 以继续。"
    exit 1
fi

# 2. 环境检查：Docker Compose
if ! [ -x "$(command -v docker-compose)" ]; then
    warn "未检测到独立 docker-compose 命令，尝试使用 'docker compose'..."
    DOCKER_COMPOSE="docker compose"
else
    DOCKER_COMPOSE="docker-compose"
fi

# 3. 拉取最新代码 (假设已在 Git 仓库目录)
if [ -d ".git" ]; then
    log "正在从远程仓库拉取最新代码..."
    git pull origin main
else
    warn "当前目录不是 Git 仓库，跳过 git pull。"
fi

# 4. 检查配置文件
if [ ! -f "deployment/.env" ]; then
    error "错误: 缺少 deployment/.env 配置文件！"
    echo "请根据 deployment/.env.example 创建并配置私钥和 RPC 地址。"
    exit 1
fi

# 5. 进入部署目录并重启服务
log "正在重新构建并启动 Docker 容器..."
cd deployment

# 停止旧容器并移除孤儿容器
$DOCKER_COMPOSE down --remove-orphans

# 构建镜像并后台启动
# --build 确保代码更改被同步到镜像中
$DOCKER_COMPOSE up -d --build

# 6. 清理冗余
log "正在清理过期的 Docker 镜像和缓存..."
docker image prune -f

# 7. 服务健康检查
log "正在等待服务启动..."
sleep 5

# 检查 API 状态 (假设 API 在 8000 端口)
if curl -s --head  --request GET http://localhost:8000/docs | grep "200 OK" > /dev/null; then
    log "✅ API 服务已成功启动：http://localhost:8000/docs"
else
    warn "❌ API 服务响应异常，请执行 'docker logs deployment-api-1' 查看日志。"
fi

# 检查 Dashboard 状态 (假设在 8501 端口)
if curl -s --head --request GET http://localhost:8501 | grep "200" > /dev/null; then
    log "✅ 可视化仪表盘已成功启动：http://localhost:8501"
else
    warn "❌ 仪表盘服务响应异常，请执行 'docker logs deployment-dashboard-1' 查看日志。"
fi

log "🎉 部署任务顺利完成！"
