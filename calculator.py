import models_np
import models_p

# Mapeamento em torno das funções implementadas em models.py
MODEL_MAP = {
    "M/M/1": models_np.mm1, #chicao fez
    "M/M/s": models_np.mms,
    "M/M/1/K": models_np.mm1k,
    "M/M/s/K": models_np.mmsk, # testado
    "M/M/1/N": models_np.mm1n,
    "M/M/s/N": models_np.mmsn, # testado
    "M/M/1/PPP": models_p.mm1_priority_preemptive,
    "M/M/1/PNP": models_p.mm1_priority_non_preemptive,
    "M/M/s/PPP": models_p.mms_priority_preemptive,
    "M/M/s/PNP": models_p.mms_priority_non_preemptive,
    # ...
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
