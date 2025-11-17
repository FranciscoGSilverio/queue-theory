from typing import Any, Callable, Dict

import models_np
import models_p

# Funcoes canonicas implementadas em cada modulo
MODEL_MAP: Dict[str, Callable[..., Dict[str, Any]]] = {
    "M/M/1": models_np.mm1,
    "M/M/S": models_np.mms,
    "M/M/1/K": models_np.mm1k,
    "M/M/S/K": models_np.mmsk,
    "M/M/1/N": models_np.mm1n,
    "M/M/S/N": models_np.mmsn,
    "M/M/1/PPP": models_p.mm1_priority_preemptive,
    "M/M/1/PNP": models_p.mm1_priority_non_preemptive,
    "M/M/S/PPP": models_p.mms_priority_preemptive,
    "M/M/S/PNP": models_p.mms_priority_non_preemptive,
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
