from typing import Any, Callable, Dict

from models import (
    mg1,
    mm1,
    mm1_priority_non_preemptive,
    mm1_priority_preemptive,
    mm1k,
    mm1n,
    mms,
    mms_priority_non_preemptive,
    mms_priority_preemptive,
    mmsk,
    mmsn,
)

# Funcoes canonicas implementadas em cada modulo
MODEL_MAP: Dict[str, Callable[..., Dict[str, Any]]] = {
    "M/M/1": mm1,
    "M/M/S": mms,
    "M/M/1/K": mm1k,
    "M/M/S/K": mmsk,
    "M/M/1/N": mm1n,
    "M/M/S/N": mmsn,
    "M/M/1/PPP": mm1_priority_preemptive,
    "M/M/1/PNP": mm1_priority_non_preemptive,
    "M/M/S/PPP": mms_priority_preemptive,
    "M/M/S/PNP": mms_priority_non_preemptive,
    "M/G/1": mg1,
}

# Sinonimos e abreviacoes que aparecem nos materiais/inputs
MODEL_ALIASES: Dict[str, str] = {
    "MM1": "M/M/1",
    "MMS": "M/M/S",
    "MM1K": "M/M/1/K",
    "MMSK": "M/M/S/K",
    "MM1N": "M/M/1/N",
    "MMSN": "M/M/S/N",
    "MM1PPP": "M/M/1/PPP",
    "MM1PNP": "M/M/1/PNP",
    "MMSPPP": "M/M/S/PPP",
    "MMSPNP": "M/M/S/PNP",
    "MG1": "M/G/1",
}


def normalize_model_name(model_name: str) -> str:
    """
    Normaliza variacoes de escrita (espacos, '>1', caixa) para uma chave
    reconhecida em MODEL_MAP.
    """
    if not model_name:
        return ""

    key = model_name.strip().upper().replace(" ", "")
    key = key.replace(">1", "")

    if key in MODEL_MAP:
        return key

    return MODEL_ALIASES.get(key, key)


def calculate(model_name: str, **params):
    key = normalize_model_name(model_name)
    model = MODEL_MAP.get(key)
    if not model:
        raise ValueError("Modelo nao implementado")

    return model(**params)
