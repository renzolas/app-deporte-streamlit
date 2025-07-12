import sqlite3
import secrets
import hashlib

def hash_password(password: str, salt: str) -> str:
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex()

def get_db():
    conn = sqlite3.connect("sports.db", check_same_thread=False)
    cursor = conn.cursor()
    
    # Tabla usuarios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            is_admin BOOLEAN DEFAULT FALSE
        )
    """)
    
    # Tabla canchas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fields (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            sport_type TEXT NOT NULL,
            price REAL NOT NULL,
            is_available BOOLEAN DEFAULT TRUE
        )
    """)
    
    # Tabla reservas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            field_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            time_slot TEXT NOT NULL
        )
    """)
    
    # Crear admin por defecto si no existe
    cursor.execute("SELECT 1 FROM users WHERE email = 'admin@admin.com'")
    if not cursor.fetchone():
        salt = secrets.token_hex(16)
        cursor.execute(
            "INSERT INTO users (email, password_hash, is_admin) VALUES (?, ?, ?)",
            ("admin@admin.com", hash_password("admin", salt), True)
        )
    
    conn.commit()
    return conn
