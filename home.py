import streamlit as st
from data.datos_ejemplo import users_db, sports_data

# Configuración inicial
st.set_page_config(page_title="App Deportiva", layout="centered", initial_sidebar_state="collapsed")

# Estilos
st.markdown("""
<style>
  .block-container {padding: 1rem 2rem;}
  .logo {text-align: center; margin-bottom: 1rem;}
  h1, h2, h3 {color: #003366;}
</style>
""", unsafe_allow_html=True)

# Estado de sesión
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.session_state.page = "login"
if "login_attempts" not in st.session_state:
    st.session_state.login_attempts = 0

# Función de login tolerant with lowercase
def login(username, password, role):
    u = users_db.get(username.lower())
    return u and u["password"] == password and u["type"] == role

# Función para mostrar logo
def mostrar_logo():
    st.markdown("<div class='logo'><h1>⚽🏋️ App Deportiva</h1><p>Tu centro deportivo inteligente</p></div>", unsafe_allow_html=True)

# Pantallas
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
            st.experimental_rerun()
        else:
            st.session_state.login_attempts += 1
            intentos_restantes = 4 - st.session_state.login_attempts
            st.error(f"❌ Usuario o contraseña incorrectos. Intentos restantes: {intentos_restantes}")

def pantalla_usuario():
    mostrar_logo()
    st.subheader(f"👤 Bienvenido, {st.session_state.username}")
    if st.button("🎯 Ver deportes"):
        st.session_state.page = "ver_deportes"
        st.experimental_rerun()
    if st.button("🔓 Cerrar sesión"):
        cerrar_sesion()

def pantalla_deportes():
    mostrar_logo()
    st.subheader("🏅 Selecciona un deporte")
    sport = st.selectbox("", list(sports_data.keys()))
    if sport:
        for coach, horarios in sports_data[sport].items():
            with st.expander(f"{coach}"):
                for h in horarios:
                    st.markdown(f"- 🕒 {h}")
    if st.button("🔙 Volver"):
        st.session_state.page = "home_user"
        st.experimental_rerun()

def pantalla_admin():
    mostrar_logo()
    st.subheader(f"🧑‍🏫 Panel de {st.session_state.username}")
    for sport, coaches in sports_data.items():
        st.markdown(f"### {sport.capitalize()}")
        for coach, horarios in coaches.items():
            with st.expander(coach):
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
    st.session_state.page = "login"
    st.experimental_rerun()

# Control de flujo
if not st.session_state.authenticated:
    pantalla_login()
else:
    if st.session_state.page == "home_user":
        pantalla_usuario()
    elif st.session_state.page == "ver_deportes":
        pantalla_deportes()
    else:
        pantalla_admin()


