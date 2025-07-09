import json
import logging
import multiprocessing

import numpy as np

from 中间结果.价格价值矩阵 import 价值矩阵, 价格矩阵


logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(module)s:%(funcName)s:%(lineno)d | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG,
)
logger = logging.getLogger(__name__)


def 进程(n, 商店序号, 价格行, 价值行, K_n_x_x, 当前信用矩阵):
    logger.debug(f'正在计算 K_{n}_x_x | {商店序号} 进程开始')
    每日获得的信用列表长度 = K_n_x_x.shape[0]
    总价格矩阵 = 价格行[:, None, None]
    # shape = (2 ** 10, 1, 1)
    总价值矩阵 = 价值行[:, None, None]
    # shape = (2 ** 10, 1, 1)
    剩余信用矩阵 = np.maximum(np.minimum(当前信用矩阵 - 总价格矩阵, 300), 0)
    # shape = (2 ** 10, 每日获得的信用列表长度, 301)

    目标函数矩阵 = np.where(
        总价格矩阵 <= 当前信用矩阵,
        总价值矩阵 + K_n_x_x[np.arange(每日获得的信用列表长度)[None, :, None], 剩余信用矩阵],
        0
    )
    # shape = (2 ** 10, 每日获得的信用列表长度, 301)
    目标函数最大值矩阵 = np.amax(目标函数矩阵, axis=0)
    # shape = (每日获得的信用列表长度, 301)
    logger.debug(f'正在计算 K_{n}_x_x | {商店序号} 进程结束')
    return 目标函数最大值矩阵


def 多进程迭代计算K_x_x_x(考虑的天数N, 每日获得的信用列表):
    每日获得的信用列表长度 = len(每日获得的信用列表)
    每日获得的信用矩阵 = np.array(每日获得的信用列表, dtype=int)[None, :, None]
    # shape = (1, 每日获得的信用列表长度, 1)
    继承信用矩阵 = np.arange(301)[None, None, :]
    # shape = (1, 1, 301)
    当前信用矩阵 = 继承信用矩阵 + 每日获得的信用矩阵
    # shape = (1, 每日获得的信用列表长度, 301)

    K_0_x_x = np.zeros((每日获得的信用列表长度, 301))
    K_x_x_x = np.empty((考虑的天数N, 每日获得的信用列表长度, 301))
    K_x_x_x[0] = K_0_x_x

    for n in range(1, 考虑的天数N):
        logger.info(f'开始计算 K_{n}_x_x')
        K_n减1_x_x = K_x_x_x[n - 1]
        with multiprocessing.Pool() as pool:
            目标函数最大值矩阵列表 = pool.starmap(
                进程,
                ((n, 商店序号, 价格行, 价值行, K_n减1_x_x, 当前信用矩阵)
                 for 商店序号, (价格行, 价值行) in enumerate(zip(价格矩阵, 价值矩阵)))
            )
        K_n_x_x = np.average(目标函数最大值矩阵列表, axis=0)
        K_x_x_x[n] = K_n_x_x
        with open(f'中间结果/K_{n}_x_x.json', 'w') as f:
            obj = {str(每日获得的信用): K_n_x_x[i, :].tolist() for i, 每日获得的信用 in enumerate(每日获得的信用列表)}
            json.dump(obj, f, separators=(',', ':'))
    return K_x_x_x


if __name__ == '__main__':
    考虑的天数N = 17
    每日获得的信用列表 = list(range(2, 1001, 4))

    with open('中间结果/K_x_x_x.json', 'r', encoding="utf-8") as f:
        old_K_x_x_x = json.load(f)

    K_x_x_x = 多进程迭代计算K_x_x_x(考虑的天数N, 每日获得的信用列表)

    obj = [{} for _ in range(考虑的天数N)]
    for n in range(考虑的天数N):
        for i, 每日获得的信用 in enumerate(每日获得的信用列表):
            obj[n][str(每日获得的信用)] = K_x_x_x[n, i, :].tolist()  # json 的 key 只能是字符串
        for 每日获得的信用, K_n_C_x in old_K_x_x_x[n].items():
            if int(每日获得的信用) not in obj[n]:
                obj[n][每日获得的信用] = K_n_C_x
        obj[n] = {k: v for k, v in sorted(obj[n].items(), key=lambda item: int(item[0]))}
    with open('中间结果/K_x_x_x.json', 'w', encoding="utf-8") as f:
        json.dump(obj, f, separators=(',', ':'))
