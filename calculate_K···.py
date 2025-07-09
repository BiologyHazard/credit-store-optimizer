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


def solve_single_shop(shop: CreditStore, current_credit: int, K_n_C_x: list[float]) -> tuple[float, tuple[bool, ...]]:
    """Choose one of 2 ** 10 purchase methods that does not overspend, such that the total value of the items purchased  + K_n_C_x[carriable_credit] is maximized"""

    target_function_max: float = -math.inf
    best_buy_index_vector: tuple[bool, ...] = tuple(False for _ in shop.items)

    # enumerate 2 ** 10 purchase methods
    for buy_index_vector in product((False, True), repeat=len(shop.items)):
        total_price: int = calculate_total_price(shop, buy_index_vector)
        total_value: float = calculate_total_value(shop, buy_index_vector)
        if total_price <= current_credit:  # does not overspend
            credit_left: int = current_credit - total_price
            carriable_credit: int = min(credit_left, 300)
            target_function: float = total_value + K_n_C_x[carriable_credit]
            if target_function > target_function_max:
                target_function_max = target_function
                best_buy_index_vector = buy_index_vector

    return target_function_max, best_buy_index_vector


if __name__ == '__main__':
    daily_credit_income_C = 813
    time_span_N = 11

    K_0_C_x: list[float] = [0 for _ in range(301)]
    K_x_C_x: list[list[float]] = [K_0_C_x]

    for n in range(1, time_span_N):
        K_n_minus_1_C_x: list[float] = K_x_C_x[-1]
        K_n_C_x: list[float] = [0 for _ in range(301)]
        for carried_credit_c in range(301):
            samples_of_K_n_C_c: list[float] = []
            for shop in stats:
                target_function_max, _ = solve_single_shop(shop, carried_credit_c + daily_credit_income_C, K_n_minus_1_C_x)
                samples_of_K_n_C_c.append(target_function_max)
            K_n_C_x[carried_credit_c] = mean(samples_of_K_n_C_c)  # use mean as an estimate of expectation
        K_x_C_x.append(K_n_C_x)

    for n, K_n_C_x in enumerate(K_x_C_x):
        print(f'K_{n}_{daily_credit_income_C}_x: {K_n_C_x}')
