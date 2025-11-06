import itertools

# TODO:
# [*]:向下继承，当选E96包含E24系统，E24天然包含E12

# E12系列
E12_SERIES = [10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82]
E12_BASE = [1E0, 1E1, 1E2, 1E3, 1E4, 1E5, 1E6]

# E24系列
E24_SERIES = [10, 11, 12, 13, 15, 16, 18, 20, 22, 24,
              27, 30, 33, 36, 39, 43, 47, 51, 56, 62, 68, 75, 82, 91]
E24_BASE = [1E0, 1E1, 1E2, 1E3, 1E4, 1E5, 1E6]

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
E96_BASE = [1E0, 1E1, 1E2, 1E3, 1E4, 1E5, 1E6, 1E7, 1E-1, 1E-2, 1E-3]

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


def parse_input_res_value(value: str) -> float:
    v = value.strip().upper()
    if v.endswith("R"):
        return float(v[:-1])
    elif v.endswith("K"):
        return float(v[:-1]) * 1e3
    elif v.endswith("M"):
        return float(v[:-1]) * 1e6
    else:
        try:
            return float(v)
        except ValueError:
            raise ValueError(f"无法解析数值: {value}")

# 生成电阻列表
def generate_e_series(series_name):
    if series_name == 'E96':
        global res_e24_list, res_e96_list
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

def find_best_divider(vout_target, vfb, r_min=1E3, r_max=1E6, series_name='E24', keep_r1=None, keep_r2=None):
    resistors = [r for r in generate_e_series(series_name) if r_min <= r <= r_max]
    best_error = float('inf')
    best_pair_list = []
    best_pair = None
    pair_index = 0

    if keep_r1 and keep_r2:
        return [(keep_r1, keep_r2, vfb * (1 + keep_r1 / keep_r2), 
                 abs(vfb * (1 + keep_r1 / keep_r2) - vout_target))]

    if keep_r1:
        for R2 in resistors:
            R1 = parse_input_res_value(keep_r1)
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
    elif keep_r2:
        for R1 in resistors:
            R2 = parse_input_res_value(keep_r2)
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
    else:
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
