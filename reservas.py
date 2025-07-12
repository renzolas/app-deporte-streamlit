import streamlit as st
import sqlite3
from datetime import date, timedelta
from typing import List, Dict, Optional

# Horarios disponibles para reservas
HORARIOS = [
    "09:00 - 10:30", "10:30 - 12:00", "12:00 - 13:30",
    "13:30 - 15:00", "15:00 - 16:30", "16:30 - 18:00",
    "18:00 - 19:30", "19:30 - 21:00"
]

def init_db():
    """Inicializa la conexión a la base de datos"""
    conn = sqlite3.connect("reservas.db")
    
    # Crear tabla de reservas si no existe
    conn.execute("""
        CREATE TABLE IF NOT EXISTS reservas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            cancha_id INTEGER NOT NULL,
            dia TEXT NOT NULL,
            horario TEXT NOT NULL,
            precio REAL NOT NULL,
            fecha_reserva TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (cancha_id) REFERENCES canchas(id),
            UNIQUE(cancha_id, dia, horario)
        )
    """)
    conn.commit()
    return conn

def reservar_cancha():
    """Interfaz para realizar reservas de canchas"""
    st.subheader("📅 Nueva Reserva")
    
    # Verificar autenticación
    if not st.session_state.get("logueado"):
        st.warning("🔒 Debes iniciar sesión para reservar")
        return
    
    email_usuario = st.session_state["email"]
    st.markdown(f"👤 Usuario: {email_usuario}")
    
    # Obtener canchas disponibles
    try:
        conn = init_db()
        canchas = conn.execute("""
            SELECT id, nombre, deporte, precio 
            FROM canchas 
            WHERE disponible = TRUE
            ORDER BY nombre
        """).fetchall()
    except sqlite3.Error as e:
        st.error(f"Error al cargar canchas: {str(e)}")
        return
    finally:
        conn.close()
    
    if not canchas:
        st.info("🏟️ No hay canchas disponibles actualmente")
        return
    
    # Selección de cancha
    nombres_canchas = [f"{c[1]} ({c[2]} - ${c[3]}/hora)" for c in canchas]
    cancha_seleccionada = st.selectbox("Selecciona una cancha:", nombres_canchas)
    cancha_id = canchas[nombres_canchas.index(cancha_seleccionada)][0]
    
    # Selección de fecha
    hoy = date.today()
    dia = st.date_input(
        "Selecciona una fecha:",
        min_value=hoy,
        max_value=hoy + timedelta(days=30)
    
    # Mostrar horarios
    st.markdown("### 🕒 Horarios Disponibles")
    mostrar_horarios_disponibles(cancha_id, dia, email_usuario)

def mostrar_horarios_disponibles(cancha_id: int, dia: date, usuario: str):
    """Muestra los horarios disponibles en formato de grilla"""
    try:
        conn = init_db()
        
        # Obtener reservas existentes
        reservas = conn.execute("""
            SELECT horario FROM reservas 
            WHERE cancha_id = ? AND dia = ?
        """, (cancha_id, str(dia))).fetchall()
        
        horarios_ocupados = [r[0] for r in reservas]
        
        # Mostrar en columnas
        cols = st.columns(4)
        
        for i, horario in enumerate(HORARIOS):
            with cols[i % 4]:
                if horario in horarios_ocupados:
                    st.button(
                        f"❌ {horario}",
                        key=f"ocupado_{i}",
                        disabled=True,
                        help="Horario no disponible"
                    )
                else:
                    if st.button(f"✅ {horario}", key=f"disp_{i}"):
                        confirmar_reserva(conn, cancha_id, dia, horario, usuario)
        
    except sqlite3.Error as e:
        st.error(f"Error al ver horarios: {str(e)}")
    finally:
        conn.close()

def confirmar_reserva(conn, cancha_id: int, dia: date, horario: str, usuario: str):
    """Procesa la confirmación de una reserva"""
    try:
        # Obtener precio de la cancha
        precio = conn.execute("""
            SELECT precio FROM canchas WHERE id = ?
        """, (cancha_id,)).fetchone()[0]
        
        # Insertar reserva
        conn.execute("""
            INSERT INTO reservas (usuario, cancha_id, dia, horario, precio)
            VALUES (?, ?, ?, ?, ?)
        """, (usuario, cancha_id, str(dia), horario, precio))
        
        conn.commit()
        st.success(f"✅ Reserva confirmada para el {dia} a las {horario}")
        st.balloons()
        st.rerun()
        
    except sqlite3.IntegrityError:
        st.error("⚠️ Este horario ya fue reservado. Por favor selecciona otro.")
    except Exception as e:
        st.error(f"❌ Error al reservar: {str(e)}")

def ver_reservas():
    """Muestra las reservas según el tipo de usuario"""
    if not st.session_state.get("logueado"):
        st.warning("🔒 Debes iniciar sesión para ver reservas")
        return
    
    es_admin = st.session_state.get("es_admin", False)
    email = st.session_state["email"]
    
    try:
        conn = init_db()
        
        if es_admin:
            st.subheader("📋 Todas las Reservas")
            reservas = conn.execute("""
                SELECT r.id, r.usuario, c.nombre, c.deporte, r.dia, r.horario, r.precio, r.fecha_reserva
                FROM reservas r
                JOIN canchas c ON r.cancha_id = c.id
                ORDER BY r.dia DESC, r.horario DESC
            """).fetchall()
        else:
            st.subheader("📋 Mis Reservas")
            reservas = conn.execute("""
                SELECT r.id, r.usuario, c.nombre, c.deporte, r.dia, r.horario, r.precio, r.fecha_reserva
                FROM reservas r
                JOIN canchas c ON r.cancha_id = c.id
                WHERE r.usuario = ?
                ORDER BY r.dia DESC, r.horario DESC
            """, (email,)).fetchall()
        
        if not reservas:
            st.info("No hay reservas registradas")
            return
        
        # Mostrar cada reserva
        for r in reservas:
            with st.expander(f"{r[4]} - {r[2]} ({r[3]})"):
                st.markdown(f"""
                **🕒 Horario:** {r[5]}  
                **💲 Precio:** ${r[6]:.2f}  
                **📅 Fecha reserva:** {r[7][:16]}  
                {f"**👤 Usuario:** {r[1]}" if es_admin else ""}
                """)
                
                if st.button("❌ Cancelar", key=f"cancel_{r[0]}"):
                    conn.execute("DELETE FROM reservas WHERE id = ?", (r[0],))
                    conn.commit()
                    st.success("Reserva cancelada")
                    st.rerun()
                
    except sqlite3.Error as e:
        st.error(f"Error al cargar reservas: {str(e)}")
    finally:
        conn.close()



