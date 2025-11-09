import models

MODEL_MAP = {
    "M/M/1": models.mm1,
    "M/M/c": models.mmc,
    "M/M/1/K": models.mm1k,
    # ...
}


def calculate(model_name, **params):
    model = MODEL_MAP.get(model_name)
    if not model:
        raise ValueError("Modelo não implementado")

    return model(**params)
