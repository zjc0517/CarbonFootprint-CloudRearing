"""
Unit Tests for Carbon Calculator
"""
import pytest
from code.carbon_calculator import CarbonCalculator

def test_normal_calculation():
    """测试常规合法输入"""
    result = CarbonCalculator.calculate_carbon_credit(
        A=500.0, EF_grass=1.2, M=100.0, EF_manure=0.8,
        E_feed=150.0, E_enteric=200.0, E_energy=100.0,
        W_user=0.1, T_hold=1.0
    )
    # 固碳: 500*1.2 + 100*0.8 = 600 + 80 = 680
    # 排放: 150 + 200 + 100 = 450
    # 净碳: 680 - 450 = 230
    # 用户积分: 230 * 0.1 * 1.0 = 23.0
    assert result == 23.0

def test_negative_values():
    """测试负数边界拦截"""
    with pytest.raises(ValueError):
        CarbonCalculator.calculate_carbon_credit(
            A=-500.0, EF_grass=1.2, M=100.0, EF_manure=0.8,
            E_feed=150.0, E_enteric=200.0, E_energy=100.0,
            W_user=0.1, T_hold=1.0
        )

def test_invalid_weight():
    """测试用户权益比例越界拦截"""
    with pytest.raises(ValueError):
        CarbonCalculator.calculate_carbon_credit(
            A=500.0, EF_grass=1.2, M=100.0, EF_manure=0.8,
            E_feed=150.0, E_enteric=200.0, E_energy=100.0,
            W_user=1.5, T_hold=1.0 # W_user 必须 <= 1
        )
