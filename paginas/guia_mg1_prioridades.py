import streamlit as st


def show_mg1_priority_guide() -> None:
    st.title("Guia M/G/1 e Prioridades")
    st.caption("Como escolher M/G/1, prioridade nao-preemptiva ou preemptiva diretamente do enunciado.")

    st.subheader("1) Quando usar M/G/1")
    st.markdown(
        """
- Apenas **1 servidor**.
- Chegada **Poisson**.
- Servico **nao exponencial**: deterministico, com variancia informada ou distribuicao geral.
- Exemplo (PDF): lambda = 0.2, mu = 0.25, sigma = 4 -> M/G/1.
"""
    )

    st.markdown("**Escolha no menu de servico:**")
    st.markdown(
        """
- Se o servico for fixo -> **deterministic**.
- Se for exponencial -> **exponential**.
- Se o enunciado traz sigma -> **general (G)**. Se o menu chamar de "poisson" mas significar geral, use essa opcao.
"""
    )

    st.markdown("**Nao use M/G/1 se:** houver mais de 1 servidor, capacidade K, populacao finita N ou prioridades.")

    st.divider()

    st.subheader("2) Prioridades nao-preemptivas (sem interrupcao)")
    st.markdown(
        """
- Normalmente **1 servidor**.
- **2 ou 3 classes** (ex.: primeira classe/economica; graves/estaveis).
- Chegada e servico **exponenciais**.
- Regra: prioridade maior passa na frente, **nao interrompe** quem esta em servico.
"""
    )

    st.markdown("**Entradas no software:** lista de lambdas por classe; mu; S (geralmente 1).")
    st.markdown("**Nao use se:** houver interrupcao, mais de 3 classes ou servico nao exponencial.")

    st.divider()

    st.subheader("3) Prioridades preemptivas (com interrupcao)")
    st.markdown(
        """
- Existem classes de prioridade.
- Quem tem prioridade **pode interromper** o atendimento em curso.
- Frases tipicas: "prioridade com interrupcao", "preemptivo", "classe 1 interrompe classe 2".
"""
    )

    st.markdown("**Entradas no software:** lista de lambdas (ex.: 0.2, 0.6, 1.2), mu exponencial, servidores (normalmente 1, ate 3).")
    st.markdown("**Nao use se:** o enunciado diz sem interrupcao, o servidor nao pode parar no meio ou o caso for M/G/1 ou com populacao finita.")

    st.divider()

    st.subheader("4) Linha final de raciocinio")
    st.markdown(
        """
- **M/G/1:** 1 servidor + servico nao exponencial (tem sigma ou tempo fixo).
- **Prioridade nao-preemptiva:** ha prioridades, ninguem e interrompido.
- **Prioridade preemptiva:** ha prioridades e atendimento pode ser interrompido.
- **Modelos basicos (M/M/1, M/M/s, M/M/1/K, M/M/1/N):** sem prioridade, servico exponencial.
"""
    )
