FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 关键修改点：拷贝 carbon_engine 文件夹
COPY carbon_engine/ ./carbon_engine/
COPY visualization/ ./visualization/

EXPOSE 8000 8501

CMD ["sh", "-c", "uvicorn carbon_engine.api:app --host 0.0.0.0 --port 8000 & streamlit run visualization/app.py --server.port 8501 --server.address 0.0.0.0"]
