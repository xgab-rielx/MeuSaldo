# MeuSaldo

MeuSaldo é um aplicativo web para controle de gastos pessoais, desenvolvido com FastAPI, SQLite e uma interface responsiva. Cada conta acessa apenas os próprios gastos.

O projeto permite cadastrar, listar, editar e excluir gastos, além de filtrar por período e categoria e consultar o total gasto em um mês.

## Funcionalidades

- Cadastro de gastos com descrição, valor, data e categoria
- Listagem de gastos
- Consulta de um gasto por ID
- Edição de gastos
- Exclusão de gastos
- Filtro por período e categoria
- Consulta do total gasto em um mês
- Interface web para cadastrar, listar, editar e excluir gastos
- Interface para filtrar por período e categoria e consultar o total mensal
- Login e logout com sessão
- Isolamento dos gastos por usuário

## Tecnologias

- Python
- FastAPI
- SQLite
- Pydantic
- pwdlib com Argon2 para armazenar senhas com hash
- Starlette SessionMiddleware para sessões
- HTML, CSS e JavaScript

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

4. Configure uma chave secreta para as sessões. No PowerShell, gere uma chave aleatória na mesma janela em que executará o servidor:

```powershell
$env:SESSION_SECRET = python -c "import secrets; print(secrets.token_urlsafe(32))"
```

No Linux ou macOS:

```bash
export SESSION_SECRET="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
```

Essa variável vale para a sessão atual do terminal. Se fechar o terminal, configure-a novamente antes de iniciar a aplicação. Não coloque a chave no código nem a envie ao GitHub.

5. Execute o servidor:

```bash
uvicorn main:app --reload
```

6. Acesse a documentação interativa:

```text
http://127.0.0.1:8000/docs
```

7. Acesse a interface web:

```text
http://127.0.0.1:8000/app
```

## Endpoints

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/login` | Inicia uma sessão com usuário e senha |
| `POST` | `/logout` | Encerra a sessão atual |
| `GET` | `/session` | Verifica se há uma sessão ativa |
| `POST` | `/spendings` | Cadastra um gasto da conta conectada |
| `GET` | `/spendings` | Lista os gastos da conta, com filtros opcionais |
| `GET` | `/spendings/monthly_total` | Retorna o total mensal da conta conectada |
| `GET` | `/spendings/{spending_id}` | Busca um gasto da conta pelo ID |
| `PUT` | `/spendings/{spending_id}` | Atualiza um gasto da conta |
| `DELETE` | `/spendings/{spending_id}` | Remove um gasto da conta |

As rotas de gastos exigem login. O `user_id` é obtido da sessão, e não de um valor enviado pelo navegador.

## Criar uma conta

Não há cadastro público. Para criar uma conta localmente, inicie a aplicação ao menos uma vez para criar o banco de dados. Com o ambiente virtual ativado, abra outro terminal na pasta do projeto e inicie o Python:

```bash
python
```

No console interativo, execute:

```python
from getpass import getpass
from database import create_user
from security import hash_password

username = input("Usuário: ")
password = getpass("Senha: ")
user_id = create_user(username, hash_password(password))
print(f"Conta criada com ID {user_id}")
```

`getpass` não exibe a senha enquanto você digita. O banco guarda o hash da senha, não a senha original. Para sair do console, digite `exit()`.

## Filtros na listagem

A rota `GET /spendings` exige uma sessão ativa e aceita os seguintes parâmetros opcionais:

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

O total considera apenas os gastos da conta conectada.

## Estrutura do projeto

```text
MeuSaldo/
├── main.py        # Rotas da API
├── database.py    # Conexão e operações SQL
├── models.py      # Modelos Pydantic
├── security.py    # Hash e verificação de senhas
├── requirements.txt
└── static/        # Interface web (HTML, CSS e JavaScript)
```

## Próximas etapas

- Backup automático
- Publicação com HTTPS, chave de sessão configurada no servidor e armazenamento persistente do banco de dados
