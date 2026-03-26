import pytest
# 使用相对导入，避免 sys.path 混乱
from .carbon_calculator import CarbonCalculator

def test_normal_calculation():
    # 测试数据
    result = CarbonCalculator.calculate_carbon_credit(
        500.0, 1.2, 100.0, 0.8, 150.0, 200.0, 100.0, 0.1, 1.0
    )
    assert result == 23.0

def test_negative_input():
    with pytest.raises(ValueError):
        CarbonCalculator.calculate_carbon_credit(-1, 1, 1, 1, 1, 1, 1, 0.1, 1)

def test_invalid_weight():
    with pytest.raises(ValueError):
        CarbonCalculator.calculate_carbon_credit(500, 1, 100, 1, 100, 100, 100, 1.5, 1)
