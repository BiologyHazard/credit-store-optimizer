import json

from scipy.interpolate import interp1d, UnivariateSpline


with open("中间结果/每日获得的信用的价值.json", 'r', encoding='utf-8') as f:
    obj: dict[str, float] = json.load(f)

每日获得的信用列表 = list(map(int, obj))
每日获得的信用的价值列表 = list(obj.values())

每日获得的信用的价值 = interp1d(每日获得的信用列表, 每日获得的信用的价值列表, kind='cubic')
每日获得的信用的价值的导数 = UnivariateSpline(每日获得的信用列表, 每日获得的信用的价值列表, s=0.004).derivative()
