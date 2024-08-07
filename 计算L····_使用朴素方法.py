import math
from functools import lru_cache
from statistics import mean

import numpy as np
from scipy.interpolate import interp1d

from 中间结果.价格价值矩阵 import 价值矩阵, 价格矩阵


@lru_cache(maxsize=None)
def _get_LnDc·(LnDc·) -> interp1d:
    return interp1d(range(12), LnDc·, kind='linear')


def LnDc·(LnDc·, e) -> float:
    return float(_get_LnDc·(tuple(LnDc·))(e))


def 求解单个商店最优购买策略(价格行, 价值行, 当前信用: int, 当前线索: float, LnD··) -> float:
    """在 2**10 种购买方案中选一种不超支的，使得 当天购买的物品总价值 + LnD··(能够继承的信用, 能够继承的线索) 最大"""
    # 先传递溢出的线索
    if 当前线索 > 11:
        传递获得的信用数量: int = math.ceil((当前线索 - 11) * 20)
        传递的线索数量: float = 传递获得的信用数量 / 20
        当前信用 += 传递获得的信用数量
        当前线索 -= 传递的线索数量
    最多可使用的信用: int = math.floor(当前信用 + 20 * 当前线索)
    目标函数最大值: float = -math.inf
    for 总价格, 总价值 in zip(价格行, 价值行):  # 枚举 2 ** 10 种购买方案
        if 总价格 <= 最多可使用的信用:
            剩余信用: int = 当前信用 - 总价格
            # 补足不足的信用
            if 剩余信用 < 0:
                能够继承的线索: float = 当前线索 + 剩余信用 / 20
                剩余信用 = 0
            else:
                能够继承的线索 = 当前线索
            能够继承的信用: int = min(剩余信用, 300)
            目标函数: float = 总价值 + LnDc·(LnD··[能够继承的信用], 能够继承的线索)
            if 目标函数 > 目标函数最大值:
                目标函数最大值 = 目标函数

    return 目标函数最大值


if __name__ == '__main__':
    每日获得的信用D = 738  # = round(813.32 - 20 * 3.783)
    每日获得的线索E = 3.783
    考虑的天数N = 2

    L0D·· = np.zeros((301, 12))
    L·D·· = np.zeros((考虑的天数N, 301, 12))
    L·D··[0] = L0D··

    for n in range(1, 考虑的天数N):
        L_n减1_D_·_· = L·D··[n - 1]
        LnD·· = np.zeros((301, 12))
        for 继承的信用c in range(301):
            for 继承的线索e in range(12):
                LnDce的采样: list[float] = []
                for 价格行, 价值行 in zip(价格矩阵[:1], 价值矩阵[:1]):
                    目标函数最大值: float = 求解单个商店最优购买策略(
                        价格行, 价值行, 继承的信用c + 每日获得的信用D, 继承的线索e + 每日获得的线索E, L_n减1_D_·_·)
                    LnDce的采样.append(目标函数最大值)
                LnD··[继承的信用c, 继承的线索e] = mean(LnDce的采样)  # 以均值作为期望的估计
        L·D··[n] = LnD··

    for n, LnD·· in enumerate(L·D··):
        print(f'L_{n}_{每日获得的信用D}_·: {LnD··}')
