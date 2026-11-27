# Clothing Store API

API for a clothing store with authentication, catalog, cart and checkout.

**Stack:** Python, FastAPI, PostgreSQL (Neon), psycopg, bcrypt, PyJWT, pytest.

## How to run

1. Clone the repository and enter the project folder.
2. Create and activate the virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

3. Install the dependencies:

```powershell
python -m pip install -r requirements.txt
```

4. Create `.env` from `.env.example` and fill in the real values: `DATABASE_URL`, `JWT_SECRET`, `ADMIN_EMAIL` and `ADMIN_PASSWORD`.

5. Apply the migrations:

```powershell
python migrate.py
```

6. Create the initial admin:

```powershell
python seed_admin.py
```

7. Start the API:

```powershell
uvicorn app.main:app --reload
```

8. Open the interactive docs at `http://127.0.0.1:8000/docs`.

9. Run the tests:

```powershell
python -m pytest -v
```

## Routes

### Phase 1: authentication

| Method | Route            | Description                             |
|--------|------------------|-----------------------------------------|
| GET    | `/health`        | Checks if the API is running            |
| POST   | `/auth/register` | Creates a user with the `user` role     |
| POST   | `/auth/login`    | Returns a JWT token with the user role  |

- The admin is not created through the API. It is created by `seed_admin.py`.
- The role is never accepted from the client on registration.
- Emails are stored in lowercase.
- Passwords are stored only as bcrypt hashes.
- Passwords longer than 72 bytes are rejected with status 422.

## Structure

- `app/routes`: receives requests and returns responses.
- `app/services`: applies the business rules.
- `app/repositories`: runs the SQL queries.
- `app/security`: password hashing and JWT tokens.
- `app/schemas`: format of input and output data.
- `migrations`: numbered database changes.
- `tests`: automated tests.

## Language

All code, messages, commits, pull requests and documentation are in English.