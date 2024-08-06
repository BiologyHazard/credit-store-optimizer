import json
import math
import multiprocessing
import random

from 中间结果.K··· import K_N减1_·_·
from 中间结果.价格价值矩阵 import 价值矩阵, 价格矩阵


def 计算每日获得的信用的价值(每日获得的信用: int, 顺序: list[int]) -> float:
    K_N减1_C_· = [K_N减1_·_·(每日获得的信用, c) for c in range(301)]
    当前信用 = 每日获得的信用
    已购买总价值 = 0
    for 商店序号 in 顺序:
        价格行 = 价格矩阵[商店序号]
        价值行 = 价值矩阵[商店序号]
        目标函数最大值 = -math.inf
        for 总价格, 总价值 in zip(价格行, 价值行):
            if 总价格 <= 当前信用:
                剩余信用 = 当前信用 - 总价格
                可继承的信用 = min(剩余信用, 300)
                目标函数 = 总价值 + K_N减1_C_·[可继承的信用]
                if 目标函数 > 目标函数最大值:
                    目标函数最大值 = 目标函数
                    最优策略总价格 = 总价格
                    最优策略总价值 = 总价值
        已购买总价值 += 最优策略总价值
        当前信用 -= 最优策略总价格
        assert 当前信用 >= 0
        继承的信用 = min(当前信用, 300)
        当前信用 = 继承的信用 + 每日获得的信用
    return 已购买总价值 / len(顺序)


if __name__ == '__main__':
    random.seed(0)
    商店数量 = len(价格矩阵)
    顺序 = list(range(商店数量)) * 5
    random.shuffle(顺序)

    每日获得的信用列表 = range(0, 1001, 5)
    with multiprocessing.Pool() as pool:
        每日获得的信用的价值列表 = pool.starmap(
            计算每日获得的信用的价值,
            [(每日获得的信用, 顺序) for 每日获得的信用 in 每日获得的信用列表],
        )
    每日获得的信用的价值 = dict(zip(map(str, 每日获得的信用列表), 每日获得的信用的价值列表))

    with open("中间结果/每日获得的信用的价值.json", 'w', encoding='utf-8') as f:
        json.dump(每日获得的信用的价值, f, ensure_ascii=False, indent=4)
