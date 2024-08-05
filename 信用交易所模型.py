import math

from typing import NamedTuple
from 信用交易所商品信息 import 信用交易所商品价格, 信用交易所商品理智价值


class 信用交易所商品(NamedTuple):
    物品名称: str
    折扣: int
    已购买: bool

    @property
    def 现价(self) -> int:
        return math.floor(信用交易所商品价格[self.物品名称] * (1 - self.折扣 / 100))

    @property
    def 原价(self) -> int:
        return 信用交易所商品价格[self.物品名称]

    @property
    def 价值(self) -> float:
        return 信用交易所商品理智价值[self.物品名称]

    @property
    def 性价比(self) -> float:
        return self.价值 / self.现价

    def copy(self, **kwargs):
        return 信用交易所商品(**({
            '物品名称': self.物品名称,
            '折扣': self.折扣,
            '已购买': self.已购买,
        } | kwargs))


class 信用交易所(NamedTuple):
    剩余信用: int
    商品列表: list[信用交易所商品]

    def 打印为一行(self):
        print(*(商品.折扣 for 商品 in self.商品列表), *(商品.物品名称 for 商品 in self.商品列表))

    def 设为全部未购买(self):
        商品列表 = [商品.copy(已购买=False) for 商品 in self.商品列表]
        return 信用交易所(self.剩余信用, 商品列表)
