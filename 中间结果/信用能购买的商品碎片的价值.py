import json

from scipy.interpolate import interp1d


with open("中间结果/信用能购买的商品碎片的价值.json", 'r', encoding='utf-8') as f:
    obj: list[float] = json.load(f)

信用能购买的商品碎片的价值 = interp1d(range(len(obj)), obj, kind='cubic')
