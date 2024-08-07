from functools import lru_cache
import multiprocessing
import logging

import numpy as np
from scipy.interpolate import interp1d

from 中间结果.价格价值矩阵 import 价值矩阵, 价格矩阵


logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(module)s:%(funcName)s:%(lineno)d | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG,
)
logger = logging.getLogger(__name__)


@lru_cache(maxsize=None)
def _get_LnDc·(LnDc·) -> interp1d:
    return interp1d(range(12), LnDc·, kind='cubic')


def LnDc·(LnDc·, e) -> float:
    return float(_get_LnDc·(tuple(LnDc·))(e))


def 进程(进程序号, 价格行, 价值行, LnD··, 当前信用矩阵, 当前线索折算信用矩阵):
    logger.debug(f'{进程序号} 进程开始')
    总价格矩阵 = 价格行[:, None, None]
    总价值矩阵 = 价值行[:, None, None]
    # 先传递溢出的线索
    传递获得的信用数量 = np.ceil(np.maximum(当前线索折算信用矩阵 - 11 * 20, 0)).astype(int)
    当前信用矩阵 = 当前信用矩阵 + 传递获得的信用数量
    当前线索折算信用矩阵 = 当前线索折算信用矩阵 - 传递获得的信用数量
    最多可使用的信用矩阵 = 当前信用矩阵 + 当前线索折算信用矩阵
    剩余信用矩阵 = 当前信用矩阵 - 总价格矩阵
    # 补足不足的信用
    能够继承的线索矩阵 = np.where(剩余信用矩阵 < 0, 当前线索折算信用矩阵 + 剩余信用矩阵, 当前线索折算信用矩阵)
    能够继承的线索矩阵 = np.maximum(能够继承的线索矩阵, 0)
    剩余信用矩阵 = np.maximum(剩余信用矩阵, 0)
    能够继承的信用矩阵 = np.minimum(剩余信用矩阵, 300)
    目标函数矩阵 = np.where(
        总价格矩阵 <= 最多可使用的信用矩阵,
        总价值矩阵 + LnD··[能够继承的信用矩阵, 能够继承的线索矩阵],
        -np.inf
    )
    目标函数最大值矩阵 = np.amax(目标函数矩阵, axis=0)
    logger.debug(f'{进程序号} 进程结束')
    return 目标函数最大值矩阵


if __name__ == '__main__':
    每日获得的信用D = 738  # = round(813.32 - 20 * 3.783)
    每日获得的线索E折算信用 = 76  # = round(3.783 * 20)
    考虑的天数N = 2

    L0D·· = np.zeros((301, 11 * 20 + 1))
    L·D·· = np.zeros((考虑的天数N, 301, 11 * 20 + 1))
    L·D··[0] = L0D··

    继承信用矩阵 = np.arange(301)[None, :, None]
    当前信用矩阵 = 继承信用矩阵 + 每日获得的信用D
    继承线索折算信用矩阵 = np.arange(11 * 20 + 1)[None, None, :]
    当前线索折算信用矩阵 = 继承线索折算信用矩阵 + 每日获得的线索E折算信用

    for n in range(1, 考虑的天数N):
        L_n减1_D_·_· = L·D··[n - 1]

        # 目标函数最大值矩阵列表 = []
        # for 价格行, 价值行 in zip(价格矩阵[:1], 价值矩阵[:1]):
        #     LnD··的采样 = 进程(0, 价格行, 价值行, L_n减1_D_·_·, 当前信用矩阵, 当前线索折算信用矩阵)
        #     目标函数最大值矩阵列表.append(LnD··的采样)
        # 用多进程
        with multiprocessing.Pool() as pool:
            目标函数最大值矩阵列表 = pool.starmap(
                进程,
                ((进程序号, 价格行, 价值行, L_n减1_D_·_·, 当前信用矩阵, 当前线索折算信用矩阵)
                 for 进程序号, (价格行, 价值行) in enumerate(zip(价格矩阵, 价值矩阵)))
            )

        L·D··[n] = np.mean(目标函数最大值矩阵列表, axis=0)

    for n, LnD·· in enumerate(L·D··):
        print(f'L_{n}_{每日获得的信用D}_·: {LnD··}')
