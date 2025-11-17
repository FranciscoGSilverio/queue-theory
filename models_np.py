from typing import Any, Dict
from math import exp, factorial


def mm1(
    lmbda: float,
    mu: float,
    n: int = None,
    t: float = None,
    **kwargs,
) -> Dict[str, Any]:
    """
    Modelo M/M/1.

    Opcionais:
      - n: retorna Pn
      - t: retorna P(W>t) e P(Wq>t)
    Outros kwargs (s, K, N, etc.) são ignorados.
    """
    if lmbda < 0:
        raise ValueError("λ (lmbda) deve ser >= 0")
    if mu <= 0:
        raise ValueError("μ (mu) deve ser > 0")

    rho = lmbda / mu

    if rho >= 1:
        raise ValueError(f"Sistema instável (ρ = {rho:.6f} >= 1).")

    p0 = 1 - rho

    # P(n) = (1 - rho) * rho^n
    def pn(n_val: int) -> float:
        if n_val < 0 or int(n_val) != n_val:
            raise ValueError("n deve ser inteiro >= 0")
        return p0 * (rho ** n_val)

    # Médias
    L = rho / (1 - rho)
    Lq = (rho ** 2) / (1 - rho)
    W = L / lmbda
    Wq = Lq / lmbda

    result: Dict[str, Any] = {
        "rho": rho,
        "p0": p0,
        "L": L,
        "Lq": Lq,
        "W": W,
        "Wq": Wq,
    }

    if n is not None:
        result["pn"] = pn(n)

    # Probabilidades associadas a t
    if t is not None:
        if t < 0:
            raise ValueError("t deve ser >= 0")

        # P(W > t) = e^(-μ(1-ρ)t)
        PW_gt_t = exp(-mu * (1 - rho) * t)

        # P(Wq > t) = ρ * e^(-μ(1-ρ)t)
        PWq_gt_t = rho * PW_gt_t

        result["P(W>t)"] = PW_gt_t
        result["P(Wq>t)"] = PWq_gt_t

    return result


def mms(
    lmbda: float,
    mu: float,
    s: int,
    n: int = None,
    t: float = None,
    **kwargs,
) -> Dict[str, Any]:
    """
    Modelo M/M/s (s >= 1, capacidade infinita).

    Opcionais:
      - n: retorna Pn
      - t: P(W>t) e P(Wq>t) via fórmula de Erlang C.
    """
    if lmbda < 0:
        raise ValueError("λ (lmbda) deve ser >= 0")
    if mu <= 0:
        raise ValueError("μ (mu) deve ser > 0")
    if not isinstance(s, int) or s <= 0:
        raise ValueError("s deve ser inteiro >= 1")

    # caso trivial λ = 0
    if lmbda == 0:
        result: Dict[str, Any] = {
            "rho": 0.0,
            "p0": 1.0,
            "L": 0.0,
            "Lq": 0.0,
            "W": 0.0,
            "Wq": 0.0,
        }
        if n is not None:
            result["pn"] = 1.0 if n == 0 else 0.0
        if t is not None:
            result["P(W>t)"] = 0.0
            result["P(Wq>t)"] = 0.0
        return result

    rho = lmbda / (s * mu)        # taxa de ocupação do sistema

    if rho >= 1:
        raise ValueError(f"Sistema instável (ρ = {rho:.6f} >= 1).")

    a = lmbda / mu                # λ/μ

    # P0
    sum1 = sum(a**k / factorial(k) for k in range(s))
    sum2 = (a**s / (factorial(s) * (1 - rho)))
    p0 = 1.0 / (sum1 + sum2)

    # Pn
    def pn_func(n_val: int) -> float:
        if n_val < 0 or int(n_val) != n_val:
            raise ValueError("n deve ser inteiro >= 0")
        if n_val <= s:
            return (a**n_val / factorial(n_val)) * p0
        else:
            return (a**n_val / (factorial(s) * (s ** (n_val - s)))) * p0

    # Lq, L, Wq, W (fórmulas padrão M/M/s)
    Lq = p0 * (a**s) * rho / (factorial(s) * (1 - rho) ** 2)
    L  = Lq + a                   # a = λ/μ
    Wq = Lq / lmbda
    W  = L  / lmbda

    result: Dict[str, Any] = {
        "rho": rho,
        "p0": p0,
        "L": L,
        "Lq": Lq,
        "W": W,
        "Wq": Wq,
    }

    if n is not None:
        result["pn"] = pn_func(n)

    # Probabilidades em função de t (M/M/s)
    if t is not None:
        if t < 0:
            raise ValueError("t deve ser >= 0")

        # Probabilidade de ter que esperar (Erlang C)
        C = (a**s / (factorial(s) * (1 - rho))) * p0

        # P(Wq > t) = C * e^{-(1-ρ)s μ t}
        PWq_gt_t = C * exp(-(1 - rho) * s * mu * t)

        # P(W > t) = e^{-μ t} [1 + C * (1 - e^{-μ t (s-1- a)}) / (s-1 - a)]
        denom = (s - 1) - a
        if abs(denom) < 1e-8:
            inner = C * (mu * t)   # limite quando denom -> 0
        else:
            inner = C * (1 - exp(-mu * t * denom)) / denom

        PW_gt_t = exp(-mu * t) * (1 + inner)

        result["P(Wq>t)"] = PWq_gt_t
        result["P(W>t)"]  = PW_gt_t

    return result


def mm1k(
    lmbda: float,
    mu: float,
    K: int,
    n: int = None,
    t: float = None,
    **kwargs,
) -> Dict[str, Any]:
    """
    Modelo M/M/1/K (capacidade finita K, incluindo o em serviço).

    Opcionais:
      - n: retorna Pn
      - t: aceito, mas ignorado (não usamos P(W>t) aqui).
    """
    if lmbda < 0:
        raise ValueError("λ (lmbda) deve ser >= 0")
    if mu <= 0:
        raise ValueError("μ (mu) deve ser > 0")
    if not isinstance(K, int) or K < 0:
        raise ValueError("K deve ser inteiro >= 0")

    if lmbda == 0:
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
            result["pn"] = 1.0 if n == 0 else 0.0
        return result

    rho = lmbda / mu  # aqui pode ser >= 1, o sistema é finito

    # caso especial ρ ≈ 1
    if abs(rho - 1.0) < 1e-8:
        p0 = 1.0 / (K + 1)

        def pn_func(n_val: int) -> float:
            if n_val < 0 or int(n_val) != n_val or n_val > K:
                raise ValueError(f"n deve ser inteiro entre 0 e {K}")
            return p0  # todos os estados com mesma probabilidade

        L = K / 2.0
    else:
        p0 = (1 - rho) / (1 - rho ** (K + 1))

        def pn_func(n_val: int) -> float:
            if n_val < 0 or int(n_val) != n_val or n_val > K:
                raise ValueError(f"n deve ser inteiro entre 0 e {K}")
            return p0 * (rho ** n_val)

        # L (mesma expressão usada nos livros/planilhas)
        L = (rho * (1 - (K + 1) * rho**K + K * rho ** (K + 1))) / (
            (1 - rho) * (1 - rho ** (K + 1))
        )

    pK = pn_func(K)
    lambda_eff = lmbda * (1 - pK)

    # Lq = L - (1 - p0)
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

    # t ignorado
    return result


def mmsk(
    lmbda: float,
    mu: float,
    s: int,
    K: int,
    n: int = None,
    t: float = None,
    **kwargs,
) -> Dict[str, Any]:
    """
    Modelo M/M/s/K (s >= 1, capacidade total K).

    Opcionais:
      - n: retorna Pn
      - t: aceito, mas ignorado.
    """
    if lmbda < 0:
        raise ValueError("λ (lmbda) deve ser >= 0")
    if mu <= 0:
        raise ValueError("μ (mu) deve ser > 0")
    if not isinstance(s, int) or s <= 0:
        raise ValueError("s deve ser inteiro >= 1")
    if not isinstance(K, int) or K < 0:
        raise ValueError("K deve ser inteiro >= 0")
    if K < s:
        raise ValueError("K deve ser >= s")

    if lmbda == 0:
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
            result["pn"] = 1.0 if n == 0 else 0.0
        return result

    rho = lmbda / (s * mu)   # aqui pode ser >= 1
    a = lmbda / mu

    # P0 (soma até K)
    sum1 = sum(a**n_state / factorial(n_state) for n_state in range(s + 1))
    sum2 = sum(
        (a**n_state) / (factorial(s) * (s ** (n_state - s)))
        for n_state in range(s + 1, K + 1)
    )
    p0 = 1.0 / (sum1 + sum2)

    def pn_func(n_val: int) -> float:
        if n_val < 0 or int(n_val) != n_val or n_val > K:
            raise ValueError(f"n deve ser inteiro entre 0 e {K}")
        if n_val <= s:
            return (a**n_val / factorial(n_val)) * p0
        else:
            return (a**n_val / (factorial(s) * (s ** (n_val - s)))) * p0

    # Lq (fórmula do slide para M/M/s/K)
    if abs(1 - rho) < 1e-10:
        raise ValueError("Caso ρ ≈ 1 não tratado na fórmula de Lq para M/M/s/K.")

    factor = p0 * (a**s) * rho / (factorial(s) * (1 - rho) ** 2)
    tail   = 1 - rho ** (K - s) - (K - s) * (1 - rho) * rho ** (K - s)
    Lq = factor * tail

    # L = Σ_{n=0}^{s-1} n Pn + Lq + s * (1 - Σ_{n=0}^{s-1} Pn)
    sumPn = [pn_func(nv) for nv in range(s)]
    L_partial = sum(nv * pn_func(nv) for nv in range(s))
    prob_busy_at_least_one = 1 - sum(sumPn)
    L = L_partial + Lq + s * prob_busy_at_least_one

    # λ̄ = λ (1 - P_K)
    pK = pn_func(K)
    lambda_eff = lmbda * (1 - pK)

    if lambda_eff > 0:
        W  = L  / lambda_eff
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

    return result


def _comb(n: int, k: int) -> int:
    """Combinação nCk simples (para o modelo com população finita)."""
    if k < 0 or k > n:
        return 0
    k = min(k, n - k)
    num = 1
    den = 1
    for i in range(1, k + 1):
        num *= n - (k - i)
        den *= i
    return num // den


def mm1n(
    lmbda: float,
    mu: float,
    N: int,
    n: int = None,
    t: float = None,
    **kwargs,
) -> Dict[str, Any]:
    """
    Modelo M/M/1/N (população finita N — “machine repair” com 1 servidor).

    Opcionais:
      - n: retorna Pn
      - t: aceito, mas ignorado (slides normalmente não usam P(W>t) aqui).
    """
    if lmbda < 0:
        raise ValueError("λ (lmbda) deve ser >= 0")
    if mu <= 0:
        raise ValueError("μ (mu) deve ser > 0")
    if not isinstance(N, int) or N < 0:
        raise ValueError("N deve ser inteiro >= 0")

    if N == 0:
        result: Dict[str, Any] = {
            "rho": 0.0,
            "p0": 1.0,
            "L": 0.0,
            "Lq": 0.0,
            "W": 0.0,
            "Wq": 0.0,
            "lambda_eff": 0.0,
            "L_operational": 0.0,
        }
        if n is not None:
            result["pn"] = 1.0 if n == 0 else 0.0
        return result

    r = lmbda / mu

    # normalização
    denom = sum(_comb(N, k) * (r ** k) for k in range(N + 1))
    p0 = 1.0 / denom

    pn_values = [_comb(N, k) * (r ** k) * p0 for k in range(N + 1)]

    def pn_func(n_val: int) -> float:
        if n_val < 0 or int(n_val) != n_val or n_val > N:
            raise ValueError(f"n deve ser inteiro entre 0 e {N}")
        return pn_values[n_val]

    L  = sum(k * pn_values[k] for k in range(N + 1))
    Lq = L - (1 - p0)
    lambda_eff = lmbda * (N - L)

    if lambda_eff > 0:
        W  = L  / lambda_eff
        Wq = Lq / lambda_eff
    else:
        W = Wq = 0.0

    # número médio de itens operacionais
    L_operational = N - L

    result: Dict[str, Any] = {
        "rho": N * lmbda / mu,   # apenas indicador
        "p0": p0,
        "L": L,
        "Lq": Lq,
        "W": W,
        "Wq": Wq,
        "lambda_eff": lambda_eff,
        "L_operational": L_operational,
    }

    if n is not None:
        result["pn"] = pn_func(n)

    # t ignorado
    return result


def mmsn(
    lmbda: float,
    mu: float,
    s: int,
    N: int,
    n: int = None,
    t: float = None,
    **kwargs,
) -> Dict[str, Any]:
    """
    Modelo M/M/s/N (população finita N, s servidores) – ex.: robôs + técnicos.

    Interpretação:
      - N: número total de “máquinas”/robôs
      - s: número de técnicos/servidores
      - cada máquina operacional falha com taxa λ
      - cada servidor repara com taxa μ

    Opcionais:
      - n: retorna Pn
      - t: aceito, mas ignorado (sem fórmula simples nos slides).
    """
    if lmbda < 0:
        raise ValueError("λ (lmbda) deve ser >= 0")
    if mu <= 0:
        raise ValueError("μ (mu) deve ser > 0")
    if not isinstance(s, int) or s <= 0:
        raise ValueError("s deve ser inteiro >= 1")
    if not isinstance(N, int) or N < 0:
        raise ValueError("N deve ser inteiro >= 0")

    if N == 0:
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
            result["pn"] = 1.0 if n == 0 else 0.0
        return result

    # taxas de nascimento/morte:
    # λ_n = (N - n) λ
    # μ_n = min(n, s) μ
    lambdas = [(N - k) * lmbda for k in range(N + 1)]        # estados 0..N
    mus = [0.0] + [min(i, s) * mu for i in range(1, N + 1)]  # estados 1..N

    # α_n = λ_{n-1} / μ_n
    alpha = [0.0] * (N + 1)
    for i in range(1, N + 1):
        alpha[i] = lambdas[i - 1] / mus[i]

    # produtos parciais Π_{k=1}^n α_k
    products = [1.0] * (N + 1)
    prod = 1.0
    for i in range(1, N + 1):
        prod *= alpha[i]
        products[i] = prod

    # normalização
    denom = sum(products)                    # Σ_{n=0}^N Π_{k=1}^n α_k
    p0 = 1.0 / denom
    p = [p0 * products[i] for i in range(N + 1)]

    # L = número médio de máquinas quebradas (em fila + em reparo)
    L = sum(i * p[i] for i in range(N + 1))

    # número médio de servidores ocupados
    busy_servers = sum(min(i, s) * p[i] for i in range(N + 1))

    # Lq = máquinas esperando (quebradas, mas não em reparo)
    Lq = L - busy_servers

    # taxa efetiva de falhas: λ̄ = λ * E[# operacionais] = λ (N - L)
    lambda_eff = lmbda * (N - L)

    if lambda_eff > 0:
        W = L / lambda_eff       # tempo médio de máquina quebrada (sistema)
        Wq = Lq / lambda_eff     # tempo médio esperando antes do reparo
    else:
        W = Wq = 0.0

    # utilização média por servidor
    rho = busy_servers / s

    # prob. de pelo menos 1 servidor ocioso (n < s)
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
        else:
            raise ValueError(f"n deve estar entre 0 e {N}")

    # t ignorado
    return result
