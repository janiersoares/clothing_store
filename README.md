# Loja de Roupas — API

API de uma loja de roupas com autenticação, catálogo, carrinho e checkout.

**Stack:** Python, FastAPI, PostgreSQL (Neon), psycopg, bcrypt, PyJWT, pytest.

## Como rodar

1. Clone o repositório e entre na pasta do projeto.
2. Crie e ative o ambiente virtual:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

3. Instale as dependências:

```powershell
python -m pip install -r requirements.txt
```

4. Crie o arquivo `.env` a partir do `.env.example` e preencha os valores reais: `DATABASE_URL`, `JWT_SECRET`, `ADMIN_EMAIL` e `ADMIN_PASSWORD`.

5. Aplique as migrations no banco:

```powershell
python migrate.py
```

6. Crie o administrador inicial:

```powershell
python seed_admin.py
```

7. Suba a API:

```powershell
uvicorn app.main:app --reload
```

8. Abra a documentação interativa em `http://127.0.0.1:8000/docs`.

9. Rode os testes:

```powershell
python -m pytest -v
```

## Rotas

### Fase 1: autenticação

| Método | Rota             | Descrição                                      |
|--------|------------------|------------------------------------------------|
| GET    | `/health`        | Verifica se a API está no ar                   |
| POST   | `/auth/register` | Cria um usuário com papel `user`               |
| POST   | `/auth/login`    | Retorna um token JWT com o papel do usuário    |

- O admin não é criado por API. Ele nasce pelo `seed_admin.py`.
- O papel nunca é aceito do cliente no cadastro.
- E-mails são salvos em minúsculas.
- Senhas são guardadas apenas como hash bcrypt.

## Estrutura

- `app/routes`: recebe as requisições e devolve as respostas.
- `app/services`: aplica as regras de negócio.
- `app/repositories`: faz as consultas SQL.
- `app/security`: hash de senha e tokens JWT.
- `app/schemas`: formato dos dados de entrada e saída.
- `migrations`: alterações do banco, numeradas.
- `tests`: testes automatizados.