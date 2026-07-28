import sqlite3
import hashlib


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(username, password):

    if len(password) < 8:
        return "Password must be at least 8 characters long."

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users(username, password) VALUES(?, ?)",
            (username, hash_password(password))
        )
        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return "Username already exists."

    finally:
        conn.close()


def login_user(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, hash_password(password))
    )

    user = cursor.fetchone()
    conn.close()

    return user
