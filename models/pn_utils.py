from typing import Callable, Dict


def build_pn_distribution(
    n: int, pn_func: Callable[[int], float], max_state: int | None = None
) -> Dict[str, float]:
    """
    Constroi um dicionario ordenado com P(0)...P(n) e o complemento P(>n).
    """
    limit = n if max_state is None else min(n, max_state)

    distribution: Dict[str, float] = {}
    for state in range(limit + 1):
        distribution[str(state)] = pn_func(state)

    if max_state is None:
        tail = 1.0 - sum(distribution.values())
    elif n < max_state:
        tail = sum(pn_func(state) for state in range(limit + 1, max_state + 1))
    else:
        tail = 0.0

    tail = max(0.0, min(1.0, tail))
    distribution[f">{n}"] = tail

    return distribution
