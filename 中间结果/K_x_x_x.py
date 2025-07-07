import json
from functools import lru_cache

from scipy.interpolate import interp1d


with open('中间结果/K_x_x_x.json', 'r', encoding='utf-8') as f:
    obj: list[dict[str, list[float]]] = json.load(f)

N: int = len(obj)


@lru_cache(maxsize=None)
def get_K_n_x_c(n, c) -> interp1d:
    x = [int(C) for C in obj[n]]
    y = [obj[n][str(C)][c] for C in obj[n]]
    return interp1d(x, y, kind='cubic')


def K_x_x_x(n: int, C: float, c: int) -> float:
    """`K_x_x_x(n, C, c)` = $K_C^n(c)$"""
    return float(get_K_n_x_c(n, c)(C))


def K_N减1_x_x(C: float, c: int) -> float:
    """`K_N减1_x_x(C, c)` = $K_C^{N-1}(c)$"""
    return K_x_x_x(N - 1, C, c)
