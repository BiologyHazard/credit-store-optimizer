# 注：代码为了可读性牺牲了性能，实际运行起来非常慢。
# 代码仓库 https://github.com/BiologyHazard/credit-store-optimizer 中有为性能优化后的代码。

import math
from collections.abc import Sequence
from itertools import product
from statistics import mean

from credit_store_models import CreditStore
from credit_store_stats import stats


def calculate_total_price(shop: CreditStore, buy_index_vector: Sequence[bool]) -> int:
    return sum(item.current_price for i, item in enumerate(shop.items) if buy_index_vector[i])


def calculate_total_value(shop: CreditStore, buy_index_vector: Sequence[bool]) -> float:
    return sum(item.value for i, item in enumerate(shop.items) if buy_index_vector[i])


def solve_single_shop(shop: CreditStore, current_credit: int, KnC·: list[float]) -> tuple[float, tuple[bool, ...]]:
    """Choose one of 2 ** 10 purchase methods that does not overspend, such that the total value of the items purchased  + KnC·[carriable_credit] is maximized"""
    target_function_max: float = -math.inf
    for buy_index_vector in product((False, True), repeat=len(shop.items)):  # enumerate 2 ** 10 purchase methods
        total_price: int = calculate_total_price(shop, buy_index_vector)
        total_value: float = calculate_total_value(shop, buy_index_vector)
        if total_price <= current_credit:
            credit_left: int = current_credit - total_price
            carriable_credit: int = min(credit_left, 300)
            target_function: float = total_value + KnC·[carriable_credit]
            if target_function > target_function_max:
                target_function_max = target_function
                best_buy_index_vector = buy_index_vector

    return target_function_max, best_buy_index_vector


if __name__ == '__main__':
    daily_credit_income_C = 813
    time_span_N = 11

    K0C·: list[float] = [0 for _ in range(301)]
    K·C·: list[list[float]] = [K0C·]

    for n in range(1, time_span_N):
        K_n_minus_1_C_·: list[float] = K·C·[-1]
        KnC·: list[float] = [0 for _ in range(301)]
        for carried_credit_c in range(301):
            samples_of_KnCc: list[float] = []
            for shop in stats:
                target_function_max, _ = solve_single_shop(shop, carried_credit_c + daily_credit_income_C, K_n_minus_1_C_·)
                samples_of_KnCc.append(target_function_max)
            KnC·[carried_credit_c] = mean(samples_of_KnCc)  # use mean as an estimate of expectation
        K·C·.append(KnC·)

    for n, KnC· in enumerate(K·C·):
        print(f'K_{n}_{daily_credit_income_C}_·: {KnC·}')
