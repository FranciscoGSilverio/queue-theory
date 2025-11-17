from typing import Any, Dict, Iterable, List
from math import factorial


def _coerce_arrival_rates(arrival_rates: Iterable[float]) -> List[float]:
    if arrival_rates is None:
        raise ValueError("É necessário fornecer as taxas de chegada por prioridade.")

    try:
        rates = [float(v) for v in arrival_rates]
    except TypeError as exc:  # not iterable
        raise ValueError("arrival_rates deve ser um iterável com números >= 0.") from exc

    if not rates:
        raise ValueError("arrival_rates não pode ser vazio.")

    for idx, rate in enumerate(rates, start=1):
        if rate < 0:
            raise ValueError(f"λ_{idx} deve ser >= 0.")
    return rates


def _validate_common_inputs(rates: Iterable[float], mu: float, s: int) -> List[float]:
    clean_rates = _coerce_arrival_rates(rates)

    if mu <= 0:
        raise ValueError("µ deve ser > 0.")
    if not isinstance(s, int) or s <= 0:
        raise ValueError("s deve ser inteiro >= 1.")

    total_lambda = sum(clean_rates)
    capacity = s * mu
    if total_lambda >= capacity and capacity > 0:
        raise ValueError(
            f"Sistema instável: λ_total={total_lambda:.6f} >= s*µ = {capacity:.6f}."
        )
    return clean_rates


def _prefix_sums(values: List[float]) -> List[float]:
    result: List[float] = []
    running = 0.0
    for value in values:
        running += value
        result.append(running)
    return result


def _erlang_c(lmbda: float, mu: float, s: int) -> float:
    if lmbda <= 0:
        return 0.0

    rho = lmbda / (s * mu)
    if rho >= 1:
        raise ValueError(
            f"Subfila com λ={lmbda:.6f} e s*µ={s*mu:.6f} é instável (ρ={rho:.6f} >= 1)."
        )

    a = lmbda / mu
    sum_terms = sum((a**k) / factorial(k) for k in range(s))
    last_term = (a**s) / (factorial(s) * (1 - rho))
    p0 = 1.0 / (sum_terms + last_term)
    return last_term * p0


def _aggregate_totals(class_metrics: List[Dict[str, float]], mu: float, s: int) -> Dict[str, Any]:
    total_lambda = sum(cls["lambda"] for cls in class_metrics)
    total_L = sum(cls["L"] for cls in class_metrics)
    total_Lq = sum(cls["Lq"] for cls in class_metrics)
    service_time = (total_lambda / mu) if mu > 0 else 0.0
    if total_lambda > 0:
        W = total_L / total_lambda
        Wq = total_Lq / total_lambda
    else:
        W = Wq = 0.0

    rho = total_lambda / (s * mu)

    # Probabilidade do sistema vazio segue o modelo clássico sem prioridades.
    if s == 1:
        p0 = 1.0 - rho
    else:
        a = total_lambda / mu
        sum_terms = sum((a**k) / factorial(k) for k in range(s))
        last_term = (a**s) / (factorial(s) * (1 - rho))
        p0 = 1.0 / (sum_terms + last_term)

    return {
        "rho": rho,
        "p0": p0,
        "L": total_L,
        "Lq": total_Lq,
        "W": W,
        "Wq": Wq,
        "per_class": class_metrics,
        "lambda_total": total_lambda,
        "service_in_progress": service_time,
    }


def mm1_priority_preemptive(
    arrival_rates: Iterable[float],
    mu: float,
) -> Dict[str, Any]:
    """
    Modelo M/M/1 com prioridades (preemptivo com retomada).

    arrival_rates: iterável com λ_i em ordem de prioridade (1 = maior).
    Retorna métricas globais e por classe.
    """

    rates = _validate_common_inputs(arrival_rates, mu, s=1)
    prefix = _prefix_sums(rates)
    total_lambda = prefix[-1]

    if total_lambda == 0:
        return {
            "rho": 0.0,
            "p0": 1.0,
            "L": 0.0,
            "Lq": 0.0,
            "W": 0.0,
            "Wq": 0.0,
            "per_class": [
                {
                    "priority": idx + 1,
                    "lambda": lam,
                    "rho": 0.0,
                    "W": 0.0,
                    "Wq": 0.0,
                    "L": 0.0,
                    "Lq": 0.0,
                }
                for idx, lam in enumerate(rates)
            ],
            "lambda_total": 0.0,
            "service_in_progress": 0.0,
        }

    class_metrics: List[Dict[str, float]] = []
    for idx, lam in enumerate(rates):
        cum_lambda = prefix[idx]
        if cum_lambda == 0:
            Wq = 0.0
        else:
            Wq = cum_lambda / (mu * (mu - cum_lambda))

        W = Wq + 1.0 / mu
        Lq = lam * Wq
        L = lam * W
        class_metrics.append(
            {
                "priority": idx + 1,
                "lambda": lam,
                "rho": lam / mu,
                "W": W,
                "Wq": Wq,
                "L": L,
                "Lq": Lq,
            }
        )

    return _aggregate_totals(class_metrics, mu=mu, s=1)


def mm1_priority_non_preemptive(
    arrival_rates: Iterable[float],
    mu: float,
) -> Dict[str, Any]:
    """
    Modelo M/M/1 com prioridades sem interrupção (não-preemptivo).
    Fórmulas clássicas para M/M/1 com m classes em ordem estrita.
    """

    rates = _validate_common_inputs(arrival_rates, mu, s=1)
    prefix = _prefix_sums(rates)
    total_lambda = prefix[-1]

    if total_lambda == 0:
        return mm1_priority_preemptive(arrival_rates, mu)

    class_metrics: List[Dict[str, float]] = []
    for idx, lam in enumerate(rates):
        cum_lambda = prefix[idx]
        higher_lambda = prefix[idx - 1] if idx > 0 else 0.0
        denom = mu - cum_lambda
        if denom <= 0:
            raise ValueError(
                f"A subfila até a classe {idx+1} ficou instável: λ={cum_lambda:.6f} >= µ."
            )
        Wq = (total_lambda + higher_lambda) / (mu * denom)
        W = Wq + 1.0 / mu
        Lq = lam * Wq
        L = lam * W
        class_metrics.append(
            {
                "priority": idx + 1,
                "lambda": lam,
                "rho": lam / mu,
                "W": W,
                "Wq": Wq,
                "L": L,
                "Lq": Lq,
            }
        )

    return _aggregate_totals(class_metrics, mu=mu, s=1)


def mms_priority_preemptive(
    arrival_rates: Iterable[float],
    mu: float,
    s: int,
) -> Dict[str, Any]:
    """
    Modelo M/M/s com prioridades e preempção.
    A subfila formada pelas classes 1..i se comporta como um M/M/s clássico com λ = Σ_{j<=i} λ_j.
    """

    rates = _validate_common_inputs(arrival_rates, mu, s=s)
    prefix = _prefix_sums(rates)

    total_lambda = prefix[-1]
    if total_lambda == 0:
        zero_metrics = [
            {
                "priority": idx + 1,
                "lambda": lam,
                "rho": 0.0,
                "W": 0.0,
                "Wq": 0.0,
                "L": 0.0,
                "Lq": 0.0,
            }
            for idx, lam in enumerate(rates)
        ]
        return {
            "rho": 0.0,
            "p0": 1.0,
            "L": 0.0,
            "Lq": 0.0,
            "W": 0.0,
            "Wq": 0.0,
            "per_class": zero_metrics,
            "lambda_total": 0.0,
            "service_in_progress": 0.0,
        }

    class_metrics: List[Dict[str, float]] = []
    for idx, lam in enumerate(rates):
        cum_lambda = prefix[idx]
        erlang_c_value = _erlang_c(cum_lambda, mu, s)
        denom = (s * mu) - cum_lambda
        Wq = erlang_c_value / denom
        W = Wq + 1.0 / mu
        Lq = lam * Wq
        L = lam * W
        class_metrics.append(
            {
                "priority": idx + 1,
                "lambda": lam,
                "rho": lam / (s * mu),
                "W": W,
                "Wq": Wq,
                "L": L,
                "Lq": Lq,
                "P(wait)": erlang_c_value,
            }
        )

    return _aggregate_totals(class_metrics, mu=mu, s=s)


def mms_priority_non_preemptive(
    arrival_rates: Iterable[float],
    mu: float,
    s: int,
) -> Dict[str, Any]:
    """
    Modelo M/M/s com prioridades sem interrupção.

    A parcela de espera causada por classes de maior prioridade segue a mesma lógica
    do caso preemptivo (Erlang C aplicado a λ acumulado). Acrescenta-se o impacto
    médio do tempo residual de clientes de prioridade inferior já em serviço.
    """

    rates = _validate_common_inputs(arrival_rates, mu, s=s)
    prefix = _prefix_sums(rates)
    total_lambda = prefix[-1]

    if total_lambda == 0:
        return mms_priority_preemptive(arrival_rates, mu, s)

    class_metrics: List[Dict[str, float]] = []
    for idx, lam in enumerate(rates):
        cum_lambda = prefix[idx]
        erlang_c_value = _erlang_c(cum_lambda, mu, s)
        denom = (s * mu) - cum_lambda
        if denom <= 0:
            raise ValueError(
                f"A subfila até a classe {idx+1} ficou instável: λ={cum_lambda:.6f} >= s*µ."
            )

        Wq_preemptive = erlang_c_value / denom
        residual_delay = (total_lambda - lam) / (s * mu * denom) if total_lambda > 0 else 0.0
        Wq = Wq_preemptive + residual_delay
        W = Wq + 1.0 / mu
        Lq = lam * Wq
        L = lam * W
        class_metrics.append(
            {
                "priority": idx + 1,
                "lambda": lam,
                "rho": lam / (s * mu),
                "W": W,
                "Wq": Wq,
                "L": L,
                "Lq": Lq,
                "P(wait)": erlang_c_value,
            }
        )

    return _aggregate_totals(class_metrics, mu=mu, s=s)

