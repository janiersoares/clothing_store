import os

import psycopg
from dotenv import load_dotenv

from app.repositories import user_repository
from app.security.passwords import hash_password

load_dotenv()


def main() -> None:
    email = os.environ["ADMIN_EMAIL"].lower()
    password = os.environ["ADMIN_PASSWORD"]

    with psycopg.connect(os.environ["DATABASE_URL"]) as connection:
        if user_repository.get_user_by_email(connection, email) is not None:
            print("Admin already exist.")
            return

        user_repository.create_user(connection, email, hash_password(password), "admin")
        print("Admin created.")


if __name__ == "__main__":
    main()

    