from typing import Any, Dict

from .pn_utils import build_pn_distribution


def mm1k(
    lmbda: float,
    mu: float,
    K: int,
    n: int | None = None,
    t: float | None = None,
    **kwargs,
) -> Dict[str, Any]:
    """
    Modelo M/M/1/K com capacidade finita K (inclui o cliente em servico).

    - Pn = rho^n * P0 para 0 <= n <= K (rho = lambda/mu); fora do intervalo Pn = 0.
    - P0 = 1 / sum_{n=0..K} rho^n (ou 1/(K+1) se rho=1).
    - lambda_eff = lambda * (1 - P_K); L = sum n*Pn; Lq = L - (1 - P0);
      W = L/lambda_eff, Wq = Lq/lambda_eff.
    Parametros opcionais:
      - n: calcula Pn
      - t: aceito mas ignorado (nao ha P(W>t) especifico)
    """
    if lmbda < 0:
        raise ValueError("lambda (lmbda) deve ser >= 0")
    if mu <= 0:
        raise ValueError("mu deve ser > 0")
    if not isinstance(K, int) or K < 0:
        raise ValueError("K deve ser inteiro >= 0")

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

    rho = lmbda / mu

    if abs(rho - 1.0) < 1e-8:
        p0 = 1.0 / (K + 1)

        def pn_func(n_val: int) -> float:
            if n_val < 0 or int(n_val) != n_val:
                raise ValueError(f"n deve ser inteiro entre 0 e {K}")
            if n_val > K:
                return 0.0
            return p0

        L = K / 2.0
    else:
        p0 = (1 - rho) / (1 - rho ** (K + 1))

        def pn_func(n_val: int) -> float:
            if n_val < 0 or int(n_val) != n_val:
                raise ValueError(f"n deve ser inteiro entre 0 e {K}")
            if n_val > K:
                return 0.0
            return p0 * (rho**n_val)

        L = (rho * (1 - (K + 1) * rho**K + K * rho ** (K + 1))) / (
            (1 - rho) * (1 - rho ** (K + 1))
        )

    pK = pn_func(K)
    lambda_eff = lmbda * (1 - pK)
    Lq = L - (1 - p0)

    if lambda_eff > 0:
        W = L / lambda_eff
        Wq = Lq / lambda_eff
    else:
        W = Wq = 0.0

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
