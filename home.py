import streamlit as st
from data.datos_ejemplo import users_db, sports_data

st.set_page_config(page_title="App Deportiva", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
        .main {background-color: #f0f2f6;}
        .block-container {padding-top: 2rem; padding-bottom: 2rem;}
        h1, h2, h3 {color: #003366;}
        .btn {background-color: #0066cc; color: white; padding: 0.5rem 1rem; border-radius: 5px; margin: 0.5rem 0;}
        .logo {text-align: center;}
    </style>
""", unsafe_allow_html=True)

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.session_state.page = "login"
if "login_attempts" not in st.session_state:
    st.session_state.login_attempts = 0

def login(username, password, role):
    username = username.lower()
    user = users_db.get(username)
    return user and user['password'] == password and user['type'] == role

def mostrar_logo():
    st.markdown("<div class='logo'><h1>⚽🏀 App Deportiva</h1><p><em>Tu centro deportivo inteligente</em></p></div>", unsafe_allow_html=True)

def pantalla_login():
    mostrar_logo()
    st.subheader("🔐 Iniciar sesión")

    if st.session_state.login_attempts >= 4:
        st.error("⚠️ Has excedido el número máximo de intentos. Por favor, inténtalo más tarde.")
        return

    username = st.text_input("👤 Usuario")
    password = st.text_input("🔑 Contraseña", type="password")
    role = st.radio("Tipo de acceso:", ["user", "admin"], horizontal=True)

    if st.button("🚀 Ingresar"):
        if login(username, password, role):
            st.session_state.authenticated = True
            st.session_state.username = username.lower()
            st.session_state.role = role
            st.session_state.page = "home_user" if role == "user" else "home_admin"
            st.session_state.login_attempts = 0
        else:
            st.session_state.login_attempts += 1
            intentos_restantes = 4 - st.session_state.login_attempts
            st.error(f"❌ Usuario o contraseña incorrectos. Intentos restantes: {intentos_restantes}")

    if st.session_state.authenticated:
        st.experimental_rerun()

def pantalla_usuario():
    mostrar_logo()
    st.subheader("👤 Panel del Usuario")
    st.write(f"Hola, **{st.session_state.username}**. ¿Qué te gustaría hacer?")

    if st.button("🎯 Ver deportes y entrenadores"):
        st.session_state.page = "ver_deportes"
        st.experimental_rerun()

    if st.button("🔓 Cerrar sesión"):
        cerrar_sesion()

def pantalla_deportes():
    mostrar_logo()
    st.subheader("🏅 Deportes disponibles")

    selected_sport = st.selectbox("Selecciona un deporte", list(sports_data.keys()))

    if selected_sport:
        st.markdown(f"### 🧑‍🏫 Entrenadores de {selected_sport}")
        for entrenador, horarios in sports_data[selected_sport].items():
            with st.expander(f"📋 {entrenador}"):
                for h in horarios:
                    st.markdown(f"🕒 {h}")

    if st.button("🔙 Volver al menú"):
        st.session_state.page = "home_user"
        st.experimental_rerun()

def pantalla_admin():
    mostrar_logo()
    st.subheader("🧑‍🏫 Panel del Entrenador")

    for sport, entrenadores in sports_data.items():
        st.markdown(f"### 🏅 {sport}")
        for entrenador, horarios in entrenadores.items():
            with st.expander(f"📋 {entrenador} - Clases reservadas"):
                alumnos = [
                    {"nombre": "Alumno 1", "fecha": "2025-07-01", "hora": horarios[0]},
                    {"nombre": "Alumno 2", "fecha": "2025-07-03", "hora": horarios[1]},
                ]
                for a in alumnos:
                    st.markdown(f"- 👤 {a['nombre']} | 📅 {a['fecha']} | ⏰ {a['hora']}")

    if st.button("🔓 Cerrar sesión"):
        cerrar_sesion()

def cerrar_sesion():
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.session_state.page = "login"
    st.session_state.login_attempts = 0
    st.experimental_rerun()

if not st.session_state.authenticated:
    pantalla_login()
else:
    if st.session_state.page == "home_user":
        pantalla_usuario()
    elif st.session_state.page == "ver_deportes":
        pantalla_deportes()
    elif st.session_state.page == "home_admin":
        pantalla_admin()

