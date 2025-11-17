import models

MODEL_MAP = {
    "M/M/1": models.mm1, #chicao fez
    "M/M/s": models.mms,
    "M/M/1/K": models.mm1k,
    "M/M/s/K": models.mmsk, # testado
    "M/M/1/N": models.mm1n,
    # ...
}


def calculate(model_name, **params):
    model = MODEL_MAP.get(model_name)
    if not model:
        raise ValueError("Modelo não implementado")

    return model(**params)
