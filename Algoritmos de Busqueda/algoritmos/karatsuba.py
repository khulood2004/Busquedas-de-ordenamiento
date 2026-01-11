# algoritmos/karatsuba.py
import time
from typing import Tuple


def _time_it(func):
    def wrapper(*args, **kwargs) -> Tuple[int, float]:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        return result, (end - start) * 1000
    return wrapper


# ---------------- KARATSUBA RECURSIVO ----------------
def _karatsuba_rec(x: int, y: int) -> int:
    if x < 10 or y < 10:
        return x * y

    n = max(len(str(x)), len(str(y)))
    m = n // 2

    high_x, low_x = divmod(x, 10 ** m)
    high_y, low_y = divmod(y, 10 ** m)

    z0 = _karatsuba_rec(low_x, low_y)
    z1 = _karatsuba_rec(low_x + high_x, low_y + high_y)
    z2 = _karatsuba_rec(high_x, high_y)

    return (z2 * 10 ** (2 * m)) + ((z1 - z2 - z0) * 10 ** m) + z0


@_time_it
def karatsuba_recursive(x: int, y: int) -> int:
    return _karatsuba_rec(x, y)


# ---------------- KARATSUBA ITERATIVO ----------------
@_time_it
def karatsuba_iterative(x: int, y: int) -> int:
    stack = [(x, y, False)]
    results = {}

    while stack:
        a, b, processed = stack.pop()

        if a < 10 or b < 10:
            results[(a, b)] = a * b
            continue

        n = max(len(str(a)), len(str(b)))
        m = n // 2

        high_a, low_a = divmod(a, 10 ** m)
        high_b, low_b = divmod(b, 10 ** m)

        if not processed:
            stack.append((a, b, True))
            stack.append((low_a, low_b, False))
            stack.append((low_a + high_a, low_b + high_b, False))
            stack.append((high_a, high_b, False))
        else:
            z0 = results[(low_a, low_b)]
            z1 = results[(low_a + high_a, low_b + high_b)]
            z2 = results[(high_a, high_b)]

            results[(a, b)] = (
                (z2 * 10 ** (2 * m)) +
                ((z1 - z2 - z0) * 10 ** m) +
                z0
            )

    return results[(x, y)]
