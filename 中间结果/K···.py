import json
from functools import lru_cache

from scipy.interpolate import interp1d

# obj: list[dict[str, list[float]]]
# """`K···[n][str(C)][c]` = $K_C^n(c)$"""

with open('中间结果/K···.json', 'r', encoding='utf-8') as f:
    obj = json.load(f)

N = len(obj)


@lru_cache(maxsize=None)
def get_Kn·c(n, c) -> interp1d:
    return interp1d(
        [int(C) for C in obj[n]],
        [obj[n][str(C)][c] for C in obj[n]],
        kind='cubic',
    )


def K···(n, C, c) -> float:
    return float(get_Kn·c(n, c)(C))


def K_N减1_·_·(C, c) -> float:
    return K···(N - 1, C, c)


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from matplotlib.font_manager import FontProperties
    prop = FontProperties(fname=r'C:\Users\Administrator\AppData\Local\Microsoft\Windows\Fonts\SourceHanSansSC-Regular.otf')
    plt.rcParams['font.family'] = prop.get_name()
    import numpy as np
    # x = np.arange(0, 301, 10)
    # y = np.arange(0, 1001, 50)
    # z = np.array([[K···(10, C, c) for c in x] for C in y])
    # plt.pcolormesh(x, y, z)
    # plt.colorbar()
    # plt.show()
    # print((K···(10, 813, 300) - K···(10, 813, 0)) / 300)
