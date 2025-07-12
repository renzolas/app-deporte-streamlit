import streamlit as st
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional

# ---------------------------
# CONFIGURACIÓN INICIAL
# ---------------------------

def init_db():
    """Inicializa la base de datos de canchas"""
    conn = sqlite3.connect("reservas.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS canchas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL,
            deporte TEXT NOT NULL,
            ubicacion TEXT,
            precio REAL NOT NULL,
            disponible BOOLEAN DEFAULT TRUE,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    return conn

# ---------------------------
# FUNCIONES PRINCIPALES
# ---------------------------

def gestion_canchas():
    """Interfaz para gestionar canchas deportivas"""
    st.subheader("⚙️ Administración de Canchas")
    
    # Pestañas para diferentes acciones
    tab1, tab2 = st.tabs(["➕ Agregar Cancha", "🏟️ Canchas Existentes"])
    
    with tab1:
        agregar_cancha()
    
    with tab2:
        listar_canchas()

def agregar_cancha():
    """Formulario para agregar nuevas canchas"""
    deportes = ["Fútbol", "Básquetbol", "Tenis", "Vóleibol", "Pádel"]
    
    with st.form("form_nueva_cancha", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            nombre = st.text_input("Nombre de la cancha*", help="Ej: Cancha 1 - Fútbol")
            deporte = st.selectbox("Deporte*", deportes)
            ubicacion = st.text_input("Ubicación")
            
        with col2:
            precio = st.number_input("Precio por hora (USD)*", min_value=0.0, step=5.0, value=50.0)
            disponible = st.checkbox("Disponible para reservas", value=True)
        
        enviar = st.form_submit_button("Guardar Cancha")
        
        if enviar:
            if not nombre:
                st.error("El nombre es obligatorio")
                return
                
            conn = init_db()
            try:
                conn.execute("""
                    INSERT INTO canchas (nombre, deporte, ubicacion, precio, disponible)
                    VALUES (?, ?, ?, ?, ?)
                """, (nombre, deporte, ubicacion, precio, disponible))
                conn.commit()
                st.success(f"Cancha '{nombre}' registrada exitosamente!")
                st.balloons()
            except sqlite3.IntegrityError:
                st.error("❌ Ya existe una cancha con ese nombre")
            finally:
                conn.close()

def listar_canchas():
    """Muestra y permite gestionar las canchas existentes"""
    conn = init_db()
    canchas = conn.execute("""
        SELECT id, nombre, deporte, ubicacion, precio, disponible 
        FROM canchas 
        ORDER BY nombre
    """).fetchall()
    conn.close()
    
    if not canchas:
        st.info("No hay canchas registradas aún.")
        return
    
    # Filtros de búsqueda
    with st.expander("🔍 Filtros", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            filtro_nombre = st.text_input("Buscar por nombre")
        
        with col2:
            deportes = list(set(c[2] for c in canchas))
            filtro_deporte = st.selectbox("Filtrar por deporte", ["Todos"] + deportes)
        
        with col3:
            filtro_disponible = st.selectbox("Disponibilidad", ["Todas", "Disponibles", "No disponibles"])
    
    # Aplicar filtros
    canchas_filtradas = [
        c for c in canchas
        if (not filtro_nombre or filtro_nombre.lower() in c[1].lower())
        and (filtro_deporte == "Todos" or c[2] == filtro_deporte)
        and (
            filtro_disponible == "Todas" or
            (filtro_disponible == "Disponibles" and c[5]) or
            (filtro_disponible == "No disponibles" and not c[5])
        )
    ]
    
    if not canchas_filtradas:
        st.warning("No hay canchas que coincidan con los filtros")
        return
    
    # Mostrar canchas en tarjetas
    for cancha in canchas_filtradas:
        id_cancha, nombre, deporte, ubicacion, precio, disponible = cancha
        
        with st.container():
            col1, col2 = st.columns([4, 1])
            
            with col1:
                st.markdown(f"""
                ### {nombre}
                **Deporte:** {deporte}  
                **Ubicación:** {ubicacion or "No especificada"}  
                **Precio:** ${precio:.2f} por hora  
                **Estado:** {"✅ Disponible" if disponible else "❌ No disponible"}
                """)
            
            with col2:
                # Botón para cambiar disponibilidad
                if st.button(
                    "🔄" if disponible else "🔒", 
                    key=f"dispo_{id_cancha}",
                    help="Cambiar disponibilidad"
                ):
                    conn = init_db()
                    conn.execute(
                        "UPDATE canchas SET disponible = ? WHERE id = ?",
                        (not disponible, id_cancha)
                    )
                    conn.commit()
                    conn.close()
                    st.experimental_rerun()
                
                # Botón para eliminar (con confirmación)
                if st.button(
                    "🗑️", 
                    key=f"elim_{id_cancha}",
                    help="Eliminar cancha"
                ):
                    if st.session_state.get("confirmar_eliminar") == id_cancha:
                        conn = init_db()
                        conn.execute("DELETE FROM canchas WHERE id = ?", (id_cancha,))
                        conn.commit()
                        conn.close()
                        st.success("Cancha eliminada")
                        st.experimental_rerun()
                    else:
                        st.session_state["confirmar_eliminar"] = id_cancha
                        st.warning("¿Confirmas eliminar esta cancha? Pulsa nuevamente el botón para eliminar")


