"""碳足迹计算器 — 单元测试."""
import pytest
from .carbon_calculator import CarbonCalculator, IPCCModel, SheepParams


class TestCarbonCalculator:

    def test_tier1_defaults_exist(self):
        d = CarbonCalculator.defaults(IPCCModel.TIER1)
        for k in ["grassland_factor", "manure_factor", "feed_emission", "enteric_emission", "energy_emission"]:
            assert k in d and d[k] > 0

    def test_tier2_defaults_exist(self):
        d = CarbonCalculator.defaults(IPCCModel.TIER2)
        for k in ["grassland_factor", "manure_factor", "feed_emission", "enteric_emission", "energy_emission"]:
            assert k in d and d[k] > 0

    def test_calculate_basic(self):
        params = SheepParams(area_km2=0.001, grassland_factor=0.65, manure_mass_t=0.5,
                            manure_factor=0.028, feed_emission_t=0.12, enteric_emission_t=0.30,
                            energy_emission_t=0.04, user_share=1.0, hold_years=1.0)
        report = CarbonCalculator.calculate(params, IPCCModel.TIER2)
        assert report.carbon_sink > 0
        assert report.carbon_emission > 0
        assert report.user_credit == round(report.net_credit, 4)

    def test_calculate_half_share(self):
        params = SheepParams(area_km2=0.002, grassland_factor=0.5, manure_mass_t=1.0,
                            manure_factor=0.02, feed_emission_t=0.15, enteric_emission_t=0.25,
                            energy_emission_t=0.05, user_share=0.5, hold_years=1.0)
        report = CarbonCalculator.calculate(params, IPCCModel.TIER1)
        assert report.user_credit == round(report.net_credit * 0.5, 4)

    def test_zero_share(self):
        params = SheepParams(area_km2=0.001, grassland_factor=0.5, manure_mass_t=0.5,
                            manure_factor=0.02, feed_emission_t=0.15, enteric_emission_t=0.25,
                            energy_emission_t=0.05, user_share=0.0, hold_years=1.0)
        report = CarbonCalculator.calculate(params, IPCCModel.TIER1)
        assert report.user_credit == 0.0

    def test_invalid_share_raises(self):
        params = SheepParams(area_km2=0.001, grassland_factor=0.5, manure_mass_t=0.5,
                            manure_factor=0.02, feed_emission_t=0.15, enteric_emission_t=0.25,
                            energy_emission_t=0.05, user_share=1.5, hold_years=1.0)
        with pytest.raises(ValueError):
            CarbonCalculator.calculate(params, IPCCModel.TIER1)

    def test_negative_hold_years_raises(self):
        params = SheepParams(area_km2=0.001, grassland_factor=0.5, manure_mass_t=0.5,
                            manure_factor=0.02, feed_emission_t=0.15, enteric_emission_t=0.25,
                            energy_emission_t=0.05, user_share=1.0, hold_years=0)
        with pytest.raises(ValueError):
            CarbonCalculator.calculate(params, IPCCModel.TIER1)

    @pytest.mark.parametrize("count", [1, 5, 100])
    def test_from_per_sheep(self, count):
        report = CarbonCalculator.from_per_sheep(sheep_count=count)
        assert report.user_credit != 0
        assert report.detail["grassland_sink"] > 0

    def test_batch_calculate(self):
        params_list = [
            SheepParams(0.001, 0.65, 0.5, 0.028, 0.12, 0.30, 0.04),
            SheepParams(0.002, 0.65, 0.6, 0.028, 0.12, 0.30, 0.04),
        ]
        reports = CarbonCalculator.batch_calculate(params_list, IPCCModel.TIER2)
        assert len(reports) == 2
        assert reports[0].user_credit != reports[1].user_credit

    def test_tier2_higher_sink_than_tier1(self):
        report1 = CarbonCalculator.from_per_sheep(model=IPCCModel.TIER1)
        report2 = CarbonCalculator.from_per_sheep(model=IPCCModel.TIER2)
        assert report2.carbon_sink > report1.carbon_sink

    def test_report_contains_detail(self):
        report = CarbonCalculator.from_per_sheep()
        for k in ["grassland_sink", "manure_sink", "feed_emission", "enteric_emission", "energy_emission"]:
            assert k in report.detail
