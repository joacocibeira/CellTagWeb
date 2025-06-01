import streamlit as st
import sqlite3
import hashlib
import os

DB_PATH = os.getenv("AUTH_DB_PATH", "users.db")


def _get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def _create_users_table():
    with _get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password_hash TEXT NOT NULL
            )
        """
        )
        conn.commit()


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def _verify_credentials(username: str, password: str) -> bool:
    with _get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
        return row and row[0] == _hash_password(password)


def login_user():
    _create_users_table()

    st.title("🔐 Login")

    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        if _verify_credentials(username, password):
            st.session_state.user = username
            st.success(f"Bienvenido, {username}")
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos")


def get_current_user():
    return st.session_state.get("user")
