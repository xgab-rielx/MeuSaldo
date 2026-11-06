# MeuSaldo

MeuSaldo é uma API local para controle de gastos pessoais, desenvolvida com FastAPI e SQLite.

O projeto permite cadastrar, listar, editar e excluir gastos, além de filtrar por período e categoria e consultar o total gasto em um mês.

## Funcionalidades

- Cadastro de gastos com descrição, valor, data e categoria
- Listagem de gastos
- Consulta de um gasto por ID
- Edição de gastos
- Exclusão de gastos
- Filtro por período e categoria
- Consulta do total gasto em um mês

## Tecnologias

- Python
- FastAPI
- SQLite
- Pydantic

## Como executar

1. Clone o repositório:

```bash
git clone https://github.com/xgab-rielx/MeuSaldo.git
cd MeuSaldo
```

2. Crie e ative um ambiente virtual:

```bash
python -m venv .venv
```

No Windows:

```bash
.venv\Scripts\activate
```

No Linux ou macOS:

```bash
source .venv/bin/activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Execute o servidor:

```bash
uvicorn main:app --reload
```

5. Acesse a documentação interativa:

```text
http://127.0.0.1:8000/docs
```

## Endpoints

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/` | Verifica que a API está no ar |
| `POST` | `/spendings` | Cadastra um gasto |
| `GET` | `/spendings` | Lista gastos, com filtros opcionais |
| `GET` | `/spendings/monthly_total` | Retorna o total gasto em um mês |
| `GET` | `/spendings/{spending_id}` | Busca um gasto pelo ID |
| `PUT` | `/spendings/{spending_id}` | Atualiza um gasto |
| `DELETE` | `/spendings/{spending_id}` | Remove um gasto |

## Filtros na listagem

A rota `GET /spendings` aceita os seguintes parâmetros opcionais:

- `start_date`: data inicial, no formato `YYYY-MM-DD`
- `end_date`: data final, no formato `YYYY-MM-DD`
- `category`: categoria exata do gasto

Exemplo:

```text
GET /spendings?start_date=2026-11-01&end_date=2026-11-30&category=alimentacao
```

## Total mensal

Exemplo:

```text
GET /spendings/monthly_total?year=2026&month=11
```

## Estrutura do projeto

```text
MeuSaldo/
├── main.py        # Rotas da API
├── database.py    # Conexão e operações SQL
├── models.py      # Modelos Pydantic
└── requirements.txt
```

## Próximos passos

- Interface web responsiva
- Autenticação
- Backup automático
- Publicação para uso pessoal