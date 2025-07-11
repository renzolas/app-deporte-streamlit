import streamlit as st
import sqlite3
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional

# ---------------------------
# CONFIGURACIÓN INICIAL
# ---------------------------

# Horarios disponibles para reservas
HORARIOS = [
    "09:00 - 10:30", "10:30 - 12:00", "12:00 - 13:30",
    "13:30 - 15:00", "15:00 - 16:30", "16:30 - 18:00",
    "18:00 - 19:30", "19:30 - 21:00"
]

def init_db():
    """Inicializa la conexión a la base de datos"""
    conn = sqlite3.connect("reservas.db")
    return conn

# ---------------------------
# FUNCIONES PRINCIPALES
# ---------------------------

def reservar_cancha():
    """Interfaz para realizar reservas de canchas"""
    st.subheader("📅 Nueva Reserva")
    
    # Verificar autenticación
    if not st.session_state.get("logueado"):
        st.warning("🔒 Debes iniciar sesión para reservar")
        return
    
    email_usuario = st.session_state["email"]
    st.markdown(f"👤 **Usuario:** {email_usuario}")
    
    # Obtener canchas disponibles
    conn = init_db()
    canchas = conn.execute("""
        SELECT id, nombre, deporte, precio 
        FROM canchas 
        WHERE disponible = TRUE
        ORDER BY nombre
    """).fetchall()
    conn.close()
    
    if not canchas:
        st.info("🏟️ No hay canchas disponibles actualmente")
        return
    
    # Selección de cancha y fecha
    nombres_canchas = [f"{c[1]} ({c[2]} - ${c[3]}/hora)" for c in canchas]
    cancha_seleccionada = st.selectbox("Seleccione cancha:", nombres_canchas)
    
    # Extraer ID de la cancha seleccionada
    cancha_id = canchas[nombres_canchas.index(cancha_seleccionada)][0]
    
    # Selección de fecha con restricciones
    hoy = date.today()
    max_fecha = hoy + timedelta(days=30)
    dia = st.date_input(
        "Seleccione fecha:",
        min_value=hoy,
        max_value=max_fecha,
        value=hoy
    )
    
    # Mostrar horarios disponibles
    st.markdown("### 🕒 Horarios Disponibles")
    mostrar_horarios_disponibles(cancha_id, dia, email_usuario)

def mostrar_horarios_disponibles(cancha_id: int, dia: date, usuario: str):
    """Muestra los horarios disponibles en formato de grilla"""
    conn = init_db()
    
    # Obtener reservas existentes para esta cancha y fecha
    reservas = conn.execute("""
        SELECT horario FROM reservas 
        WHERE cancha_id = ? AND dia = ?
    """, (cancha_id, str(dia))).fetchall()
    
    horarios_ocupados = [r[0] for r in reservas]
    
    # Mostrar horarios en columnas
    cols = st.columns(4)  # 4 columnas para mejor visualización
    
    for i, horario in enumerate(HORARIOS):
        with cols[i % 4]:
            if horario in horarios_ocupados:
                st.button(
                    f"❌ {horario}",
                    key=f"ocupado_{i}",
                    disabled=True,
                    help="Horario ya reservado"
                )
            else:
                if st.button(f"✅ {horario}", key=f"disp_{i}"):
                    confirmar_reserva(conn, cancha_id, dia, horario, usuario)
    
    conn.close()

def confirmar_reserva(conn, cancha_id: int, dia: date, horario: str, usuario: str):
    """Procesa la confirmación de una reserva"""
    try:
        # Obtener detalles de la cancha
        cancha = conn.execute("""
            SELECT nombre, precio FROM canchas WHERE id = ?
        """, (cancha_id,)).fetchone()
        
        # Insertar reserva
        conn.execute("""
            INSERT INTO reservas (usuario, cancha_id, dia, horario, precio)
            VALUES (?, ?, ?, ?, ?)
        """, (usuario, cancha_id, str(dia), horario, cancha[1]))
        
        conn.commit()
        st.success(f"✅ Reserva confirmada para el {dia} a las {horario} en {cancha[0]}")
        st.balloons()
        st.experimental_rerun()
        
    except sqlite3.IntegrityError:
        st.error("⚠️ Este horario ya fue reservado por otro usuario. Por favor seleccione otro.")
    except Exception as e:
        st.error(f"❌ Error al procesar la reserva: {str(e)}")

def ver_reservas():
    """Muestra las reservas según el tipo de usuario"""
    if not st.session_state.get("logueado"):
        st.warning("🔒 Debes iniciar sesión para ver reservas")
        return
    
    es_admin = st.session_state.get("es_admin", False)
    email_actual = st.session_state["email"]
    
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
        """, (email_actual,)).fetchall()
    
    if not reservas:
        st.info("No hay reservas registradas")
        conn.close()
        return
    
    # Filtros para admin
    if es_admin:
        with st.expander("🔍 Filtros Avanzados", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                filtro_usuario = st.text_input("Filtrar por usuario")
            with col2:
                filtro_fecha = st.date_input("Filtrar por fecha")
    
    # Mostrar reservas
    for r in reservas:
        # Aplicar filtros si es admin
        if es_admin:
            if filtro_usuario and filtro_usuario.lower() not in r[1].lower():
                continue
            if filtro_fecha and str(filtro_fecha) != r[4]:
                continue
        
        with st.container():
            st.markdown(f"""
            ### 🏟️ {r[2]} ({r[3]})
            **📅 Fecha:** {r[4]}  
            **🕒 Horario:** {r[5]}  
            **💲 Precio:** ${r[6]:.2f}  
            **👤 Usuario:** {r[1] if es_admin else 'Tú'}  
            **⏰ Reservado el:** {r[7][:16]}  
            """)
            
            # Botón para cancelar reserva
            if st.button("❌ Cancelar Reserva", key=f"cancel_{r[0]}"):
                conn.execute("DELETE FROM reservas WHERE id = ?", (r[0],))
                conn.commit()
                st.success("Reserva cancelada correctamente")
                st.experimental_rerun()
            
            st.markdown("---")
    
    conn.close()



