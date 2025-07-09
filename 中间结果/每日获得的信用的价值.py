import json

from scipy.interpolate import interp1d, UnivariateSpline


with open("中间结果/每日获得的信用的价值.json", 'r', encoding='utf-8') as f:
    obj: dict[str, float] = json.load(f)


def 计算信用能购买的商品碎片的价值的导数(每日获得的信用: int) -> float:
    l = max(每日获得的信用 - 1, 0)
    r = min(每日获得的信用 + 1, max(每日获得的信用列表))
    return (每日获得的信用的价值(r) - 每日获得的信用的价值(l)) / (r - l)


每日获得的信用列表 = list(map(int, obj))
每日获得的信用的价值列表 = list(obj.values())

每日获得的信用的价值 = interp1d(每日获得的信用列表, 每日获得的信用的价值列表, kind='linear')
每日获得的信用的价值的导数列表 = [计算信用能购买的商品碎片的价值的导数(i) for i in range(max(每日获得的信用列表) + 1)]
每日获得的信用的价值的导数 = interp1d(range(max(每日获得的信用列表) + 1), 每日获得的信用的价值的导数列表, kind='linear')
