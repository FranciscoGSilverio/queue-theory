from math import factorial
from typing import Any, Dict

from .pn_utils import build_pn_distribution


def mmsk(
    lmbda: float,
    mu: float,
    s: int,
    K: int,
    n: int | None = None,
    t: float | None = None,
    **kwargs,
) -> Dict[str, Any]:
    """
    Modelo M/M/s/K com capacidade total K.

    - Pn = (a^n / n!) P0 para n < s; Pn = (a^n / (s! * s^{n-s})) P0 para s <= n <= K, com a = lambda/mu.
    - P0 = 1 / [ sum_{n=0}^{s-1} a^n/n! + sum_{n=s}^{K} a^n/(s! s^{n-s}) ].
    - lambda_eff = lambda * (1 - P_K); L = sum n*Pn; ocupacao = sum min(n,s)*Pn; Lq = L - ocupacao;
      W = L/lambda_eff; Wq = Lq/lambda_eff.
    Parametros opcionais:
      - n: calcula Pn
      - t: aceito, mas nao utilizado
    """
    if lmbda < 0:
        raise ValueError("lambda (lmbda) deve ser >= 0")
    if mu <= 0:
        raise ValueError("mu deve ser > 0")
    if not isinstance(s, int) or s <= 0:
        raise ValueError("s deve ser inteiro >= 1")
    if not isinstance(K, int) or K < 0:
        raise ValueError("K deve ser inteiro >= 0")
    if K < s:
        raise ValueError("K deve ser >= s")

    if lmbda == 0:
        def pn_func_zero(n_val: int) -> float:
            if n_val < 0 or int(n_val) != n_val:
                raise ValueError(f"n deve ser inteiro entre 0 e {K}")
            if n_val > K:
                return 0.0
            return 1.0 if n_val == 0 else 0.0

        result: Dict[str, Any] = {
            "rho": 0.0,
            "p0": 1.0,
            "L": 0.0,
            "Lq": 0.0,
            "W": 0.0,
            "Wq": 0.0,
            "lambda_eff": 0.0,
        }
        if n is not None:
            result["pn"] = pn_func_zero(n)
            result["pn_distribution"] = build_pn_distribution(n, pn_func_zero, max_state=K)
        return result

    rho = lmbda / (s * mu)
    a = lmbda / mu

    sum_first = sum(a**n_state / factorial(n_state) for n_state in range(s))
    sum_tail = sum(
        (a**n_state) / (factorial(s) * (s ** (n_state - s)))
        for n_state in range(s, K + 1)
    )
    p0 = 1.0 / (sum_first + sum_tail)

    def pn_func(n_val: int) -> float:
        if n_val < 0 or int(n_val) != n_val:
            raise ValueError(f"n deve ser inteiro entre 0 e {K}")
        if n_val > K:
            return 0.0
        if n_val <= s:
            return (a**n_val / factorial(n_val)) * p0
        return (a**n_val / (factorial(s) * (s ** (n_val - s)))) * p0

    pn_values = [pn_func(nv) for nv in range(K + 1)]

    pK = pn_values[K]
    lambda_eff = lmbda * (1 - pK)

    L = sum(nv * pn_values[nv] for nv in range(K + 1))
    busy_servers = sum(min(nv, s) * pn_values[nv] for nv in range(K + 1))
    Lq = L - busy_servers
    if Lq < 0:
        Lq = 0.0  # protecao numerica

    W = L / lambda_eff if lambda_eff > 0 else 0.0
    Wq = Lq / lambda_eff if lambda_eff > 0 else 0.0

    result: Dict[str, Any] = {
        "rho": rho,
        "p0": p0,
        "L": L,
        "Lq": Lq,
        "W": W,
        "Wq": Wq,
        "lambda_eff": lambda_eff,
        "pK": pK,
    }

    if n is not None:
        result["pn"] = pn_func(n)
        result["pn_distribution"] = build_pn_distribution(n, pn_func, max_state=K)

    return result
