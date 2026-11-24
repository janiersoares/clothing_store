import psycopg


def create_user(connection: psycopg.Connection, email: str, password_hash: str, role: str) -> dict:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO users (email, password_hash, role)
            VALUES (%s, %s, %s)
            RETURNING id, email, role
            """,
            (email, password_hash, role),
        )
        row = cursor.fetchone()
        connection.commit()
        return {"id": row[0], "email": row[1], "role": row[2]}


def get_user_by_email(connection: psycopg.Connection, email: str) -> dict | None:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, email, password_hash, role
            FROM users
            WHERE email = %s
            """,
            (email,),
        )
        row = cursor.fetchone()
        if row:
            return {"id": row[0], "email": row[1], "password_hash": row[2], "role": row[3]}
        return None
    
