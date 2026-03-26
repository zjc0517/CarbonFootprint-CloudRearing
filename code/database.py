"""
Database Configuration Module
管理数据库连接与会话生成。
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# 默认使用本地 SQLite 数据库，商用生产环境可通过环境变量替换为 MySQL/PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./carbon_rearing.db")

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """依赖项：获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
