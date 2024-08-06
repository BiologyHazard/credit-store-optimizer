import json
from statistics import mean

from scipy.interpolate import interp1d

from 统计结果 import 信用交易所统计字典


if __name__ == '__main__':
    每日获得的信用枚举空间 = range(0, 1501, 1)
    信用能购买的商品碎片的价值列表 = []
    for 商店 in 信用交易所统计字典.values():
        已花费信用 = 0
        已购买物品的价值 = 0
        x: list[float] = [0]
        y: list[float] = [0]
        for 商品序号, 商品 in sorted(enumerate(商店.商品列表), key=lambda x: x[1].性价比, reverse=True):
            已花费信用 += 商品.现价
            已购买物品的价值 += 商品.价值
            x.append(已花费信用)
            y.append(已购买物品的价值)
        linear_interpolation = interp1d(x, y, kind='linear', bounds_error=False, fill_value=已购买物品的价值, assume_sorted=True)
        信用能购买的商品碎片的价值列表.append(linear_interpolation(每日获得的信用枚举空间))

    信用能购买的商品碎片的价值 = [mean(价值) for 价值 in zip(*信用能购买的商品碎片的价值列表)]

    with open("中间结果/信用能购买的商品碎片的价值.json", 'w', encoding='utf-8') as f:
        json.dump(信用能购买的商品碎片的价值, f, indent=4)
