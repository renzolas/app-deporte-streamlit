import streamlit as st
from database import get_db
import hashlib
import secrets

def hash_password(password: str, salt: str) -> str:
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex()

def register_user(email: str, password: str) -> bool:
    conn = get_db()
    try:
        salt = secrets.token_hex(16)
        conn.execute(
            "INSERT INTO users (email, password_hash) VALUES (?, ?)",
            (email, hash_password(password, salt))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_user(email: str, password: str) -> bool:
    conn = get_db()
    try:
        user = conn.execute(
            "SELECT email, is_admin FROM users WHERE email = ?",
            (email,)).fetchone()
        
        if user:
            st.session_state.update({
                "email": user[0],
                "is_admin": user[1],
                "logged_in": True
            })
            return True
        return False
    finally:
        conn.close()
