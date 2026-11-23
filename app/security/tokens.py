import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv

load_dotenv()

ALGORITHM = "HS256"
TOKEN_EXPIRES_IN = timedelta(hours=1)


def create_access_token(user: dict) -> str:
    payload = {
        "sub": str(user["id"]),
        "email": user["email"],
        "role": user["role"],
        "exp": datetime.now(timezone.UTC) + TOKEN_EXPIRES_IN,
    }
    return jwt.encode(payload, os.environ["JWT_SECRET"], algorithm=ALGORITHM)