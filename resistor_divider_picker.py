#!/usr/bin/env python3
import argparse
import itertools
import sys

# TODO:
# [*]:向下继承，当选E96包含E24系统，E24天然包含E12

# E12系列
E12_SERIES = [10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82]
E12_BASE = [1E1, 1E2, 1E3, 1E4, 1E5, 1E6]

# E24系列
E24_SERIES = [10, 11, 12, 13, 15, 16, 18, 20, 22, 24,
              27, 30, 33, 36, 39, 43, 47, 51, 56, 62, 68, 75, 82, 91]
E24_BASE = [1E1, 1E2, 1E3, 1E4, 1E5, 1E6]

# E96系列
E96_SERIES = [
    100.0, 102.0, 105.0, 107.0, 110.0, 113.0, 115.0, 118.0, 121.0, 124.0,
    127.0, 130.0, 133.0, 137.0, 140.0, 143.0, 147.0, 150.0, 154.0, 158.0,
    162.0, 165.0, 169.0, 174.0, 178.0, 182.0, 187.0, 191.0, 196.0, 200.0,
    205.0, 210.0, 215.0, 221.0, 226.0, 232.0, 237.0, 243.0, 249.0, 255.0,
    261.0, 267.0, 274.0, 280.0, 287.0, 294.0, 301.0, 309.0, 316.0, 324.0,
    332.0, 340.0, 348.0, 357.0, 365.0, 374.0, 383.0, 392.0, 402.0, 412.0,
    422.0, 432.0, 442.0, 453.0, 464.0, 475.0, 487.0, 499.0, 511.0, 523.0,
    536.0, 549.0, 562.0, 576.0, 590.0, 604.0, 619.0, 634.0, 649.0, 665.0,
    681.0, 698.0, 715.0, 732.0, 750.0, 768.0, 787.0, 806.0, 825.0, 845.0,
    866.0, 887.0, 909.0, 931.0, 953.0, 976.0]
E96_BASE = [1E1, 1E2, 1E3, 1E4, 1E5, 1E6, 1E7, 1E-1, 1E-2, 1E-3]

series_map = {
    "E12": E12_SERIES,
    "E24": E24_SERIES,
    "E96": E96_SERIES,
}

base_map = {
    "E12": E12_BASE,
    "E24": E24_BASE,
    "E96": E96_BASE,
}
res_e24_list = []
res_e96_list = []

# 生成电阻列表
def generate_e_series(series_name):
    if series_name == 'E96':
        decades = base_map[series_name]
        series = series_map[series_name]
        res_e96_list = [round(base * decade, 1) for base in series for decade in decades]
        decades = base_map['E24']
        series = series_map['E24']
        res_e24_list = [round(base * decade, 1) for base in series for decade in decades]
        return sorted(list(set(res_e24_list+res_e96_list)))
    else:
        decades = base_map[series_name]
        series = series_map[series_name]
        return sorted(round(base * decade, 1) for base in series for decade in decades)

def format_resistor(value_ohm: float) -> str:
    if value_ohm < 1_000:
        return f"{value_ohm:.1f}R"
    elif value_ohm < 1_000_000:
        return f"{value_ohm / 1_000:.1f}K"
    elif value_ohm < 1_000_000_000:
        return f"{value_ohm / 1_000_000:.1f}M"
    else:
        return f"{value_ohm / 1_000_000_000:.1f}G"


def find_best_divider(vout_target, vfb, r_min, r_max, series_name):
    resistors = [r for r in generate_e_series(series_name) if r_min <= r <= r_max]
    best_error = float('inf')
    best_pair_list = []
    best_pair = None
    pair_index = 0

    for R1, R2 in itertools.product(resistors, repeat=2):
        vout = vfb * (1 + R1 / R2)
        error = abs(vout - vout_target)
        if error < best_error:
            best_error = error
            best_pair = (R1, R2, vout, error)
            best_pair_list.clear()
            best_pair_list.append(best_pair)
        elif error == best_error:
            best_pair = (R1, R2, vout, error)
            best_pair_list.append(best_pair)

    return best_pair_list

# description="Select best resistor pair for DCDC voltage divider.")
def main():
    parser = argparse.ArgumentParser(
        description="🔧 自动从标准阻值中选出最合适的电阻对用于DCDC分压反馈。",
        epilog="""
示例：
  python resistor_divider_picker.py --vout 3.3 --vfb 0.8 --series E24
  python resistor_divider_picker.py --vout 5 --vfb 1.25 --rmin 1000 --rmax 100000 --series E12

说明：
  R1接在输出与FB之间，R2接在FB与GND之间
  输出电压 Vout = Vfb * (1 + R1/R2)
        """
        , 
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("--vout", type=float, required=True, help="Target output voltage (e.g. 3.3)")
    parser.add_argument("--vfb", type=float, required=True, help="FB voltage of DCDC IC (e.g. 0.8)")
    parser.add_argument("--rmin", type=float, default=1e3, help="Minimum resistor value (default 1k)")
    parser.add_argument("--rmax", type=float, default=1e6, help="Maximum resistor value (default 1M)")
    parser.add_argument("--series", choices=["E24", "E12", "E96"], default="E24", help="Resistor series to use")

    # ✅ 如果没有传任何参数，显示帮助信息
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    best_list = find_best_divider(args.vout, args.vfb, args.rmin, args.rmax, 
                             args.series)

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

if __name__ == "__main__":
    main()
