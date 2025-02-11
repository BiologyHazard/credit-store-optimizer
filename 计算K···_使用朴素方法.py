# 注：代码为了可读性牺牲了性能，实际运行起来非常慢。
# 代码仓库 https://github.com/BiologyHazard/credit-store-optimizer 中有为性能优化后的代码。

import math
from collections.abc import Sequence
from itertools import product
from statistics import mean

from 信用交易所模型 import 信用交易所
from 统计结果 import 信用交易所统计结果


def 计算总价格(商店: 信用交易所, 购买指标向量: Sequence[bool]) -> int:
    return sum(商品.现价 for i, 商品 in enumerate(商店.商品列表) if 购买指标向量[i])


def 计算总价值(商店: 信用交易所, 购买指标向量: Sequence[bool]) -> float:
    return sum(商品.价值 for i, 商品 in enumerate(商店.商品列表) if 购买指标向量[i])


def 求解单个商店最优购买策略(商店: 信用交易所, 当前信用: int, KnC·: list[float]) -> tuple[float, tuple[bool, ...]]:
    """在 2**10 种购买方案中选一种不超支的，使得 当天购买的物品总价值 + KnC·[能够继承的信用] 最大"""
    目标函数最大值: float = -math.inf
    for 购买指标向量 in product((False, True), repeat=len(商店.商品列表)):  # 枚举 2 ** 10 种购买方案
        总价格: int = 计算总价格(商店, 购买指标向量)
        总价值: float = 计算总价值(商店, 购买指标向量)
        if 总价格 <= 当前信用:
            剩余信用: int = 当前信用 - 总价格
            能够继承的信用: int = min(剩余信用, 300)
            目标函数: float = 总价值 + KnC·[能够继承的信用]
            if 目标函数 > 目标函数最大值:
                目标函数最大值 = 目标函数
                最优策略购买指标向量 = 购买指标向量

    return 目标函数最大值, 最优策略购买指标向量


if __name__ == '__main__':
    每日获得的信用C = 813
    考虑的天数N = 11

    K0C·: list[float] = [0 for _ in range(301)]
    K·C·: list[list[float]] = [K0C·]

    for n in range(1, 考虑的天数N):
        K_n减1_C_·: list[float] = K·C·[-1]
        KnC·: list[float] = [0 for _ in range(301)]
        for 继承的信用c in range(301):
            KnCc的采样: list[float] = []
            for 商店 in 信用交易所统计结果:
                目标函数最大值, _ = 求解单个商店最优购买策略(商店, 继承的信用c + 每日获得的信用C, K_n减1_C_·)
                KnCc的采样.append(目标函数最大值)
            KnC·[继承的信用c] = mean(KnCc的采样)  # 以均值作为期望的估计
        K·C·.append(KnC·)

    for n, KnC· in enumerate(K·C·):
        print(f'K_{n}_{每日获得的信用C}_·: {KnC·}')
