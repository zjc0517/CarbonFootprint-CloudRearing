from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

# 关键修改点：使用相对导入或重命名后的包名
from .carbon_calculator import CarbonCalculator
from . import models, database

app = FastAPI(title="CarbonFootprint API")

# 后面保持之前的业务代码不变...
# (省略重复的业务逻辑，确保开头的 import 正确即可)
