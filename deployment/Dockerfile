# 基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制代码与依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY code/ ./code/
COPY visualization/ ./visualization/

# 暴露端口 (假设 API跑在8000，Streamlit跑在8501)
EXPOSE 8000 8501

# 启动脚本 (可使用 supervisord 或编写 shell 脚本同时启动前后端)
CMD ["sh", "-c", "uvicorn code.api:app --host 0.0.0.0 --port 8000 & streamlit run visualization/app.py --server.port 8501"]
