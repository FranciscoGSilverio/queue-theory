from typing import Any, Callable, Dict

from models import (
    mg1,
    mm1,
    mm1k,
    mm1n,
    mms,
    mmsk,
    mmsn,
    priority_with_preemption,
    priority_without_preemption,
)

# Funcoes canonicas implementadas em cada modulo
MODEL_MAP: Dict[str, Callable[..., Dict[str, Any]]] = {
    "M/M/1": mm1,
    "M/M/S": mms,
    "M/M/1/K": mm1k,
    "M/M/S/K": mmsk,
    "M/M/1/N": mm1n,
    "M/M/S/N": mmsn,
    "PRIORIDADE_PREEMPTIVA_3X3": priority_with_preemption,
    "PRIORIDADE_NAO_PREEMPTIVA_3X3": priority_without_preemption,
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
    "MG1": "M/G/1",
    "PRIORIDADECOMINTERRUPCAO": "PRIORIDADE_PREEMPTIVA_3X3",
    "PRIORIDADESEMINTERROMPER": "PRIORIDADE_NAO_PREEMPTIVA_3X3",
    "PRIORIDADESEMINTERRUPCAO": "PRIORIDADE_NAO_PREEMPTIVA_3X3",
    "PRIORIDADECOMINT": "PRIORIDADE_PREEMPTIVA_3X3",
    "PRIORIDADESEMSUSPENSAO": "PRIORIDADE_NAO_PREEMPTIVA_3X3",
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
