import streamlit as st
from users import registrar_usuario, login_usuario, init_user_db
from fields import gestion_canchas
from reservas import reservar_cancha, ver_reservas
import sqlite3

# ---------------------------
# CONFIGURACIÓN INICIAL
# ---------------------------

def init_app():
    """Inicializa las bases de datos al iniciar la aplicación"""
    init_user_db()  # Base de datos de usuarios
    conn = sqlite3.connect("reservas.db")  # Base de datos de reservas
    conn.close()

# Configuración de la página
st.set_page_config(
    page_title="Sistema de Reservas Deportivas",
    page_icon="⚽",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
    .main {padding-top: 1rem;}
    .stButton button {background-color: #4CAF50; color: white;}
    .stAlert {border-left: 4px solid #2C3E50;}
    .reserva-card {border-radius: 10px; padding: 1rem; margin: 0.5rem 0; border: 1px solid #eee;}
    </style>
    """, unsafe_allow_html=True)

# ---------------------------
# FUNCIONES PRINCIPALES
# ---------------------------

def main():
    """Función principal de la aplicación"""
    
    # Inicialización del estado de sesión
    if "logueado" not in st.session_state:
        st.session_state.update({
            "logueado": False,
            "email": "",
            "es_admin": False,
            "canchas": []
        })

    # Encabezado principal
    st.markdown("<h1 style='text-align: center;'>⚽ Sistema de Reservas Deportivas</h1>", unsafe_allow_html=True)

    # Flujo de autenticación
    if not st.session_state["logueado"]:
        mostrar_interfaz_autenticacion()
    else:
        mostrar_interfaz_principal()

def mostrar_interfaz_autenticacion():
    """Muestra la interfaz de login/registro"""
    opcion = st.sidebar.radio("Seleccione una opción:", ["🔐 Iniciar sesión", "📝 Registrarse"])

    if opcion == "📝 Registrarse":
        st.subheader("Registro de nuevo usuario")
        with st.form("formulario_registro"):
            email = st.text_input("Correo electrónico")
            password = st.text_input("Contraseña", type="password")
            enviar = st.form_submit_button("Registrarme")

            if enviar:
                with st.spinner("Registrando usuario..."):
                    exito, mensaje = registrar_usuario(email, password)
                    if exito:
                        st.success(mensaje)
                    else:
                        st.error(mensaje)

    else:  # Login
        st.subheader("Inicio de sesión")
        with st.form("formulario_login"):
            email = st.text_input("Correo electrónico")
            password = st.text_input("Contraseña", type="password")
            enviar = st.form_submit_button("Ingresar")

            if enviar:
                with st.spinner("Verificando credenciales..."):
                    if login_usuario(email, password):
                        st.session_state.update({
                            "logueado": True,
                            "email": email,
                            "es_admin": email == "admin@cancha.com"
                        })
                        st.success("¡Bienvenido!")
                        st.rerun()
                    else:
                        st.error("Credenciales incorrectas")

def mostrar_interfaz_principal():
    """Interfaz después del login"""
    # Barra lateral con información de usuario
    st.sidebar.success(f"👤 Usuario: {st.session_state['email']}")
    
    if st.sidebar.button("🚪 Cerrar sesión"):
        st.session_state.update({
            "logueado": False,
            "email": "",
            "es_admin": False
        })
        st.rerun()

    # Interfaz según tipo de usuario
    if st.session_state["es_admin"]:
        mostrar_interfaz_administrador()
    else:
        mostrar_interfaz_usuario()

def mostrar_interfaz_administrador():
    """Interfaz para administradores"""
    st.sidebar.markdown("## 🛠 Panel de Control")
    opcion = st.sidebar.radio("Opciones:", ["🏟️ Gestionar Canchas", "📋 Ver Reservas"])

    st.subheader("Panel de Administración")
    if opcion == "🏟️ Gestionar Canchas":
        gestion_canchas()
    else:
        ver_reservas()

def mostrar_interfaz_usuario():
    """Interfaz para usuarios regulares"""
    st.sidebar.markdown("## 👤 Menú Principal")
    opcion = st.sidebar.radio("Opciones:", ["📅 Hacer Reserva", "🗓 Mis Reservas"])

    if opcion == "📅 Hacer Reserva":
        reservar_cancha()
    else:
        ver_reservas()

# ---------------------------
# EJECUCIÓN PRINCIPAL
# ---------------------------

if __name__ == "__main__":
    init_app()  # Inicializa bases de datos
    main()



