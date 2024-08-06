from itertools import product

import numpy as np

from 统计结果 import 信用交易所统计结果


def 计算价格价值矩阵():
    """
    `价格矩阵[i][j]` 表示下标为 `i` 的商店购买商品组合 `j` 的总价格
    `价值矩阵[i][j]` 表示下标为 `i` 的商店购买商品组合 `j` 的总价值
    其中 `j` 为 10 位二进制数，每一位表示是否购买对应商品

    提前计算价格价值矩阵，后面计算 `K` 的时候可以直接查表
    """
    价格矩阵 = np.zeros((len(信用交易所统计结果), 2 ** 10), dtype=np.int16)
    价值矩阵 = np.zeros((len(信用交易所统计结果), 2 ** 10), dtype=np.float64)
    for 商店序号, 商店 in enumerate(信用交易所统计结果):
        assert len(商店.商品列表) == 10
        for 购买方案序号, 购买指标向量 in enumerate(product((False, True), repeat=10)):
            总价格: int = sum(商品.现价 for i, 商品 in enumerate(商店.商品列表) if 购买指标向量[i])
            总价值: float = sum(商品.价值 for i, 商品 in enumerate(商店.商品列表) if 购买指标向量[i])
            价格矩阵[商店序号, 购买方案序号] = 总价格
            价值矩阵[商店序号, 购买方案序号] = 总价值
    return 价格矩阵, 价值矩阵


if __name__ == '__main__':
    # 计算价格价值矩阵，使用 gzip 压缩并保存
    价格矩阵, 价值矩阵 = 计算价格价值矩阵()
    np.savez_compressed('中间结果/价值价格矩阵', 价值矩阵=价值矩阵, 价格矩阵=价格矩阵)
