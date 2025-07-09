import json

from scipy.interpolate import interp1d


with open("中间结果/信用能购买的商品碎片的价值.json", 'r', encoding='utf-8') as f:
    obj: list[float] = json.load(f)


def 计算信用能购买的商品碎片的价值的导数(每日获得的信用: int) -> float:
    l = max(每日获得的信用 - 1, 0)
    r = min(每日获得的信用 + 1, len(obj) - 1)
    return (obj[r] - obj[l]) / (r - l)


信用能购买的商品碎片的价值的导数列表 = [计算信用能购买的商品碎片的价值的导数(i) for i in range(len(obj))]
信用能购买的商品碎片的价值 = interp1d(range(len(obj)), obj, kind='linear')
信用能购买的商品碎片的价值的导数 = interp1d(range(len(obj)), 信用能购买的商品碎片的价值的导数列表, kind='linear')
