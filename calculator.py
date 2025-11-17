import models_np
import models_p

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


def calculate(model_name, **params):
    model = MODEL_MAP.get(model_name)
    if not model:
        raise ValueError("Modelo não implementado")

    return model(**params)
