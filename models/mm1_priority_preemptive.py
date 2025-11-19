from typing import Any, Dict, Iterable, List

from .priority_common import aggregate_totals, prefix_sums, validate_common_inputs


def mm1_priority_preemptive(
    arrival_rates: Iterable[float],
    mu: float,
) -> Dict[str, Any]:
    """
    Modelo M/M/1 com prioridades preemptivas (com retomada).
    """
    rates = validate_common_inputs(arrival_rates, mu, s=1)
    prefix = prefix_sums(rates)
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

    return aggregate_totals(class_metrics, mu=mu, s=1)
