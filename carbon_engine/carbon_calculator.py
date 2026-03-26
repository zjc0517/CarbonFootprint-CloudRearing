import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CarbonCalculator:
    @staticmethod
    def calculate_carbon_credit(A, EF_grass, M, EF_manure, E_feed, E_enteric, E_energy, W_user, T_hold):
        # 基础校验
        params = [A, EF_grass, M, EF_manure, E_feed, E_enteric, E_energy, W_user, T_hold]
        if any(not isinstance(p, (int, float)) or p < 0 for p in params):
            raise ValueError("所有输入参数必须为非负数字")
        if not (0 <= W_user <= 1):
            raise ValueError("W_user 权益比例必须在 0 到 1 之间")

        # 公式逻辑
        carbon_sink = (A * EF_grass) + (M * EF_manure)
        carbon_emission = E_feed + E_enteric + E_energy
        i_user = (carbon_sink - carbon_emission) * W_user * T_hold
        
        return round(float(i_user), 4)
