import sqlite3

def get_db():
    conn = sqlite3.connect("sports.db", check_same_thread=False)
    cursor = conn.cursor()
    
    # Tabla de usuarios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            is_admin BOOLEAN DEFAULT FALSE
        )
    """)
    
    # Tabla de canchas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fields (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            sport_type TEXT NOT NULL,
            price REAL NOT NULL,
            is_available BOOLEAN DEFAULT TRUE
        )
    """)
    
    # Tabla de reservas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            field_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            time_slot TEXT NOT NULL,
            FOREIGN KEY (field_id) REFERENCES fields(id)
        )
    """)
    
    # Crear admin por defecto (email: admin@admin.com, contraseña: admin)
    cursor.execute("SELECT 1 FROM users WHERE email = 'admin@admin.com'")
    if not cursor.fetchone():
        salt = secrets.token_hex(16)
        cursor.execute(
            "INSERT INTO users (email, password_hash, is_admin) VALUES (?, ?, ?)",
            ("admin@admin.com", hash_password("admin", salt), True)
        )
    
    conn.commit()
    return conn
