from typing import Any, Dict

from .pn_utils import build_pn_distribution


def mm1n(
    lmbda: float,
    mu: float,
    N: int,
    n: int | None = None,
    t: float | None = None,
    **kwargs,
) -> Dict[str, Any]:
    """
    Modelo M/M/1/N (população finita / finite-source).
    N = tamanho da população (máquinas, clientes potenciais, etc.).
    n = estado desejado para Pn (n clientes no sistema).
    """
    if lmbda < 0:
        raise ValueError("lambda (lmbda) deve ser >= 0")
    if mu <= 0:
        raise ValueError("mu deve ser > 0")
    if not isinstance(N, int) or N < 0:
        raise ValueError("N deve ser inteiro >= 0")

    # Caso degenerado: nenhuma fonte
    if N == 0:
        def pn_zero(n_val: int) -> float:
            if n_val < 0 or int(n_val) != n_val or n_val > N:
                raise ValueError(f"n deve ser inteiro entre 0 e {N}")
            return 1.0 if n_val == 0 else 0.0

        result: Dict[str, Any] = {
            "rho": 0.0,              # parâmetro N*lambda/mu
            "p0": 1.0,
            "L": 0.0,
            "Lq": 0.0,
            "W": 0.0,
            "Wq": 0.0,
            "lambda_eff": 0.0,
            "L_operational": 0.0,
            "server_utilization": 0.0,
        }
        if n is not None:
            result["pn"] = pn_zero(n)
            result["pn_distribution"] = build_pn_distribution(n, pn_zero, max_state=N)
        return result

    # Razão r = lambda/mu
    r = lmbda / mu

    # A_n = N!/(N-n)! * r^n, construído recursivamente
    # A_0 = 1
    A: list[float] = [1.0]
    for k in range(1, N + 1):
        # A_k = A_{k-1} * (N-(k-1)) * r
        A_k = A[k - 1] * (N - (k - 1)) * r
        A.append(A_k)

    # P0 = 1 / sum(A_n)
    denom = sum(A)
    p0 = 1.0 / denom

    # Pn = A_n * P0
    pn_values = [a * p0 for a in A]

    def pn_func(n_val: int) -> float:
        if n_val < 0 or int(n_val) != n_val or n_val > N:
            raise ValueError(f"n deve ser inteiro entre 0 e {N}")
        return pn_values[n_val]

    # Número médio no sistema
    L = sum(k * pn_values[k] for k in range(N + 1))

    # Número médio em serviço (só 0 ou 1 servidor): E[em serviço] = 1 - P0
    L_service = 1.0 - p0

    # Número médio na "fila" (entidades esperando)
    Lq = L - L_service
    if Lq < 0:
        Lq = 0.0  # proteção numérica

    # Taxa efetiva de chegada (ou de saída) = mu * E[em serviço]
    lambda_eff = mu * L_service
    if lambda_eff > 0:
        W = L / lambda_eff
        Wq = Lq / lambda_eff
    else:
        W = 0.0
        Wq = 0.0

    # Número médio fora do sistema (população total - em sistema)
    L_operational = N - L

    result: Dict[str, Any] = {
        # este rho é o parâmetro N*lambda/mu, como em muitos livros/slides
        "rho": N * lmbda / mu,
        "p0": p0,
        "L": L,
        "Lq": Lq,
        "W": W,
        "Wq": Wq,
        "lambda_eff": lambda_eff,
        "L_operational": L_operational,
        # utilização real do servidor (probabilidade de estar ocupado)
        "server_utilization": L_service,
    }

    if n is not None:
        result["pn"] = pn_func(n)
        result["pn_distribution"] = build_pn_distribution(n, pn_func, max_state=N)

    # t (P(W>t), P(Wq>t)) não é trivial no modelo de fonte finita,
    # então deixei sem usar aqui. Se você quiser, dá pra implementar
    # depois com aproximações, mas não é padrão em M/M/1/N.
    return result
