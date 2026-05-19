"""命令行工具 — python -m carbon_engine.cli"""

import argparse, json
from .carbon_calculator import CarbonCalculator, IPCCModel


def main():
    p = argparse.ArgumentParser(description="绒光公社 碳足迹计算引擎")
    p.add_argument("--sheep-id", default="RG-001")
    p.add_argument("--count", type=int, default=1)
    p.add_argument("--model", choices=["tier1", "tier2"], default="tier2")
    p.add_argument("--area", type=float, default=0.006, help="单只羊放牧面积(km²)")
    p.add_argument("--manure", type=float, default=0.5, help="单只羊粪便量(t/yr)")
    p.add_argument("--share", type=float, default=1.0)
    p.add_argument("--years", type=float, default=1.0)
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    model = IPCCModel(args.model)
    report = CarbonCalculator.from_per_sheep(
        sheep_count=args.count, area_per_sheep=args.area,
        manure_per_sheep=args.manure, user_share=args.share,
        hold_years=args.years, model=model,
    )
    report.sheep_id = args.sheep_id

    if args.json:
        print(json.dumps({
            "sheep_id": report.sheep_id, "model": report.model.value,
            "carbon_sink_tco2": report.carbon_sink,
            "carbon_emission_tco2e": report.carbon_emission,
            "net_credit_tco2e": report.net_credit,
            "user_credit_tco2e": report.user_credit,
            "detail": report.detail,
        }, indent=2, ensure_ascii=False))
    else:
        print(f"碳足迹报告: {report.sheep_id}  (IPCC {report.model.value})")
        print(f"  碳汇:   {report.carbon_sink:.4f} tCO2")
        print(f"  排放:   {report.carbon_emission:.4f} tCO2e")
        print(f"  净碳汇: {report.net_credit:.4f} tCO2e")
        print(f"  用户配额: {report.user_credit:.4f} tCO2e")


if __name__ == "__main__":
    main()
