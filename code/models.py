"""
Database Models Module
定义数据表结构。
"""
from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime
from .database import Base

class CarbonRecord(Base):
    """碳积分计算历史记录表"""
    __tablename__ = "carbon_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50), index=True, nullable=False) # 关联的用户ID或钱包地址
    
    # 输入参数
    grass_area = Column(Float, nullable=False)
    manure_management = Column(Float, nullable=False)
    feed_emission = Column(Float, nullable=False)
    enteric_emission = Column(Float, nullable=False)
    energy_emission = Column(Float, nullable=False)
    user_weight = Column(Float, nullable=False)
    hold_time = Column(Float, nullable=False)
    
    # 计算结果
    total_sink = Column(Float, nullable=False)
    total_emission = Column(Float, nullable=False)
    net_credit = Column(Float, nullable=False) # 最终的 I_user
    
    # 元数据
    created_at = Column(DateTime, default=datetime.utcnow)
    tx_hash = Column(String(100), nullable=True) # 预留给区块链的上链交易哈希
