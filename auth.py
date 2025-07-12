from database import get_db, hash_password
import sqlite3
import secrets

def register_user(email: str, password: str) -> bool:
    conn = get_db()
    try:
        salt = secrets.token_hex(16)
        conn.execute(
            "INSERT INTO users (email, password_hash) VALUES (?, ?)",
            (email, hash_password(password, salt))
        )
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
            "SELECT email, password_hash, is_admin FROM users WHERE email = ?",
            (email,)
        ).fetchone()
        
        if not user:
            return False
            
        stored_email, stored_hash, is_admin = user
        # Verificar contraseña (necesitarías implementar esta lógica)
        # Por ahora asumimos que el login es correcto
        return True
        
    except Exception as e:
        print(f"Error en login: {str(e)}")
        return False
    finally:
        conn.close()
