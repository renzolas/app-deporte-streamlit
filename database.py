import sqlite3

def get_db():
    """Retorna una conexión a la base de datos con todas las tablas necesarias"""
    conn = sqlite3.connect("sports.db", check_same_thread=False)
    
    # Crear tablas si no existen
    cursor = conn.cursor()
    
    # Tabla de usuarios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            is_admin BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
            user_id INTEGER NOT NULL,
            field_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            time_slot TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (field_id) REFERENCES fields(id),
            UNIQUE(field_id, date, time_slot)
        )
    """)
    
    # Crear usuario admin por defecto
    cursor.execute("SELECT 1 FROM users WHERE email = 'admin@sports.com'")
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO users (email, password_hash, is_admin) VALUES (?, ?, ?)",
            ("admin@sports.com", "hashed_password", True)
        )
    
    conn.commit()
    return conn
