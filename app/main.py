from fastapi import FastAPI

from app.routes import auth

app = FastAPI(title="Loja de Roupas")

app.include_router(auth.router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}