from typing import Any, Dict
from math import exp

def mm1(lmbda: float, mu: float, n: int = None, t: float = None) -> Dict[str, Any]:
    """
    Calcula as métricas do modelo M/M/1.
    Agora inclui:
      - P(W > t): prob. do tempo de espera no sistema ultrapassar t
      - P(Wq > t): prob. do tempo de espera na fila ultrapassar t
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




def mmc(lmbda, mu, c):
    # implementar fórmula simplificada
    pass


def mm1k(lmbda, mu, K):
    # implementar fórmula correspondente
    pass

# ... e assim por diante até as 11
