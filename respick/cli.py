import sys
import argparse
from .core import find_best_divider

def format_resistor(value_ohm: float) -> str:
    if value_ohm < 1_000:
        return f"{value_ohm:.1f}R"
    elif value_ohm < 1_000_000:
        return f"{value_ohm / 1_000:.1f}K"
    elif value_ohm < 1_000_000_000:
        return f"{value_ohm / 1_000_000:.1f}M"
    else:
        return f"{value_ohm / 1_000_000_000:.1f}G"

def main():
    parser = argparse.ArgumentParser(
        description="🔧 自动从标准阻值中选出最合适的电阻对用于DCDC分压反馈。",
        epilog="""
示例：
  respick --vout 3.3 --vfb 0.8 --series E24
  respick --vout 5 --vfb 1.25 --rmin 1000 --rmax 100000 --series E12

说明：
  R1接在输出与FB之间，R2接在FB与GND之间
  输出电压 Vout = Vfb * (1 + R1/R2)
        """
        , 
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--vout", type=float, required=True, help="Target output voltage")
    parser.add_argument("--vfb", type=float, default=0.6, help="Feedback reference voltage (default: 0.8V)")
    parser.add_argument("--r1", type=str, default=None, help="Fixed R1 value (optional)")
    parser.add_argument("--r2", type=str, default=None, help="Fixed R2 value (optional)")
    parser.add_argument("--rmin", type=float, default=1e3, help="Minimum resistor value (default 1k)")
    parser.add_argument("--rmax", type=float, default=1e6, help="Maximum resistor value (default 1M)")
    parser.add_argument("--series", choices=["E24", "E12", "E96"], default="E24", help="Resistor series to use")
    # ✅ 如果没有传任何参数，显示帮助信息
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    best_list = find_best_divider(args.vout, args.vfb, args.rmin, args.rmax, 
                             args.series, keep_r1=args.r1, keep_r2=args.r2)
    if len(best_list):
        for index, best in enumerate(best_list):
            r1, r2, vout, err = best
            r1_format = format_resistor(r1)
            r2_format = format_resistor(r2)

            # print(f"✅ 最佳组合: R1 = {r1:.1f} Ω, R2 = {r2:.1f} Ω")
            print(f"✅ 最佳组合{index}: R1 = {r1_format}, R2 = {r2_format}")
        print(f"→ 输出电压 Vout = {vout:.4f} V，误差 = {err:.4f} V ({(err / args.vout) * 100:.2f} %)")
    else:
        print("❌ 没有找到合适的电阻组合")
