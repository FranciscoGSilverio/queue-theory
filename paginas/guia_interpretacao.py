import streamlit as st


def show_interpretation_guide() -> None:
    st.title("Guia rapido: interpretar exercicios de filas")
    st.caption(
        "Explicacao direta para identificar o modelo e extrair lambda, mu, S, K e N para usar no software."
    )

    st.subheader("1. Como saber qual modelo usar?")
    st.markdown(
        """
**Olhe sempre duas coisas:**
- **Quantos servidores?** 1 -> M/M/1; 2 -> M/M/2; S atendentes -> M/M/s.
- **Capacidade maxima?** Se disser "comporta no maximo K clientes" -> M/M/s/K; se nada for dito -> K = infinito.
- **Populacao finita?** Se houver N itens fixos (maquinas, trens etc.) -> M/M/s/N.
- **Atendimento exponencial?** E o padrao. Se for diferente, o enunciado avisa (ex.: M/G/1).
"""
    )

    st.subheader("2. Entradas que o software pede")
    st.markdown(
        """
| Parametro | Significado | Como identificar |
| --- | --- | --- |
| **lambda** | taxa de chegada | "1 cliente a cada 30 min" -> lambda = 1/30 |
| **mu** | taxa de servico | "atende em 10 min" -> mu = 1/10 |
| **S** | numero de servidores | "duas pistas/atendentes" -> S = 2 |
| **K** | capacidade do sistema | "comporta no maximo 5 clientes" -> K = 5 |
| **N** | populacao finita | "existem 6 trens" -> N = 6 |
"""
    )

    st.subheader("3. Como interpretar lambda e mu na pratica")
    st.markdown(
        """
E sempre **1 dividido pelo tempo medio** (na mesma unidade: horas, minutos ou dias).

- Intervalo medio entre chegadas = 30 h -> lambda = 1/30.
- Tempo medio de atendimento = 6h40m (6,66 h) -> mu = 1/6,66.
"""
    )

    st.subheader("4. Como identificar N, K e S")
    st.markdown(
        """
- **N (populacao):** "mineradora abastece 6 trens" -> N = 6 -> M/M/1/N.
- **K (capacidade):** "comporta no maximo 5 pacientes" -> K = 5 -> M/M/1/K.
- **S (servidores):** "2 maquinas/pistas/tecnicos" -> S = 2 -> M/M/S (ou M/M/S/K ou M/M/S/N se houver limite ou populacao).
"""
    )

    st.subheader("5. Disciplina da fila (se importar)")
    st.markdown(
        """
- **FIFO**: padrao.
- **Prioridade sem interrupcao (non-preemptive)**: respeita o servico atual.
- **Prioridade com interrupcao (preemptive)**: quem chega com prioridade pode interromper.
"""
    )

    st.subheader("6. Passo a passo para ler o enunciado")
    st.markdown(
        """
1) Identifique o modelo: servidores? capacidade? populacao? prioridade?  
2) Ache **lambda**: "um cliente a cada X minutos" ou "Y clientes por hora" -> lambda = 1/tempo.  
3) Ache **mu**: "tempo medio de atendimento de 10 min" -> mu = 1/10.  
4) Ache **S, K, N**: atendentes? capacidade maxima? populacao fixa?  
5) Envie para o software conforme o modelo:
   - M/M/1 -> lambda, mu
   - M/M/1/K -> lambda, mu, K
   - M/M/s -> lambda, mu, S
   - M/M/s/K -> lambda, mu, S, K
   - M/M/1/N -> lambda, mu, N
"""
    )

    st.subheader("7. Tres exemplos rapidos")
    st.markdown(
        """
- **Populacao finita:** "6 trens... intervalo 30 h... servico 6h40m" -> lambda = 1/30; mu = 1/6,66; N = 6; S = 1 -> **M/M/1/N**.
- **Capacidade K:** "comporta no maximo 5 clientes" -> K = 5; S = 1 -> **M/M/1/K**.
- **Dois atendentes:** "duas pistas de pouso / 2 equipamentos" -> S = 2 -> **M/M/2** (ou **M/M/2/K** se houver limite).
"""
    )

    st.subheader("8. O segredo (5 perguntas)")
    st.markdown(
        """
1. Qual o tempo entre chegadas? -> lambda = 1/(tempo).  
2. Qual o tempo de atendimento? -> mu = 1/(tempo).  
3. Quantos atendentes existem? -> S.  
4. Existe capacidade maxima? -> K.  
5. A populacao de clientes e fixa? -> N.
"""
    )
