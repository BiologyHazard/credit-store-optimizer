import math
import random
from abc import ABC, abstractmethod
from itertools import product
from typing import Sequence

from 信用交易所模型 import 信用交易所, 信用交易所商品
from 统计结果 import 信用交易所统计字典


def 计算未购买的物品列表(商店: 信用交易所) -> list[tuple[int, 信用交易所商品]]:
    return [(商品序号, 商品) for 商品序号, 商品 in enumerate(商店.商品列表) if not 商品.已购买]


def 计算总价格(商店: 信用交易所, 购买指标向量: Sequence[bool]) -> int:
    return sum(商品.现价 for i, 商品 in enumerate(商店.商品列表) if 购买指标向量[i])


def 计算总价值(商店: 信用交易所, 购买指标向量: Sequence[bool]) -> float:
    return sum(商品.价值 for i, 商品 in enumerate(商店.商品列表) if 购买指标向量[i])


class 信用交易所购买策略(ABC):
    @abstractmethod
    def 求解(self, 商店: 信用交易所) -> Sequence[bool]:
        """
        返回一个 bool 序列，表示是否购买对应的商品。若商品原来就已购买，则对应位置为 `False`
        """
        pass


class 啥都不买策略(信用交易所购买策略):
    def 求解(self, 商店: 信用交易所) -> tuple[bool, ...]:
        return tuple(False for _ in 商店.商品列表)


class 随机购买_直到不能购买为止策略(信用交易所购买策略):
    def 求解(self, 商店: 信用交易所) -> list[bool]:
        当前信用 = 商店.剩余信用
        购买指标向量 = [False for _ in 商店.商品列表]
        未购买的商品序号列表 = 计算未购买的物品列表(商店)
        random.shuffle(未购买的商品序号列表)
        while 未购买的商品序号列表:
            商品序号, 商品 = 未购买的商品序号列表.pop()
            if 商品.现价 <= 当前信用:
                购买指标向量[商品序号] = True
                当前信用 -= 商品.现价
            else:
                break
        return 购买指标向量


class 从左到右购买_直到不能购买为止策略(信用交易所购买策略):
    def 求解(self, 商店: 信用交易所) -> list[bool]:
        当前信用 = 商店.剩余信用
        购买指标向量 = [False for _ in 商店.商品列表]
        for 商品序号, 商品 in 计算未购买的物品列表(商店):
            if 商品.现价 <= 当前信用:
                购买指标向量[商品序号] = True
                当前信用 -= 商品.现价
            else:
                break
        return 购买指标向量


class 按性价比购买_直到不能购买为止策略(信用交易所购买策略):
    def 求解(self, 商店: 信用交易所) -> list[bool]:
        当前信用 = 商店.剩余信用
        购买指标向量 = [False for _ in 商店.商品列表]
        for 商品序号, 商品 in sorted(计算未购买的物品列表(商店), key=lambda x: x[1].性价比, reverse=True):
            if 商品.现价 <= 当前信用:
                购买指标向量[商品序号] = True
                当前信用 -= 商品.现价
            else:
                break
        return 购买指标向量


class 按性价比购买_并设定性价比阈值策略(信用交易所购买策略):
    def __init__(self, 阈值: float | None = None, 每日获得的信用: int | None = None):
        if 阈值 is not None:
            self.阈值 = 阈值
        else:
            from 中间结果.K··· import K_N减1_·_·
            if 每日获得的信用 is None:
                raise TypeError('必须提供阈值或者每日获得的信用')
            self.阈值 = (K_N减1_·_·(每日获得的信用, 300) - K_N减1_·_·(每日获得的信用, 0)) / 300
        print(self.阈值)

    @staticmethod
    def 计算当前折算价格(当前信用: int, 商品: 信用交易所商品) -> float:
        return max(min(300 - (当前信用 - 商品.现价), 商品.现价), 0)

    @staticmethod
    def 计算当前折算性价比(当前信用: int, 商品: 信用交易所商品) -> float:
        当前折算价格 = 按性价比购买_并设定性价比阈值策略.计算当前折算价格(当前信用, 商品)
        return 商品.价值 / 当前折算价格 if 当前折算价格 > 0 else math.inf

    def 求解(self, 商店: 信用交易所) -> list[bool]:
        当前信用 = 商店.剩余信用
        购买指标向量 = [False for _ in 商店.商品列表]
        for 商品序号, 商品 in sorted(计算未购买的物品列表(商店), key=lambda x: x[1].性价比, reverse=True):
            if 商品.现价 <= 当前信用 and 商品.性价比 >= self.阈值:
                购买指标向量[商品序号] = True
                当前信用 -= 商品.现价
            else:
                break
        while True:
            当前折算性价比列表 = [
                self.计算当前折算性价比(当前信用, 商品)
                if not 购买指标向量[商品序号] and not 商品.已购买 and 商品.现价 <= 当前信用
                else -math.inf
                for 商品序号, 商品 in enumerate(商店.商品列表)
            ]
            最大折算性价比商品编号, 最大折算性价比 = max(enumerate(当前折算性价比列表), key=lambda x: x[1])
            if 最大折算性价比 >= self.阈值:
                购买指标向量[最大折算性价比商品编号] = True
                当前信用 -= 商店.商品列表[最大折算性价比商品编号].现价
            else:
                break
        return 购买指标向量


class 考虑天数为N时的最优策略(信用交易所购买策略):
    def __init__(self, 每日获得的信用: int, N: int | None = None):
        from 中间结果.K··· import K···
        from 中间结果.K··· import N as N_
        if N is None:
            N = N_
        self.KNC· = [K···(N - 1, 每日获得的信用, c) for c in range(301)]

    def 求解(self, 商店: 信用交易所) -> tuple[bool, ...]:
        当前信用 = 商店.剩余信用
        目标函数最大值: float = -math.inf
        for 购买指标向量 in product(*((False, True) if not 商品.已购买 else (False, ) for 商品 in 商店.商品列表)):
            总价格: float = 计算总价格(商店, 购买指标向量)
            总价值: float = 计算总价值(商店, 购买指标向量)
            剩余信用: float = 当前信用 - 总价格
            能够继承的信用: float = min(剩余信用, 300)
            if 总价格 <= 当前信用:
                目标函数: float = 总价值 + self.KNC·[能够继承的信用]
                if 目标函数 > 目标函数最大值:
                    目标函数最大值 = 目标函数
                    最优策略购买指标向量 = 购买指标向量
        return 最优策略购买指标向量


class 最优策略的近似策略(考虑天数为N时的最优策略):
    def __init__(self, 每日获得的信用: int):
        from 中间结果.信用能购买的商品碎片的价值 import 信用能购买的商品碎片的价值
        if 每日获得的信用 <= 150:
            raise ValueError('最优策略的近似策略要求每日获得的信用至少为 150')
        self.KNC· = [信用能购买的商品碎片的价值[c] for c in range(每日获得的信用 - 150, 每日获得的信用 + 151)]

    # 求解方法不变


def 模拟一轮购买(
    策略: 信用交易所购买策略,
    每日获取信用: int,
    初始继承信用: int = 0,
    商店列表: list[信用交易所] | None = None,
) -> float:
    if 商店列表 is None:
        商店列表 = [商店.设为全部未购买() for 商店 in 信用交易所统计字典.values()]
        random.shuffle(商店列表)

    当前信用 = 初始继承信用 + 每日获取信用
    总价值之和 = 0
    for 商店 in 商店列表:
        购买指标向量 = 策略.求解(信用交易所(当前信用, 商店.商品列表))
        当前信用 -= 计算总价格(商店, 购买指标向量)
        if 当前信用 < 0:
            raise ValueError('信用不足')
        总价值之和 += 计算总价值(商店, 购买指标向量)
        继承的信用 = min(当前信用, 300)
        当前信用 = 继承的信用 + 每日获取信用
    return 总价值之和 / len(商店列表)


def 比较策略的优劣(
    策略字典: dict[str, 信用交易所购买策略],
    每日获取信用: int,
    初始继承信用: int = 0,
    商店列表: list[信用交易所] | None = None,
) -> dict[str, float]:
    if 商店列表 is None:
        商店列表 = [商店.设为全部未购买() for 商店 in 信用交易所统计字典.values()]
        random.shuffle(商店列表)
    return {
        策略名: 模拟一轮购买(策略, 每日获取信用, 初始继承信用, 商店列表)
        for 策略名, 策略 in 策略字典.items()
    }


if __name__ == '__main__':
    每日获取信用 = 942
    初始继承信用 = 0
    策略字典 = {
        '啥都不买策略': 啥都不买策略(),
        '从左到右购买_直到不能购买为止策略': 从左到右购买_直到不能购买为止策略(),
        '按性价比购买_直到不能购买为止策略': 按性价比购买_直到不能购买为止策略(),
        '按性价比购买_并设定性价比阈值策略': 按性价比购买_并设定性价比阈值策略(每日获得的信用=每日获取信用),
        '考虑天数为N=11时的最优策略': 考虑天数为N时的最优策略(每日获得的信用=每日获取信用, N=11),
        '最优策略的近似策略': 最优策略的近似策略(每日获得的信用=每日获取信用),
    }
    策略优劣的结果 = 比较策略的优劣(策略字典, 每日获取信用, 初始继承信用)
    for 策略名, 期望值 in 策略优劣的结果.items():
        print(f'{策略名}: {期望值}')
