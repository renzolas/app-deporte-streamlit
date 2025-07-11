import streamlit as st
import sqlite3
import hashlib
import secrets
from datetime import datetime
from typing import Tuple, Optional

# ---------------------------
# CONFIGURACIÓN DE BASE DE DATOS
# ---------------------------

def init_user_db():
    """Inicializa la base de datos de usuarios"""
    conn = sqlite3.connect("reservas.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            nombre TEXT,
            telefono TEXT,
            es_admin BOOLEAN DEFAULT FALSE,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            verificado BOOLEAN DEFAULT FALSE
        )
    """)
    
    # Crear usuario admin por defecto si no existe
    cursor.execute("SELECT 1 FROM usuarios WHERE email = 'admin@cancha.com'")
    if not cursor.fetchone():
        salt = generar_salt()
        password_hash = hash_password("admin", salt)
        cursor.execute(
            """INSERT INTO usuarios 
            (email, password_hash, salt, nombre, es_admin, verificado) 
            VALUES (?, ?, ?, ?, ?, ?)""",
            ("admin@cancha.com", password_hash, salt, "Administrador", True, True)
        )
    
    conn.commit()
    return conn

# ---------------------------
# FUNCIONES DE SEGURIDAD
# ---------------------------

def generar_salt() -> str:
    """Genera un valor salt aleatorio seguro"""
    return secrets.token_hex(16)

def hash_password(password: str, salt: str) -> str:
    """Genera hash seguro de contraseña usando PBKDF2"""
    return hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000  # Número de iteraciones
    ).hex()

# ---------------------------
# FUNCIONES PRINCIPALES
# ---------------------------

def registrar_usuario(email: str, password: str, **kwargs) -> Tuple[bool, str]:
    """
    Registra un nuevo usuario con validaciones
    
    Args:
        email: Correo electrónico
        password: Contraseña en texto plano
        kwargs: Datos adicionales (nombre, teléfono)
    
    Returns:
        Tuple[bool, str]: (éxito, mensaje)
    """
    # Validaciones básicas
    if not email or "@" not in email:
        return False, "El email no es válido"
    
    if len(password) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres"
    
    conn = None
    try:
        conn = init_user_db()
        cursor = conn.cursor()
        
        # Verificar si el usuario ya existe
        cursor.execute("SELECT 1 FROM usuarios WHERE email = ?", (email,))
        if cursor.fetchone():
            return False, "Este email ya está registrado"
        
        # Crear usuario con seguridad
        salt = generar_salt()
        password_hash = hash_password(password, salt)
        
        cursor.execute(
            """INSERT INTO usuarios 
            (email, password_hash, salt, nombre, telefono, verificado) 
            VALUES (?, ?, ?, ?, ?, ?)""",
            (email, password_hash, salt, kwargs.get('nombre'), kwargs.get('telefono'), False)
        )
        
        conn.commit()
        return True, "Registro exitoso. Por favor inicia sesión."
        
    except sqlite3.Error as e:
        return False, f"Error en el registro: {str(e)}"
    finally:
        if conn:
            conn.close()

def login_usuario(email: str, password: str) -> bool:
    """
    Autentica un usuario con credenciales seguras
    
    Args:
        email: Correo electrónico
        password: Contraseña en texto plano
    
    Returns:
        bool: True si la autenticación es exitosa
    """
    if not email or not password:
        return False
    
    conn = None
    try:
        conn = init_user_db()
        cursor = conn.cursor()
        
        cursor.execute(
            """SELECT password_hash, salt, es_admin, verificado 
            FROM usuarios WHERE email = ?""", 
            (email,)
        )
        resultado = cursor.fetchone()
        
        if not resultado:
            return False
            
        stored_hash, salt, es_admin, verificado = resultado
        
        # Verificar contraseña
        input_hash = hash_password(password, salt)
        
        if secrets.compare_digest(input_hash, stored_hash):
            # Actualizar sesión
            st.session_state.update({
                "logueado": True,
                "email": email,
                "es_admin": es_admin,
                "verificado": verificado
            })
            return True
            
    except sqlite3.Error:
        return False
    finally:
        if conn:
            conn.close()
    
    return False

def obtener_info_usuario(email: str) -> Optional[Dict]:
    """
    Obtiene información del usuario desde la base de datos
    
    Args:
        email: Correo electrónico del usuario
    
    Returns:
        Dict: Información del usuario o None si no existe
    """
    conn = None
    try:
        conn = init_user_db()
        cursor = conn.cursor()
        
        cursor.execute(
            """SELECT email, nombre, telefono, fecha_registro, verificado 
            FROM usuarios WHERE email = ?""", 
            (email,)
        )
        resultado = cursor.fetchone()
        
        if resultado:
            return {
                "email": resultado[0],
                "nombre": resultado[1],
                "telefono": resultado[2],
                "fecha_registro": resultado[3],
                "verificado": resultado[4]
            }
            
    except sqlite3.Error:
        return None
    finally:
        if conn:
            conn.close()
    
    return None

def actualizar_usuario(email: str, **kwargs) -> Tuple[bool, str]:
    """
    Actualiza información del usuario
    
    Args:
        email: Correo electrónico del usuario
        kwargs: Campos a actualizar (nombre, teléfono)
    
    Returns:
        Tuple[bool, str]: (éxito, mensaje)
    """
    conn = None
    try:
        conn = init_user_db()
        cursor = conn.cursor()
        
        # Construir consulta dinámica
        campos = []
        valores = []
        
        if 'nombre' in kwargs:
            campos.append("nombre = ?")
            valores.append(kwargs['nombre'])
        
        if 'telefono' in kwargs:
            campos.append("telefono = ?")
            valores.append(kwargs['telefono'])
        
        if not campos:
            return False, "No hay datos para actualizar"
        
        valores.append(email)  # Para el WHERE
        
        query = f"UPDATE usuarios SET {', '.join(campos)} WHERE email = ?"
        cursor.execute(query, valores)
        
        conn.commit()
        return True, "Datos actualizados correctamente"
        
    except sqlite3.Error as e:
        return False, f"Error al actualizar: {str(e)}"
    finally:
        if conn:
            conn.close()

# ---------------------------
# FUNCIONES ADICIONALES
# ---------------------------

def listar_usuarios() -> List[Dict]:
    """Obtiene lista de todos los usuarios (solo admin)"""
    conn = None
    try:
        conn = init_user_db()
        cursor = conn.cursor()
        
        cursor.execute(
            """SELECT email, nombre, telefono, es_admin, fecha_registro, verificado 
            FROM usuarios ORDER BY fecha_registro DESC"""
        )
        
        return [
            {
                "email": row[0],
                "nombre": row[1],
                "telefono": row[2],
                "es_admin": row[3],
                "fecha_registro": row[4],
                "verificado": row[5]
            }
            for row in cursor.fetchall()
        ]
        
    except sqlite3.Error:
        return []
    finally:
        if conn:
            conn.close()

def cambiar_rol(email: str, es_admin: bool) -> Tuple[bool, str]:
    """Cambia el rol de un usuario (solo admin)"""
    conn = None
    try:
        conn = init_user_db()
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE usuarios SET es_admin = ? WHERE email = ?",
            (es_admin, email)
        )
        
        conn.commit()
        return True, f"Rol de {email} actualizado a {'admin' if es_admin else 'usuario'}"
        
    except sqlite3.Error as e:
        return False, f"Error al cambiar rol: {str(e)}"
    finally:
        if conn:
            conn.close()

