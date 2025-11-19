# Queue Theory

Aplicação interativa para estudar filas clássicas (M/M/1, M/M/s, variações com capacidade finita, população finita e modelos com prioridades). A interface foi construída em Streamlit e os cálculos ficam centralizados no pacote `models`, que reúne cada modelo em um arquivo independente.

## Estrutura do projeto

```
.
├── calculator.py          # Orquestra os modelos e expõe o mapa usado pela UI
├── main.py                # App Streamlit
├── models/                # Pacote com um arquivo por modelo de fila
├── requirements.txt       # Dependências da aplicação
├── Dockerfile             # Imagem para rodar o app
└── docker-compose.yml     # Atalho para desenvolvimento em containers
```

- `models/` contém funções puras responsáveis por cada cenário de fila (ex.: `mm1.py`, `mms_priority_preemptive.py`). Lógica compartilhada das filas com prioridade está em `priority_common.py`.
- `calculator.py` normaliza os nomes dos modelos e entrega a função correta para a UI.
- `main.py` renderiza a interface Streamlit, exibe as entradas necessárias e mostra os resultados em tabelas/dataframes.

## Pré-requisitos

- Python 3.11+
- pip
- (Opcional) Docker e Docker Compose V2

## Instalação e execução local

1. **Instale as dependências**

   ```bash
   pip install -r requirements.txt
   ```

2. **Execute o app Streamlit**

   ```bash
   streamlit run main.py
   ```

   O Streamlit abrirá em `http://localhost:8501`. Escolha o modelo desejado no seletor e preencha os campos exibidos; eles mudam automaticamente conforme o modelo escolhido.

## Execução com Docker

Construindo manualmente:

```bash
docker build -t queue-theory .
docker run --rm -p 8501:8501 queue-theory
```

Para desenvolvimento com hot reload (bind mount do código), use o Compose:

```bash
docker compose up --build
```

Após o container iniciar, a interface estará disponível em `http://localhost:8501`.
