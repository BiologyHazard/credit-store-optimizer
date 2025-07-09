import json
import math
import multiprocessing
import random
from abc import ABC, abstractmethod
from collections.abc import Container, Sequence
from itertools import product

from 中间结果.K_x_x_x import N, K_N减1_x_x
from 信用交易所模型 import 信用交易所, 信用交易所商品
from 统计结果 import 信用交易所统计结果


def 计算未购买的商品列表(商店: 信用交易所, 购买指标向量: Sequence[bool] | None = None) -> list[tuple[int, 信用交易所商品]]:
    if 购买指标向量 is None:
        购买指标向量 = [False for _ in 商店.商品列表]
    return [(商品序号, 商品) for 商品序号, 商品 in enumerate(商店.商品列表) if not 商品.已购买 and not 购买指标向量[商品序号]]


def 计算总价格(商店: 信用交易所, 购买指标向量: Sequence[bool]) -> int:
    return sum(商品.现价 for i, 商品 in enumerate(商店.商品列表) if 购买指标向量[i])


def 计算总价值(商店: 信用交易所, 购买指标向量: Sequence[bool]) -> float:
    return sum(商品.价值 for i, 商品 in enumerate(商店.商品列表) if 购买指标向量[i])


# def 还原购买指标向量(购买方案序号: int) -> tuple[bool, ...]:
#     # 最高位为首个商品，最低位为最后一个商品
#     return tuple(bool((购买方案序号 >> i) & 1) for i in reversed(range(10)))


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


class 随机购买策略(信用交易所购买策略):
    def __init__(self, 信用小于等于300时停止购买: bool = False):
        self.信用小于等于300时停止购买: bool = 信用小于等于300时停止购买

    def 求解(self, 商店: 信用交易所) -> list[bool]:
        seed = f'{商店.剩余信用}_{商店.商品列表}'
        random_instance = random.Random(seed)
        当前信用 = 商店.剩余信用
        购买指标向量 = [False for _ in 商店.商品列表]
        未购买的商品列表 = 计算未购买的商品列表(商店)
        random_instance.shuffle(未购买的商品列表)
        while 未购买的商品列表:
            商品序号, 商品 = 未购买的商品列表.pop()
            if 商品.现价 <= 当前信用 and not (self.信用小于等于300时停止购买 and 当前信用 <= 300):
                购买指标向量[商品序号] = True
                当前信用 -= 商品.现价
            else:
                break
        return 购买指标向量


class 从左到右购买策略(信用交易所购买策略):
    def __init__(self, 信用小于等于300时停止购买: bool = False):
        self.信用小于等于300时停止购买: bool = 信用小于等于300时停止购买

    def 求解(self, 商店: 信用交易所) -> list[bool]:
        当前信用 = 商店.剩余信用
        购买指标向量 = [False for _ in 商店.商品列表]
        for 商品序号, 商品 in 计算未购买的商品列表(商店):
            if 商品.现价 <= 当前信用 and not (self.信用小于等于300时停止购买 and 当前信用 <= 300):
                购买指标向量[商品序号] = True
                当前信用 -= 商品.现价
            else:
                break
        return 购买指标向量


class 从左到右购买_设定黑白名单策略(信用交易所购买策略):
    def __init__(self,
                 黑名单: Container[str] | None = None,
                 白名单: Container[str] | None = None,
                 信用溢出时无视黑名单: bool = False,
                 信用小于等于300时停止购买: bool = False):
        if 黑名单 is None:
            黑名单 = set()
        if 白名单 is None:
            白名单 = set()
        self.黑名单: Container[str] = 黑名单
        self.白名单: Container[str] = 白名单
        self.信用溢出时无视黑名单: bool = 信用溢出时无视黑名单
        self.信用小于等于300时停止购买: bool = 信用小于等于300时停止购买

    def 求解(self, 商店: 信用交易所) -> list[bool]:
        当前信用 = 商店.剩余信用
        购买指标向量 = [False for _ in 商店.商品列表]
        # 先购买白名单中的商品
        for 商品序号, 商品 in 计算未购买的商品列表(商店):
            if 商品.商品名称 in self.白名单 and 商品.现价 <= 当前信用 and not (self.信用小于等于300时停止购买 and 当前信用 <= 300):
                购买指标向量[商品序号] = True
                当前信用 -= 商品.现价
        # 再购买不在黑名单中的商品
        for 商品序号, 商品 in 计算未购买的商品列表(商店, 购买指标向量):
            if 商品.商品名称 in self.黑名单:
                continue
            if 商品.现价 <= 当前信用 and not (self.信用小于等于300时停止购买 and 当前信用 <= 300):
                购买指标向量[商品序号] = True
                当前信用 -= 商品.现价
            else:
                break
        # 信用溢出时无视黑名单继续购买
        if self.信用溢出时无视黑名单:
            for 商品序号, 商品 in 计算未购买的商品列表(商店, 购买指标向量):
                if 当前信用 <= 300:
                    break
                if 商品.现价 <= 当前信用 and not (self.信用小于等于300时停止购买 and 当前信用 <= 300):
                    购买指标向量[商品序号] = True
                    当前信用 -= 商品.现价
        return 购买指标向量


class 按性价比从高到低购买策略(信用交易所购买策略):
    def __init__(self, 信用小于等于300时停止购买: bool = False):
        self.信用小于等于300时停止购买: bool = 信用小于等于300时停止购买

    def 求解(self, 商店: 信用交易所) -> list[bool]:
        当前信用 = 商店.剩余信用
        购买指标向量 = [False for _ in 商店.商品列表]
        for 商品序号, 商品 in sorted(计算未购买的商品列表(商店), key=lambda x: x[1].性价比, reverse=True):
            if 商品.现价 <= 当前信用 and not (self.信用小于等于300时停止购买 and 当前信用 <= 300):
                购买指标向量[商品序号] = True
                当前信用 -= 商品.现价
            else:
                break
        return 购买指标向量


class 考虑天数为N时的信用交易所最优购买策略(信用交易所购买策略):
    def __init__(self,
                 每日获得的信用: int,
                 K_N减1_C_x: Sequence[float] | None = None):
        if K_N减1_C_x is None:
            K_N减1_C_x = [K_N减1_x_x(每日获得的信用, c) for c in range(301)]
        self.K_N减1_C_x: Sequence[float] = K_N减1_C_x

    def 求解(self, 商店: 信用交易所) -> tuple[bool, ...]:
        """在所有购买方案中选一种不超支的，使得 购买的物品总价值 + K_N-1_C_x[能够继承的信用] 最大"""
        当前信用: int = 商店.剩余信用
        目标函数最大值: float = -math.inf
        最优策略购买指标向量: tuple[bool, ...] = tuple(False for _ in 商店.商品列表)
        for 购买指标向量 in product(*((False, True) if not 商品.已购买 else (False, ) for 商品 in 商店.商品列表)):
            总价格: float = 计算总价格(商店, 购买指标向量)
            总价值: float = 计算总价值(商店, 购买指标向量)
            剩余信用: float = 当前信用 - 总价格
            能够继承的信用: float = min(剩余信用, 300)
            if 总价格 <= 当前信用:
                目标函数: float = 总价值 + self.K_N减1_C_x[能够继承的信用]
                if 目标函数 > 目标函数最大值:
                    目标函数最大值 = 目标函数
                    最优策略购买指标向量 = 购买指标向量
        return 最优策略购买指标向量

    def 快速求解(self, 价格行, 价值行, 当前信用) -> tuple[int, float]:
        目标函数最大值: float = -math.inf
        最优策略总价格: int = 0
        最优策略总价值: float = 0
        for 总价格, 总价值 in zip(价格行, 价值行):
            if 总价格 <= 当前信用:
                剩余信用 = 当前信用 - 总价格
                能够继承的信用 = min(剩余信用, 300)
                目标函数 = 总价值 + self.K_N减1_C_x[能够继承的信用]
                if 目标函数 > 目标函数最大值:
                    目标函数最大值 = 目标函数
                    最优策略总价格 = 总价格
                    最优策略总价值 = 总价值
        return 最优策略总价格, 最优策略总价值


class 最优购买策略的近似策略(考虑天数为N时的信用交易所最优购买策略):
    def __init__(self, 每日获得的信用: int):
        from 中间结果.信用能购买的商品碎片的价值 import 信用能购买的商品碎片的价值
        if 每日获得的信用 < 150:
            # 每日获得的信用小于 150 时，取信用能购买的商品碎片的价值[0 <= c <= 300] 作为近似值
            self.K_N减1_C_x = 信用能购买的商品碎片的价值(range(301))
        else:
            # 每日获得的信用大于等于 时，取信用能购买的商品碎片的价值[C - 150 <= c <= C + 150] 作为近似值
            self.K_N减1_C_x = 信用能购买的商品碎片的价值(range(每日获得的信用 - 150, 每日获得的信用 + 151))

    # 求解方法不变


class 按性价比从高到低购买_并设定性价比阈值策略(信用交易所购买策略):
    def __init__(self, 阈值: float | None = None, 每日获得的信用: int | None = None):
        if 阈值 is not None:
            self.阈值 = 阈值
        else:
            # from 中间结果.K_x_x_x import K_N减1_x_x
            from 中间结果.信用能购买的商品碎片的价值 import 信用能购买的商品碎片的价值的导数
            if 每日获得的信用 is None:
                raise TypeError('必须提供阈值或者每日获得的信用')
            # self.阈值 = (K_N减1_x_x(每日获得的信用, 300) - K_N减1_x_x(每日获得的信用, 0)) / 300
            self.阈值 = 信用能购买的商品碎片的价值的导数(每日获得的信用)

    @staticmethod
    def 计算当前折算价格(当前信用: int, 商品: 信用交易所商品) -> float:
        return max(min(300 - (当前信用 - 商品.现价), 商品.现价), 0)

    @staticmethod
    def 计算当前折算性价比(当前信用: int, 商品: 信用交易所商品) -> float:
        当前折算价格 = 按性价比从高到低购买_并设定性价比阈值策略.计算当前折算价格(当前信用, 商品)
        return 商品.价值 / 当前折算价格 if 当前折算价格 > 0 else math.inf

    def 求解(self, 商店: 信用交易所) -> list[bool]:
        当前信用 = 商店.剩余信用
        购买指标向量 = [False for _ in 商店.商品列表]
        for 商品序号, 商品 in sorted(计算未购买的商品列表(商店), key=lambda x: x[1].性价比, reverse=True):
            if 商品.现价 <= 当前信用 and self.计算当前折算性价比(当前信用, 商品) >= self.阈值:
                购买指标向量[商品序号] = True
                当前信用 -= 商品.现价
            else:
                break
        return 购买指标向量


def 模拟一轮购买(
    策略: 信用交易所购买策略,
    每日获得的信用: int,
    初始继承信用: int,
    商店列表: list[信用交易所],
    顺序: list[int] | None = None,  # 用于快速求解
) -> float:
    当前信用 = 初始继承信用 + 每日获得的信用
    已购买总价值 = 0
    if isinstance(策略, 考虑天数为N时的信用交易所最优购买策略) and 顺序 is not None:
        # 快速求解
        from 中间结果.价格价值矩阵 import 价格矩阵, 价值矩阵
        for 商店序号 in 顺序:
            价格行 = 价格矩阵[商店序号]
            价值行 = 价值矩阵[商店序号]
            总价格, 总价值 = 策略.快速求解(价格行, 价值行, 当前信用)
            当前信用 -= 总价格
            if 当前信用 < 0:
                raise ValueError('信用不足')
            已购买总价值 += 总价值
            继承的信用 = min(当前信用, 300)
            当前信用 = 继承的信用 + 每日获得的信用
    else:
        # 普通求解
        for 商店 in 商店列表:
            购买指标向量 = 策略.求解(信用交易所(当前信用, 商店.商品列表))
            当前信用 -= 计算总价格(商店, 购买指标向量)
            if 当前信用 < 0:
                raise ValueError('信用不足')
            已购买总价值 += 计算总价值(商店, 购买指标向量)
            继承的信用 = min(当前信用, 300)
            当前信用 = 继承的信用 + 每日获得的信用
    return 已购买总价值 / len(商店列表)


def 比较策略的优劣(
    策略字典: dict[str, 信用交易所购买策略],
    每日获得的信用: int,
    初始继承信用: int,
    商店列表: list[信用交易所],
    顺序: list[int],
) -> dict[str, float]:
    print(f"正在计算 {每日获得的信用}")
    return {
        策略名称: 模拟一轮购买(策略, 每日获得的信用, 初始继承信用, 商店列表, 顺序)
        for 策略名称, 策略 in 策略字典.items()
    }


def 策略字典(每日获得的信用: int):
    黑名单 = ['加急许可×1', '家具零件×20', '家具零件×25', '碳×5', '碳素×3']
    白名单 = ['招聘许可×1', '龙门币×1800', '龙门币×3600', '技巧概要·卷2×3']
    return {
        '啥都不买策略': 啥都不买策略(),
        '随机购买，直到不能购买为止策略': 随机购买策略(信用小于等于300时停止购买=False),
        '随机购买，直到信用小于等于 300 策略': 随机购买策略(信用小于等于300时停止购买=True),
        '从左到右购买，直到不能购买为止策略': 从左到右购买策略(信用小于等于300时停止购买=False),
        '从左到右购买，直到信用小于等于 300 策略': 从左到右购买策略(信用小于等于300时停止购买=True),
        '从左到右购买，设定黑白名单，信用溢出时停止购买策略\n优先购买：招聘许可、龙门币、技巧概要·卷2\n黑名单：加急许可、家具零件、碳、碳素':
        从左到右购买_设定黑白名单策略(
            黑名单=黑名单,
            白名单=白名单,
            信用溢出时无视黑名单=False,
            信用小于等于300时停止购买=False,
        ),
        '从左到右购买，设定黑白名单，信用溢出时无视黑名单策略\n优先购买：招聘许可、龙门币、技巧概要·卷2\n黑名单：加急许可、家具零件、碳、碳素':
        从左到右购买_设定黑白名单策略(
            黑名单=黑名单,
            白名单=白名单,
            信用溢出时无视黑名单=True,
            信用小于等于300时停止购买=False,
        ),
        '按性价比从高到低购买，直到不能购买为止策略': 按性价比从高到低购买策略(信用小于等于300时停止购买=False),
        '按性价比从高到低购买，直到信用小于等于 300 策略': 按性价比从高到低购买策略(信用小于等于300时停止购买=True),
        f'考虑天数为 N = {N} 时的信用交易所最优购买策略': 考虑天数为N时的信用交易所最优购买策略(每日获得的信用=每日获得的信用),
        '最优购买策略的近似策略': 最优购买策略的近似策略(每日获得的信用=每日获得的信用),
        '按性价比从高到低购买，并设定性价比阈值策略': 按性价比从高到低购买_并设定性价比阈值策略(每日获得的信用=每日获得的信用),
    }


if __name__ == '__main__':
    # 商店 = 信用交易所(700+75, [
    #     信用交易所商品('破损装置×2', 75, False),
    #     信用交易所商品('赤金×6', 75, False),
    #     信用交易所商品('糖×2', 50, False),
    #     信用交易所商品('源岩×2', 50, False),
    #     信用交易所商品('酮凝集×2', 50, False),
    #     信用交易所商品('糖×2', 0, False),
    #     信用交易所商品('龙门币×3600', 0, False),
    #     信用交易所商品('初级作战记录×9', 0, False),
    #     信用交易所商品('初级作战记录×9', 0, False),
    #     信用交易所商品('招聘许可×1', 0, False),
    # ])
    # print(考虑天数为N时的信用交易所最优购买策略(700).求解(商店))
    # exit(0)

    # 商店 = 信用交易所(813+200, [
    #     信用交易所商品('家具零件×20', 75, False),
    #     信用交易所商品('', 75, False),
    #     信用交易所商品('', 50, False),
    #     信用交易所商品('赤金×6', 50, False),
    #     信用交易所商品('聚酸酯×2', 50, False),
    #     信用交易所商品('糖×2', 0, False),
    #     信用交易所商品('龙门币×3600', 0, False),
    #     信用交易所商品('', 0, False),
    #     信用交易所商品('初级作战记录×9', 0, False),
    #     信用交易所商品('加急许可×1', 0, False),
    # ])
    # print(考虑天数为N时的信用交易所最优购买策略(813).求解(商店))
    # exit(0)

    每日获得的信用列表 = range(0, 1001, 4)
    初始继承信用 = 0

    random.seed(0)
    顺序: list[int] = list(range(len(信用交易所统计结果))) * 10
    random.shuffle(顺序)
    商店列表: list[信用交易所] = [信用交易所统计结果[商店序号].设为全部未购买() for 商店序号 in 顺序]

    with multiprocessing.Pool() as pool:
        结果: list[dict[str, float]] = pool.starmap(
            比较策略的优劣,
            ((策略字典(每日获得的信用), 每日获得的信用, 初始继承信用, 商店列表, 顺序)
             for 每日获得的信用 in 每日获得的信用列表),
        )

    不同购买策略的比较: dict[str, dict[str, float]] = {
        策略名称: {
            str(每日获得的信用): 结果[i][策略名称]
            for i, 每日获得的信用 in enumerate(每日获得的信用列表)
        }
        for 策略名称 in next(iter(结果))
    }

    with open("中间结果/不同购买策略的比较.json", 'w', encoding='utf-8') as f:
        json.dump(不同购买策略的比较, f, ensure_ascii=False, indent=4)
