from typing import Any, Dict, List

from .pn_utils import build_pn_distribution


def mmsn(
    lmbda: float,
    mu: float,
    s: int,
    N: int,
    n: int | None = None,
    t: float | None = None,
    **kwargs,
) -> Dict[str, Any]:
    """
    Modelo M/M/s/N (populacao finita com s servidores).

    - Processo nascimento-morte com lambda_n = (N - n) * lambda e mu_n = min(n, s) * mu.
    - A_n = A_{n-1} * (lambda_{n-1}/mu_n) com A_0 = 1; P0 = 1/sum(A_n), Pn = A_n * P0.
    - L = sum n*Pn; Lq = L - E[servidores ocupados]; lambda_eff = lambda * (N - L);
      W = L/lambda_eff, Wq = Lq/lambda_eff.
    """
    if lmbda < 0:
        raise ValueError("lambda (lmbda) deve ser >= 0")
    if mu <= 0:
        raise ValueError("mu deve ser > 0")
    if not isinstance(s, int) or s <= 0:
        raise ValueError("s deve ser inteiro >= 1")
    if not isinstance(N, int) or N < 0:
        raise ValueError("N deve ser inteiro >= 0")

    if N == 0:
        def pn_zero(n_val: int) -> float:
            if n_val < 0 or int(n_val) != n_val or n_val > N:
                raise ValueError(f"n deve ser inteiro entre 0 e {N}")
            return 1.0 if n_val == 0 else 0.0

        result: Dict[str, Any] = {
            "rho": 0.0,
            "p0": 1.0,
            "L": 0.0,
            "Lq": 0.0,
            "W": 0.0,
            "Wq": 0.0,
            "lambda_eff": 0.0,
            "L_operational": 0.0,
            "P(any_idle_server)": 1.0,
        }
        if n is not None:
            result["pn"] = pn_zero(n)
            result["pn_distribution"] = build_pn_distribution(n, pn_zero, max_state=N)
        return result

    lambdas: List[float] = [(N - k) * lmbda for k in range(N + 1)]
    mus: List[float] = [0.0] + [min(i, s) * mu for i in range(1, N + 1)]

    alpha = [0.0] * (N + 1)
    for i in range(1, N + 1):
        alpha[i] = lambdas[i - 1] / mus[i]

    products = [1.0] * (N + 1)
    prod = 1.0
    for i in range(1, N + 1):
        prod *= alpha[i]
        products[i] = prod

    denom = sum(products)
    p0 = 1.0 / denom
    p = [p0 * products[i] for i in range(N + 1)]

    L = sum(i * p[i] for i in range(N + 1))
    busy_servers = sum(min(i, s) * p[i] for i in range(N + 1))
    Lq = L - busy_servers

    lambda_eff = lmbda * (N - L)

    if lambda_eff > 0:
        W = L / lambda_eff
        Wq = Lq / lambda_eff
    else:
        W = Wq = 0.0

    rho = busy_servers / s
    prob_any_idle = sum(p[i] for i in range(min(s, N + 1)))
    L_operational = N - L

    result: Dict[str, Any] = {
        "rho": rho,
        "p0": p0,
        "L": L,
        "Lq": Lq,
        "W": W,
        "Wq": Wq,
        "lambda_eff": lambda_eff,
        "L_operational": L_operational,
        "P(any_idle_server)": prob_any_idle,
    }

    if n is not None:
        if 0 <= n <= N:
            result["pn"] = p[n]
            result["pn_distribution"] = build_pn_distribution(n, lambda idx: p[idx], max_state=N)
        else:
            raise ValueError(f"n deve estar entre 0 e {N}")

    return result
