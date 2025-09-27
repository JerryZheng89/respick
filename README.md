# Resister picker
## Power Divider Resistor picker

```
usage: resistor_divider_picker.py [-h] --vout VOUT --vfb VFB [--rmin RMIN] [--rmax RMAX] [--series {E24,E12,E96}]

🔧 自动从标准阻值中选出最合适的电阻对用于DCDC分压反馈。

options:
  -h, --help            show this help message and exit
  --vout VOUT           Target output voltage (e.g. 3.3)
  --vfb VFB             FB voltage of DCDC IC (e.g. 0.8)
  --rmin RMIN           Minimum resistor value (default 1k)
  --rmax RMAX           Maximum resistor value (default 1M)
  --series {E24,E12,E96}
                        Resistor series to use

示例：
  respick --vout 3.3 --vfb 0.8 --series E24
  respick --vout 5 --vfb 1.25 --rmin 1000 --rmax 100000 --series E12

说明：
  R1接在输出与FB之间，R2接在FB与GND之间
  输出电压 Vout = Vfb * (1 + R1/R2)
```

- 本地测试
```shell
python -m respick --vout 3.3 --vfb 0.6
```

- 本地安装
```shell
pip install -e .
```

- 本地cli终端测试
```shell
respick --vout 1.8 --vfb 0.6 --series E24
```

## build
```shell
python -m build
```

## upload pypi
```shell
twine upload dist/*
```