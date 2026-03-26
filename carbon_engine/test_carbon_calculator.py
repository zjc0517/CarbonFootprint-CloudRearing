import pytest
import sys
import os

# 确保测试时能找到 carbon_engine 包
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 关键修改点：从新命名的 carbon_engine 导入
from carbon_engine.carbon_calculator import CarbonCalculator

def test_normal_calculation():
    result = CarbonCalculator.calculate_carbon_credit(
        A=500.0, EF_grass=1.2, M=100.0, EF_manure=0.8,
        E_feed=150.0, E_enteric=200.0, E_energy=100.0,
        W_user=0.1, T_hold=1.0
    )
    assert result == 23.0

def test_negative_values():
    with pytest.raises(ValueError):
        CarbonCalculator.calculate_carbon_credit(A=-1, EF_grass=1, M=1, EF_manure=1, E_feed=1, E_enteric=1, E_energy=1, W_user=0.1, T_hold=1)
