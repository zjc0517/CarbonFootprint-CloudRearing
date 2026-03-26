import streamlit as st
import sys
import os

# 确保能引入 carbon_engine
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 关键修改点
from carbon_engine.carbon_calculator import CarbonCalculator

st.set_page_config(page_title="Carbon Rearing Dashboard")
st.title("🌱 云养行业碳足迹计算与积分系统")
# 后面保持之前的业务代码不变...
