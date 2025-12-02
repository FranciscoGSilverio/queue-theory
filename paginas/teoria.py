import streamlit as st


def show_home_content():
    st.header("Página Inicial e Conceitos Fundamentais")

    st.markdown("""
    A **Teoria das Filas** é um campo da Pesquisa Operacional que estuda a formação e o comportamento de filas. Ela nos ajuda a encontrar um equilíbrio ideal entre o **custo do serviço** e o **custo da espera**.
    
    O objetivo é dimensionar a capacidade do sistema para minimizar o custo total:
    $$ Custo Total = Custo do Serviço + Custo da Espera $$
    """)
    
    st.info("Exemplos: Caixas de supermercado, pedágios, servidores de banco de dados, triagem hospitalar.")

    st.subheader("Os 3 Pilares da Teoria das Filas")
    st.markdown(r"""
    Todo sistema de filas pode ser descrito por três componentes básicos:

    1.  **Processo de Chegada (A):**
        - Descreve como os clientes chegam ao sistema.
        - **$\lambda$ (Lambda):** Taxa média de chegada (clientes por unidade de tempo).
        - **$1/\lambda$:** Tempo médio entre chegadas.
        - Geralmente assume-se uma distribuição de Poisson para as chegadas (tempos entre chegadas exponenciais).

    2.  **Processo de Atendimento (B):**
        - Descreve quanto tempo leva para atender um cliente.
        - **$\mu$ (Mi):** Taxa média de serviço por servidor (clientes atendidos por unidade de tempo).
        - **$1/\mu$:** Tempo médio de serviço.
        - Frequentemente assume-se distribuição Exponencial para os tempos de serviço.

    3.  **Disciplina da Fila e Servidores (s):**
        - **$s$:** Número de servidores paralelos.
        - **Disciplina:** Regra de atendimento (FIFO - First In First Out, LIFO - Last In First Out, PRI - Prioridade, GD - General Discipline).
    """)

    st.subheader("Lei de Little")
    st.markdown(r"""
    Uma das leis mais fundamentais e robustas da teoria das filas. Ela relaciona o número médio de itens no sistema ($L$) com a taxa de chegada ($\lambda$) e o tempo médio no sistema ($W$).
    
    $$ L = \lambda \cdot W $$
    
    Da mesma forma, para a fila:
    $$ L_q = \lambda \cdot W_q $$
    """)

    st.subheader("Notação de Kendall")
    st.markdown("A notação padrão **A/B/s/K/N/D** resume as características do sistema:")
    
    st.markdown("""
    | Símbolo | Significado | Opções Comuns |
    |:---:|---|---|
    | **A** | Distribuição das Chegadas | **M** (Markov/Exponencial), **D** (Determinística), **G** (Geral), **$E_k$** (Erlang) |
    | **B** | Distribuição do Serviço | **M** (Markov/Exponencial), **D** (Determinística), **G** (Geral) |
    | **s** | Número de Servidores | 1, 2, 3, ..., $\infty$ |
    | **K** | Capacidade do Sistema | Inteiro (se omitido = $\infty$) |
    | **N** | Tamanho da População | Inteiro (se omitido = $\infty$) |
    | **D** | Disciplina da Fila | FIFO, LIFO, SIRO, PRI (se omitido = FIFO) |
    """)
    
    st.markdown(
        """
        Custo total = Custo de operação (reais/hora) * L (número médio no sistema) + Custo de atendimento (reais por hora) * S (número de servidores)
        """
    )


def show_basic_models_content():
    st.header("Modelos Básicos: M/M/1 e M/M/s")

    st.subheader("O Modelo M/M/1")
    st.markdown(r"""
    **Características:**
    - Chegadas de Poisson ($\lambda$).
    - Tempos de serviço Exponenciais ($\mu$).
    - 1 Servidor.
    - População e Capacidade Infinitas.
    
    **Condição de Estabilidade:** $\lambda < \mu$ ou $\rho < 1$.
    """)

    st.markdown("### Fórmulas M/M/1")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Fator de Utilização ($\rho$):**")
        st.latex(r"\rho = \frac{\lambda}{\mu}")
        
        st.markdown("**Probabilidade de zero clientes ($P_0$):**")
        st.latex(r"P_0 = 1 - \rho")
        
        st.markdown("**Probabilidade de $n$ clientes ($P_n$):**")
        st.latex(r"P_n = (1 - \rho)\rho^n")

    with col2:
        st.markdown("**Número médio no sistema ($L$):**")
        st.latex(r"L = \frac{\lambda}{\mu - \lambda} = \frac{\rho}{1-\rho}")
        
        st.markdown("**Número médio na fila ($L_q$):**")
        st.latex(r"L_q = L - \rho = \frac{\rho^2}{1-\rho}")
        
        st.markdown("**Tempo médio no sistema ($W$):**")
        st.latex(r"W = \frac{1}{\mu - \lambda} = \frac{L}{\lambda}")

        st.markdown("**Tempo médio na fila ($W_q$):**")
        st.latex(r"W_q = \frac{\rho}{\mu - \lambda} = W - \frac{1}{\mu}")

    st.divider()

    st.subheader("O Modelo M/M/s")
    st.markdown(r"""
    **Características:**
    - Múltiplos servidores ($s$).
    - Fila única para todos os servidores.
    - O primeiro servidor livre atende o próximo da fila.
    
    **Condição de Estabilidade:** $\lambda < s\mu$ ou $\rho = \frac{\lambda}{s\mu} < 1$.
    """)

    st.markdown("### Fórmulas M/M/s")
    
    st.markdown("**Probabilidade de sistema vazio ($P_0$):**")
    st.latex(r"P_0 = \left[ \sum_{n=0}^{s-1} \frac{(\lambda/\mu)^n}{n!} + \frac{(\lambda/\mu)^s}{s!(1-\rho)} \right]^{-1}")
    
    st.markdown("**Probabilidade de espera (Erlang C):**")
    st.markdown("Probabilidade de um cliente chegar e ter que esperar (todos servidores ocupados).")
    st.latex(r"P(Wait) = P(n \ge s) = \frac{(\lambda/\mu)^s}{s!(1-\rho)} P_0")
    
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("**Número médio na fila ($L_q$):**")
        st.latex(r"L_q = \frac{P(Wait) \cdot \rho}{1-\rho}")
        
        st.markdown("**Número médio no sistema ($L$):**")
        st.latex(r"L = L_q + \frac{\lambda}{\mu}")

    with col4:
        st.markdown("**Tempo médio na fila ($W_q$):**")
        st.latex(r"W_q = \frac{L_q}{\lambda}")
        
        st.markdown("**Tempo médio no sistema ($W$):**")
        st.latex(r"W = W_q + \frac{1}{\mu}")


def show_real_limitations_content():
    st.header("Modelos com Limitações do Mundo Real")
    st.markdown("Os modelos básicos assumem capacidade e população infinitas. Na prática, isso nem sempre é verdade.")

    st.subheader("M/M/s/K: Capacidade Finita do Sistema")
    st.markdown("""
    **Características:**
    - Capacidade máxima do sistema = $K$ (fila + serviço).
    - Se o sistema está cheio (K clientes), novos clientes são recusados (perda).
    
    **Importante:** O sistema é sempre estável para qualquer $\lambda$ e $\mu$, pois a fila não pode crescer indefinidamente.
    """)
    
    st.markdown("### Fórmulas M/M/s/K")
    
    st.markdown("**Probabilidade de sistema cheio ($P_K$):**")
    st.latex(r"P_K = \frac{(\lambda/\mu)^K / K!}{\sum_{n=0}^{K} (\lambda/\mu)^n / n!} \quad \text{(para s=1)}")
    
    st.markdown("**Taxa Efetiva de Chegada ($\lambda_{eff}$):**")
    st.markdown("Apenas clientes que entram no sistema contam para os cálculos de média.")
    st.latex(r"\lambda_{eff} = \lambda (1 - P_K)")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Número médio no sistema ($L$):**")
        st.latex(r"L = \sum_{n=0}^{K} n \cdot P_n")
        
        st.markdown("**Número médio na fila ($L_q$):**")
        st.latex(r"L_q = L - \frac{\lambda_{eff}}{\mu}")

    with col2:
        st.markdown("**Tempo médio no sistema ($W$):**")
        st.latex(r"W = \frac{L}{\lambda_{eff}}")
        
        st.markdown("**Tempo médio na fila ($W_q$):**")
        st.latex(r"W_q = \frac{L_q}{\lambda_{eff}}")

    st.divider()

    st.subheader("M/M/s/N: População Finita (Fonte Finita)")
    st.markdown("""
    **Características:**
    - População total de potenciais clientes é $N$.
    - A taxa de chegada depende do número de clientes já no sistema.
    - Se $n$ clientes estão no sistema, apenas $N-n$ podem chegar.
    - Taxa de chegada no estado $n$: $\lambda_n = (N-n)\lambda$.
    """)
    
    st.markdown("### Fórmulas M/M/s/N")
    
    st.markdown("**Probabilidade de sistema vazio ($P_0$):**")
    st.latex(r"P_0 = \left[ \sum_{n=0}^{N} \binom{N}{n} (\lambda/\mu)^n \right]^{-1} \quad \text{(para s=1)}")
    
    st.markdown("**Probabilidade de $n$ clientes ($P_n$):**")
    st.latex(r"P_n = \binom{N}{n} (\lambda/\mu)^n P_0 \quad \text{(para s=1)}")
    
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("**Número médio no sistema ($L$):**")
        st.latex(r"L = N - \frac{\mu(1-P_0)}{\lambda}")
        
        st.markdown("**Número médio na fila ($L_q$):**")
        st.latex(r"L_q = N - \frac{\lambda + \mu(1-P_0)}{\lambda}")

    with col4:
        st.markdown("**Tempo médio no sistema ($W$):**")
        st.latex(r"W = \frac{L}{\lambda(N-L)}")
        
        st.markdown("**Tempo médio na fila ($W_q$):**")
        st.latex(r"W_q = \frac{L_q}{\lambda(N-L)}")


def show_advanced_models_content():
    st.header("Modelos Avançados")

    st.subheader("M/G/1: Tempos de Serviço Gerais")
    st.markdown(r"""
    **Características:**
    - Chegadas de Poisson ($\lambda$).
    - Tempos de serviço com distribuição Geral (média $1/\mu$, variância $\sigma^2$).
    - 1 Servidor.
    
    **Fórmula de Pollaczek-Khintchine (P-K):**
    Esta fórmula fundamental mostra como a variabilidade afeta a fila.
    """)
    
    st.latex(r"L_q = \frac{\lambda^2 \sigma^2 + \rho^2}{2(1 - \rho)}")
    st.latex(r"W_q = \frac{\lambda^2 \sigma^2 + \rho^2}{2\lambda(1 - \rho)}")
    
    st.info(r"""
    **Interpretação:**
    - Se $\sigma^2 = 0$ (Determinístico, M/D/1), a fila é metade da fila do M/M/1.
    - Se $\sigma^2$ é grande, a fila explode mesmo com $\rho$ baixo.
    - **Conclusão:** Reduzir a variabilidade é tão importante quanto aumentar a velocidade!
    """)

    st.divider()

    st.subheader("Modelos com Prioridades")
    st.markdown("""
    Sistemas onde certas classes de clientes têm preferência sobre outras.
    Suponha $k$ classes de prioridade ($1, 2, ..., k$), onde 1 é a maior prioridade.
    """)

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Prioridade Não Preemptiva")
        st.markdown("""
        - O serviço em andamento **não** é interrompido.
        - O cliente prioritário espera o serviço atual terminar e então "fura a fila".
        """)
        st.markdown("**Tempo médio de espera para classe $k$ ($W_{q,k}$):**")
        st.latex(r"W_{q,k} = \frac{\sum_{i=1}^{k} \lambda_i / \mu_i^2}{2(1 - \sigma_{k-1})(1 - \sigma_k)}")
        st.caption("Onde $\sigma_k = \sum_{i=1}^{k} \rho_i$")

    with col2:
        st.markdown("### Prioridade Preemptiva")
        st.markdown("""
        - O serviço em andamento **é interrompido** se chegar alguém mais importante.
        - O cliente de baixa prioridade volta para a fila (ou espera ao lado).
        """)
        st.markdown("**Vantagem:**")
        st.markdown("Clientes VIP quase não esperam, como se o sistema fosse só deles.")
        st.markdown("**Desvantagem:**")
        st.markdown("Clientes de baixa prioridade podem sofrer 'starvation' (nunca serem atendidos).")


def show_theory():
    st.title("Conteúdo Teórico sobre Teoria das Filas")
    
    PAGES = {
        "Início e Conceitos": show_home_content,
        "Modelos Básicos (M/M/1 e M/M/s)": show_basic_models_content,
        "Limitações Reais (K e N)": show_real_limitations_content,
        "Avançados (M/G/1 e Prioridades)": show_advanced_models_content,
    }

    selection = st.radio("Selecione o tópico para aprender", list(PAGES.keys()))
    page_function = PAGES[selection]
    with st.container(border=True):
        page_function()
