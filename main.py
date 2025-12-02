import streamlit as st

from paginas.calculadora import show_calculator
from paginas.guia_mg1_prioridades import show_mg1_priority_guide
from paginas.guia_interpretacao import show_interpretation_guide
from paginas.teoria import show_theory


st.set_page_config(page_title="Teoria das Filas", page_icon="📈", layout="wide")


def main() -> None:
    st.sidebar.title("Menu")
    page = st.sidebar.radio(
        "Selecione uma página",
        [
            "Calculadora",
            "Conteúdo Teórico",
            "Guia rápido (lambda, mu, S, K, N)",
            "Guia M/G/1 e Prioridades",
        ],
    )

    if page == "Calculadora":
        show_calculator()
    elif page == "Conteúdo Teórico":
        show_theory()
    elif page == "Guia rápido (lambda, mu, S, K, N)":
        show_interpretation_guide()
    elif page == "Guia M/G/1 e Prioridades":
        show_mg1_priority_guide()


if __name__ == "__main__":
    main()
