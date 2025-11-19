from typing import Any, Dict, Iterable, List

from .mms_priority_preemptive import mms_priority_preemptive
from .priority_common import (
    aggregate_totals,
    erlang_c,
    prefix_sums,
    validate_common_inputs,
)


def mms_priority_non_preemptive(
    arrival_rates: Iterable[float],
    mu: float,
    s: int,
) -> Dict[str, Any]:
    """
    Modelo M/M/s com prioridades nao preemptivas.
    """
    rates = validate_common_inputs(arrival_rates, mu, s=s)
    prefix = prefix_sums(rates)
    total_lambda = prefix[-1]

    if total_lambda == 0:
        return mms_priority_preemptive(arrival_rates, mu, s)

    class_metrics: List[Dict[str, float]] = []
    for idx, lam in enumerate(rates):
        cum_lambda = prefix[idx]
        erlang_c_value = erlang_c(cum_lambda, mu, s)
        denom = (s * mu) - cum_lambda
        if denom <= 0:
            raise ValueError(
                f"A subfila ate a classe {idx + 1} ficou instavel: lambda={cum_lambda:.6f} >= s*mu."
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

    return aggregate_totals(class_metrics, mu=mu, s=s)
