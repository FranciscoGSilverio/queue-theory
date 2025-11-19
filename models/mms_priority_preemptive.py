from typing import Any, Dict, Iterable, List

from .priority_common import (
    aggregate_totals,
    erlang_c,
    prefix_sums,
    validate_common_inputs,
)


def mms_priority_preemptive(
    arrival_rates: Iterable[float],
    mu: float,
    s: int,
) -> Dict[str, Any]:
    """
    Modelo M/M/s com prioridades preemptivas.
    """
    rates = validate_common_inputs(arrival_rates, mu, s=s)
    prefix = prefix_sums(rates)

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
        erlang_c_value = erlang_c(cum_lambda, mu, s)
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

    return aggregate_totals(class_metrics, mu=mu, s=s)
