import json
from functools import lru_cache

from scipy.interpolate import interp1d


with open('中间结果/K···.json', 'r', encoding='utf-8') as f:
    obj: list[dict[str, list[float]]] = json.load(f)

N: int = len(obj)


@lru_cache(maxsize=None)
def get_Kn·c(n, c) -> interp1d:
    x = [int(C) for C in obj[n]]
    y = [obj[n][str(C)][c] for C in obj[n]]
    return interp1d(x, y, kind='cubic')


def K···(n: int, C: float, c: int) -> float:
    """`K···(n, C, c)` = $K_C^n(c)$"""
    return float(get_Kn·c(n, c)(C))


def K_N减1_·_·(C: float, c: int) -> float:
    """`K_N减1_·_·(C, c)` = $K_C^{N-1}(c)$"""
    return K···(N - 1, C, c)
