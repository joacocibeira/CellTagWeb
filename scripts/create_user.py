# scripts/create_user.py

import sqlite3
import hashlib
import argparse
import os

DB_PATH = "./data/auth/users.db"


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="Username to create")
    parser.add_argument("password", help="Password for the user")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL
        )
    """
    )
    try:
        conn.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (args.username, hash_password(args.password)),
        )
        conn.commit()
        print(f"✅ User '{args.username}' created.")
    except sqlite3.IntegrityError:
        print(f"⚠️ User '{args.username}' already exists.")
    conn.close()
