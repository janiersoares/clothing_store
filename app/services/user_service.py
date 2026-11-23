from app.repositories import user_repository
from app.security.passwords import hash_password


class EmailAlreadyExistsError(Exception):
    pass


def register_user(connection, email: str, password: str) -> dict:
    normalized_email = email.lower()

    existing_user = user_repository.get_user_by_email(connection, normalized_email)
    if existing_user is not None:
        raise EmailAlreadyExistsError("Email já cadastrado")

    password_hash = hash_password(password)
    return user_repository.create_user(connection, normalized_email, password_hash, "user")
