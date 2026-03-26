"""
FastAPI RESTful API Module
对前端和第三方系统提供碳积分计算与查询接口。
"""
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import List

from .carbon_calculator import CarbonCalculator
from . import models, database

# 初始化数据库表
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="CarbonFootprint-CloudRearing API",
    description="云养行业碳足迹计算与积分系统后端接口",
    version="1.0.0"
)

# Pydantic 数据验证模型
class CalculationRequest(BaseModel):
    user_id: str = Field(..., description="用户唯一标识或钱包地址")
    A: float = Field(..., ge=0, description="草场面积 (ha)")
    EF_grass: float = Field(1.2, ge=0, description="草场固碳因子")
    M: float = Field(..., ge=0, description="粪便管理量 (吨)")
    EF_manure: float = Field(0.8, ge=0, description="粪便减排因子")
    E_feed: float = Field(..., ge=0, description="饲料碳排放")
    E_enteric: float = Field(..., ge=0, description="肠道发酵排放")
    E_energy: float = Field(..., ge=0, description="能耗碳排放")
    W_user: float = Field(..., ge=0, le=1, description="用户持有权益占比 (0-1)")
    T_hold: float = Field(..., ge=0, description="持有时间 (年)")

class CalculationResponse(BaseModel):
    user_id: str
    total_sink: float
    total_emission: float
    net_credit: float
    record_id: int

@app.post("/api/v1/calculate", response_model=CalculationResponse, summary="计算并保存碳积分")
def calculate_and_store(req: CalculationRequest, db: Session = Depends(database.get_db)):
    try:
        # 1. 调用核心算法计算
        i_user = CarbonCalculator.calculate_carbon_credit(
            req.A, req.EF_grass, req.M, req.EF_manure,
            req.E_feed, req.E_enteric, req.E_energy,
            req.W_user, req.T_hold
        )
        
        total_sink = (req.A * req.EF_grass) + (req.M * req.EF_manure)
        total_emission = req.E_feed + req.E_enteric + req.E_energy
        
        # 2. 持久化到数据库
        db_record = models.CarbonRecord(
            user_id=req.user_id,
            grass_area=req.A,
            manure_management=req.M,
            feed_emission=req.E_feed,
            enteric_emission=req.E_enteric,
            energy_emission=req.E_energy,
            user_weight=req.W_user,
            hold_time=req.T_hold,
            total_sink=total_sink,
            total_emission=total_emission,
            net_credit=i_user
        )
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
        
        return {
            "user_id": req.user_id,
            "total_sink": round(total_sink, 4),
            "total_emission": round(total_emission, 4),
            "net_credit": round(i_user, 4),
            "record_id": db_record.id
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="服务器内部错误")
