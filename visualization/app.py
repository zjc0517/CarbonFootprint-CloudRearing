"""
交互式仪表盘 - 碳足迹监控台
"""
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import sys
import os

# 确保能引入上层目录的模块
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from code.carbon_calculator import CarbonCalculator

st.set_page_config(page_title="Carbon Rearing Dashboard", layout="wide")

st.title("🌱 云养行业碳足迹计算与积分系统")

# 侧边栏：参数输入
with st.sidebar:
    st.header("参数配置")
    st.subheader("固碳参数 (Sink)")
    A = st.number_input("草场面积 A (ha)", value=500.0)
    EF_grass = st.number_input("草场固碳因子 EF_grass", value=1.2)
    M = st.number_input("粪便管理量 M (吨)", value=100.0)
    EF_manure = st.number_input("粪便减排因子 EF_manure", value=0.8)

    st.subheader("排放参数 (Emission)")
    E_feed = st.number_input("饲料碳排放 E_feed", value=150.0)
    E_enteric = st.number_input("肠道发酵排放 E_enteric", value=200.0)
    E_energy = st.number_input("能耗碳排放 E_energy", value=100.0)
    
    st.subheader("用户参数")
    W_user = st.slider("用户持有权益 W_user (%)", 0.0, 100.0, 5.0) / 100
    T_hold = st.number_input("持有时间 T_hold (年)", value=1.0)

# 触发计算
try:
    i_user = CarbonCalculator.calculate_carbon_credit(
        A, EF_grass, M, EF_manure, E_feed, E_enteric, E_energy, W_user, T_hold
    )
    
    carbon_sink = (A * EF_grass) + (M * EF_manure)
    carbon_emission = E_feed + E_enteric + E_energy

    # 顶部指标展示
    col1, col2, col3 = st.columns(3)
    col1.metric("总固碳量 (吨)", f"{carbon_sink:.2f}")
    col2.metric("总碳排放 (吨)", f"{carbon_emission:.2f}")
    col3.metric("您的碳积分 (I_user)", f"{i_user:.2f} 吨CO₂e")

    # 可视化图表
    st.markdown("### 📊 碳足迹构成分析")
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        # 饼图对比固碳与排放（使用绝对值作图以便直观显示比例）
        labels = ['总固碳量 (Sink)', '总碳排放 (Emission)']
        values = [carbon_sink, carbon_emission]
        fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4, 
                                        marker_colors=['#2E8B57', '#FF6347'])])
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_chart2:
        # 敏感性分析：持有时间对积分的影响 (模拟时间序列)
        times = np.linspace(0, 5, 20)
        credits = [(carbon_sink - carbon_emission) * W_user * t for t in times]
        fig_line = go.Figure(data=go.Scatter(x=times, y=credits, mode='lines+markers',
                                            line=dict(color='royalblue', width=3)))
        fig_line.update_layout(title="碳积分随时间推移的累积趋势", xaxis_title="时间 (年)", yaxis_title="积分 (I_user)")
        st.plotly_chart(fig_line, use_container_width=True)

except Exception as e:
    st.error(f"计算出错: {str(e)}")
