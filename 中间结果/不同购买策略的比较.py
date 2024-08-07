import json
from scipy.interpolate import interp1d


with open("中间结果/不同购买策略的比较.json", 'r', encoding='utf-8') as f:
    obj: dict[str, dict[str, float]] = json.load(f)


不同购买策略的比较: dict[str, interp1d] = {}
for 策略名称, 策略表现 in obj.items():
    x = list(map(int, 策略表现.keys()))
    y = list(策略表现.values())
    不同购买策略的比较[策略名称] = interp1d(x, y, kind='cubic')
