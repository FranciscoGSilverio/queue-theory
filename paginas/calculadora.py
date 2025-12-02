import streamlit as st
from dataclasses import dataclass
from typing import Any, Dict, List

from calculator import MODEL_MAP, calculate


@dataclass
class InputField:
    name: str
    label: str
    field_type: str = "float"  # float, int, list_float, string, select
    required: bool = True
    placeholder: str | None = None
    help_text: str | None = None
    options: List[str] | None = None
    default: Any = ""


MODEL_CONFIG: Dict[str, Dict[str, Any]] = {
    "M/M/1": {
        "description": "Fila M/M/1 com um servidor e capacidade infinita.",
        "fields": [
            InputField("lmbda", "Taxa de chegada (lambda)", placeholder="ex: 12.5"),
            InputField("mu", "Taxa de servico (mu)", placeholder="ex: 15"),
            InputField("n", "n (probabilidade Pn)", field_type="int", required=False, placeholder="opcional"),
            InputField(
                "t",
                "t (tempo para P(W>t) / P(Wq>t)) [mesma unidade de λ e μ]",
                field_type="float",
                required=False,
                placeholder="ex: 0.05 (3 min se λ, μ em horas)",
                help_text="Use o mesmo tempo de λ e μ. Ex: se λ e μ são por hora, 0.05 h ≈ 3 min.",
            ),
        ],
    },
    "M/M/S": {
        "description": "Fila M/M/s com multiplos servidores e capacidade infinita.",
        "fields": [
            InputField("lmbda", "Taxa de chegada (lambda)", placeholder="ex: 20"),
            InputField("mu", "Taxa de servico (mu)", placeholder="ex: 12"),
            InputField("s", "Numero de servidores (s)", field_type="int", placeholder="ex: 3"),
            InputField("n", "n (probabilidade Pn)", field_type="int", required=False, placeholder="opcional"),
            InputField(
                "t",
                "t (tempo para P(W>t) / P(Wq>t)) [mesma unidade de λ e μ]",
                field_type="float",
                required=False,
                placeholder="ex: 0.05 (3 min se λ, μ em horas)",
                help_text="Use o mesmo tempo de λ e μ. Ex: se λ e μ são por hora, 0.05 h ≈ 3 min.",
            ),
        ],
    },
    "M/M/1/K": {
        "description": "Fila M/M/1 com capacidade total K (incluindo o cliente em servico).",
        "fields": [
            InputField("lmbda", "Taxa de chegada (lambda)", placeholder="ex: 8"),
            InputField("mu", "Taxa de servico (mu)", placeholder="ex: 10"),
            InputField("K", "Capacidade total (K)", field_type="int", placeholder="ex: 12"),
            InputField("n", "n (probabilidade Pn)", field_type="int", required=False, placeholder="opcional"),
        ],
    },
    "M/M/S/K": {
        "description": "Fila M/M/s com capacidade maxima K.",
        "fields": [
            InputField("lmbda", "Taxa de chegada (lambda)", placeholder="ex: 18"),
            InputField("mu", "Taxa de servico (mu)", placeholder="ex: 7"),
            InputField("s", "Numero de servidores (s)", field_type="int", placeholder="ex: 4"),
            InputField("K", "Capacidade total (K)", field_type="int", placeholder="ex: 30"),
            InputField("n", "n (probabilidade Pn)", field_type="int", required=False, placeholder="opcional"),
        ],
    },
    "M/M/1/N": {
        "description": "Fila M/M/1 com populacao finita N (maquinas/itens disponiveis).",
        "fields": [
            InputField("lmbda", "Taxa de chegada (lambda)", placeholder="ex: 6"),
            InputField("mu", "Taxa de servico (mu)", placeholder="ex: 9"),
            InputField("N", "Tamanho da populacao (N)", field_type="int", placeholder="ex: 20"),
            InputField("n", "n (probabilidade Pn)", field_type="int", required=False, placeholder="opcional"),
        ],
    },
    "M/M/S/N": {
        "description": "Fila M/M/s com populacao finita N.",
        "fields": [
            InputField("lmbda", "Taxa de chegada (lambda)", placeholder="ex: 6"),
            InputField("mu", "Taxa de servico (mu)", placeholder="ex: 9"),
            InputField("s", "Numero de servidores (s)", field_type="int", placeholder="ex: 2"),
            InputField("N", "Tamanho da populacao (N)", field_type="int", placeholder="ex: 25"),
            InputField("n", "n (probabilidade Pn)", field_type="int", required=False, placeholder="opcional"),
        ],
    },
    "M/M/1/PPP": {
        "description": "Fila M/M/1 com prioridades preemptivas.",
        "fields": [
            InputField(
                "arrival_rates",
                "Taxas de chegada por prioridade",
                field_type="list_float",
                placeholder="ex: 2, 1.5, 0.3",
                help_text="Informe uma taxa por prioridade (1 = maior prioridade).",
            ),
            InputField("mu", "Taxa de servico (mu)", placeholder="ex: 12"),
        ],
    },
    "M/M/1/PNP": {
        "description": "Fila M/M/1 com prioridades nao preemptivas.",
        "fields": [
            InputField(
                "arrival_rates",
                "Taxas de chegada por prioridade",
                field_type="list_float",
                placeholder="ex: 3, 2, 0.5",
                help_text="Informe uma taxa por prioridade (1 = maior prioridade).",
            ),
            InputField("mu", "Taxa de servico (mu)", placeholder="ex: 10"),
        ],
    },
    "M/M/S/PPP": {
        "description": "Fila M/M/s com prioridades preemptivas.",
        "fields": [
            InputField(
                "arrival_rates",
                "Taxas de chegada por prioridade",
                field_type="list_float",
                placeholder="ex: 4, 3, 1",
                help_text="Separe as taxas com virgula ou nova linha.",
            ),
            InputField("mu", "Taxa de servico (mu)", placeholder="ex: 14"),
            InputField("s", "Numero de servidores (s)", field_type="int", placeholder="ex: 3"),
        ],
    },
    "M/M/S/PNP": {
        "description": "Fila M/M/s com prioridades nao preemptivas.",
        "fields": [
            InputField(
                "arrival_rates",
                "Taxas de chegada por prioridade",
                field_type="list_float",
                placeholder="ex: 4, 3, 1",
                help_text="Separe as taxas com virgula ou nova linha.",
            ),
            InputField("mu", "Taxa de servico (mu)", placeholder="ex: 14"),
            InputField("s", "Numero de servidores (s)", field_type="int", placeholder="ex: 3"),
        ],
    },
    "PRIORIDADE_PREEMPTIVA_3X3": {
        "description": "Modelo com prioridades com interrupcao (preemptivo), minimo 3 classes e ate 3 canais.",
        "fields": [
            InputField(
                "arrival_rates",
                "Taxas de chegada por prioridade (minimo 3)",
                field_type="list_float",
                placeholder="ex: 0.2, 0.6, 1.2",
                help_text="Informe ao menos tres taxas (classe 1 = maior prioridade).",
            ),
            InputField("mu", "Taxa de servico (mu)", placeholder="ex: 3"),
            InputField(
                "s",
                "Numero de servidores (1 a 3)",
                field_type="int",
                default=3,
                placeholder="ex: 3",
                help_text="Use entre 1 e 3 canais (exemplo da aula usa 3).",
            ),
        ],
    },
    "PRIORIDADE_NAO_PREEMPTIVA_3X3": {
        "description": "Modelo com prioridades sem interrupcao (nao preemptivo), minimo 3 classes e ate 3 canais.",
        "fields": [
            InputField(
                "arrival_rates",
                "Taxas de chegada por prioridade (minimo 3)",
                field_type="list_float",
                placeholder="ex: 0.2, 0.6, 1.2",
                help_text="Informe ao menos tres taxas (classe 1 = maior prioridade).",
            ),
            InputField("mu", "Taxa de servico (mu)", placeholder="ex: 3"),
            InputField(
                "s",
                "Numero de servidores (1 a 3)",
                field_type="int",
                default=3,
                placeholder="ex: 3",
                help_text="Use entre 1 e 3 canais (exemplo da aula usa 3).",
            ),
        ],
    },
    "M/G/1": {
        "description": "Fila M/G/1 (atendimento geral) com diferentes distribuicoes de servico.",
        "fields": [
            InputField("lmbda", "Taxa de chegada (lambda)", placeholder="ex: 5.5"),
            InputField("mu", "Taxa media de servico (mu)", placeholder="ex: 6"),
            InputField(
                "service_distribution",
                "Distribuicao do servico",
                field_type="select",
                options=["poisson", "exponential", "deterministic"],
                default="poisson",
                help_text="Controla a variancia usada no calculo (Poisson, Exponential ou Deterministic).",
            ),
        ],
    },
}


METRIC_LABELS: Dict[str, str] = {
    "rho": "Utilizacao (rho)",
    "p0": "Probabilidade de sistema vazio (P0)",
    "pn": "Probabilidade de n clientes (Pn)",
    "pn_distribution": "Probabilidades ate n (e >n)",
    "pK": "Probabilidade de capacidade cheia (PK)",
    "L": "Numero medio no sistema (L)",
    "Lq": "Numero medio na fila (Lq)",
    "W": "Tempo medio no sistema (W)",
    "Wq": "Tempo medio na fila (Wq)",
    "P(W>t)": "Probabilidade de W > t",
    "P(Wq>t)": "Probabilidade de Wq > t",
    "lambda_eff": "Taxa efetiva de chegada (lambda efetiva)",
    "service_in_progress": "Clientes em servico",
    "lambda_total": "Taxa total de chegada",
    "P(any_idle_server)": "Probabilidade de haver servidor ocioso",
    "L_operational": "Numero medio operando",
}

PROBABILITY_KEYS = {"p0", "pn", "pK", "P(W>t)", "P(Wq>t)", "P(any_idle_server)", "P(wait)"}
TIME_KEYS = {"W", "Wq"}


def render_field(field: InputField, model_key: str) -> Any:
    key = f"{model_key}_{field.name}"
    label = f"{field.label}{' *' if field.required else ''}"
    default_value = "" if field.default in (None, "", 0) else str(field.default)

    if field.field_type == "select":
        options = field.options or []
        if not options:
            return ""
        default = field.default if field.default else options[0]
        index = options.index(default) if default in options else 0
        return st.selectbox(label, options, index=index, help=field.help_text, key=key)

    if field.field_type == "list_float":
        return st.text_area(
            label,
            value=default_value,
            placeholder=field.placeholder or "",
            help=field.help_text,
            height=110,
            key=key,
        )

    return st.text_input(
        label,
        value=default_value,
        placeholder=field.placeholder or "",
        help=field.help_text,
        key=key,
    )


def parse_list_of_floats(raw_text: str) -> List[float]:
    cleaned = raw_text.replace(";", ",").replace("\n", ",")
    tokens = [part.strip() for part in cleaned.split(",")]
    values = []
    for token in tokens:
        if not token:
            continue
        values.append(float(token))
    if not values:
        raise ValueError("Informe pelo menos uma taxa de chegada para prioridades.")
    return values


def parse_params(raw_inputs: Dict[str, Any], fields: List[InputField]) -> Dict[str, Any]:
    params: Dict[str, Any] = {}
    errors: List[str] = []

    for field in fields:
        raw_value = raw_inputs.get(field.name)
        if field.field_type == "select":
            params[field.name] = raw_value
            continue

        text_value = (raw_value or "").strip()
        if not text_value:
            if field.required:
                errors.append(f"O campo '{field.label}' e obrigatorio.")
            continue

        try:
            if field.field_type == "float":
                params[field.name] = float(text_value)
            elif field.field_type == "int":
                params[field.name] = int(float(text_value))
            elif field.field_type == "list_float":
                params[field.name] = parse_list_of_floats(text_value)
            elif field.field_type == "string":
                params[field.name] = text_value
            else:
                params[field.name] = text_value
        except ValueError:
            errors.append(f"Valor invalido em '{field.label}'.")

    if errors:
        raise ValueError("\n".join(errors))

    return params


def format_result_value(key: str, value: Any) -> Any:
    def fmt_num(val: float) -> str:
        if val == 0:
            return "0"
        abs_val = abs(val)
        if abs_val < 1e-4 or abs_val >= 1e4:
            return f"{val:.3e}"
        return f"{val:.6f}"

    if isinstance(value, float):
        if key in TIME_KEYS:
            minutes = value * 60
            return f"{fmt_num(value)} h ({fmt_num(minutes)} min)"
        if key in PROBABILITY_KEYS:
            return f"{fmt_num(value)} ({value * 100:.4f} %)"
        return fmt_num(value)
    return value


def display_extra_sections(model_key: str, result: Dict[str, Any]) -> None:
    if model_key in ("M/M/1/K", "M/M/S/K"):
        lam_eff = result.get("lambda_eff")
        pK = result.get("pK")
        if lam_eff is not None and pK is not None and 0 <= pK < 1:
            lam_total = lam_eff / (1 - pK)
            lost_rate = lam_total * pK
            st.info(f"Chegadas perdidas por unidade de tempo: {lost_rate:.4f}")

    if model_key in ("M/M/1/N", "M/M/S/N"):
        L_oper = result.get("L_operational")
        idle = result.get("P(any_idle_server)")
        if L_oper is not None:
            st.info(f"Numero medio de unidades operacionais: {L_oper:.4f}")
        if idle is not None:
            st.info(f"Tempo com pelo menos um servidor ocioso: {idle:.6f} ({idle * 100:.4f} %)")


def display_results(model_key: str, result: Dict[str, Any]) -> None:
    st.success("Calculo concluido com sucesso.")

    scalar_items = {}
    nested_items = {}
    for key, value in result.items():
        if isinstance(value, (dict, list)):
            nested_items[key] = value
        else:
            scalar_items[key] = value

    if scalar_items:
        table_rows = [
            {"Metrica": METRIC_LABELS.get(key, key), "Valor": format_result_value(key, value)}
            for key, value in scalar_items.items()
        ]
        st.subheader("Resultados gerais")
        st.table(table_rows)

    if "per_class" in nested_items:
        st.subheader("Metricas por prioridade")
        st.dataframe(nested_items.pop("per_class"), use_container_width=True)

    if "pn_distribution" in nested_items:
        pn_dist = nested_items.pop("pn_distribution")
        dist_rows = [
            {"n": state, "Pn": format_result_value("pn", prob)} for state, prob in pn_dist.items()
        ]
        st.subheader(METRIC_LABELS.get("pn_distribution", "Distribuicao Pn"))
        st.table(dist_rows)

    for key, value in nested_items.items():
        st.subheader(METRIC_LABELS.get(key, key))
        st.json(value)

    display_extra_sections(model_key, result)


def show_calculator() -> None:
    st.title("Calculadora Interativa de Teoria das Filas")
    st.write("Selecione um modelo, forneça os parâmetros e visualize os principais indicadores.")

    available_models = [name for name in MODEL_MAP.keys() if name in MODEL_CONFIG]
    if not available_models:
        st.error("Nenhum modelo configurado para a interface.")
        return

    selected_model = st.radio("Modelo", available_models, index=0)
    config = MODEL_CONFIG[selected_model]
    if description := config.get("description"):
        st.info(description)

    with st.form("params_form"):
        st.subheader("Parâmetros de entrada")
        raw_inputs = {field.name: render_field(field, selected_model) for field in config["fields"]}
        submitted = st.form_submit_button("Calcular")

    if submitted:
        try:
            params = parse_params(raw_inputs, config["fields"])
            result = calculate(selected_model, **params)
        except Exception as exc:
            st.error(str(exc))
        else:
            display_results(selected_model, result)
