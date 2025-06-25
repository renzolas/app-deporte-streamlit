import streamlit as st
from data.datos_ejemplo import users_db  # ✅ Importa desde archivo externo

# ----------- CONFIGURACIÓN DE PÁGINA -----------
st.set_page_config(page_title="App Deportiva", layout="centered")
st.title("🏋️‍♀️ Bienvenido a la App Deportiva")

# ----------- SESIÓN -----------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.role = ""
    st.session_state.username = ""

# ----------- FUNCIÓN DE LOGIN -----------
def login(username, password, role):
    user = users_db.get(username)
    if user and user['password'] == password and user['type'] == role:
        return True
    return False

# ----------- INTERFAZ DE LOGIN -----------
if not st.session_state.authenticated:
    st.subheader("Iniciar sesión")

    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    role = st.radio("Tipo de acceso", ["user", "admin"], horizontal=True)

    if st.button("Ingresar"):
        if login(username, password, role):
            st.session_state.authenticated = True
            st.session_state.role = role
            st.session_state.username = username
            st.success(f"Bienvenido, {username} ({role})")
            st.info("Usa el menú de la izquierda para navegar")
            st.stop()
        else:
            st.error("Credenciales incorrectas. Intenta de nuevo.")

else:
    st.success(f"Sesión activa: {st.session_state.username} ({st.session_state.role})")
    st.info("Usa el menú lateral izquierdo para acceder a las páginas.")
    if st.button("Cerrar sesión"):
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.experimental_rerun()
