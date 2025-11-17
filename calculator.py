from typing import Dict

import models

# Mapeamento em torno das funções implementadas em models.py
MODEL_MAP = {
    "M/M/1": models.mm1,
    "M/M/S": models.mms,
    "M/M/1/K": models.mm1k,
    "M/M/S/K": models.mmsk,
    "M/M/1/N": models.mm1n,
    "M/M/S/N": models.mmsn,
}

# Sinônimos usados nos slides/app (maiúsc/minus, >1, sem barras, etc.)
MODEL_ALIASES: Dict[str, str] = {
    "MM1": "M/M/1",
    "MMS": "M/M/S",
    "MM1K": "M/M/1/K",
    "MMSK": "M/M/S/K",
    "MM1N": "M/M/1/N",
    "MMSN": "M/M/S/N",
}


def normalize_model_name(model_name: str) -> str:
    """
    Normaliza variações de escrita (espacos, caixa, '>1') para uma chave
    canônica que esteja em MODEL_MAP.
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
        raise ValueError("Modelo não implementado")

    return model(**params)
