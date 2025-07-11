import streamlit as st
from users import registrar_usuario, login_usuario
from fields import gestion_canchas
from reservas import reservar_cancha, ver_reservas

# Inicialización de reservas
if "reservas" not in st.session_state:
    st.session_state["reservas"] = []

st.set_page_config(page_title="App de Reservas Deportivas", layout="wide")

def main():
    st.markdown("<h1 style='text-align: center; color: #2C3E50;'>⚽ App de Reservas Deportivas</h1>", unsafe_allow_html=True)

    if "logueado" not in st.session_state:
        st.session_state["logueado"] = False

    if not st.session_state["logueado"]:
        menu = ["Login", "Registro"]
        opcion = st.sidebar.selectbox("👤 Selecciona una opción", menu)

        if opcion == "Registro":
            st.subheader("📝 Registro")
            email = st.text_input("Email")
            password = st.text_input("Contraseña", type="password")
            if st.button("Registrar"):
                exito, mensaje = registrar_usuario(email, password)
                if exito:
                    st.success(mensaje)
                else:
                    st.error(mensaje)

        else:  # Login
            st.subheader("🔐 Iniciar sesión")
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Contraseña", type="password", key="login_pass")

            if st.button("Entrar") and not st.session_state["logueado"]:
                if login_usuario(email, password):
                    st.session_state["logueado"] = True
                    st.session_state["email"] = email
                    st.success("Login exitoso. Esperá un momento...")
                else:
                    st.error("Email o contraseña incorrectos.")

    else:
        email = st.session_state["email"]
        es_admin = email == "admin@cancha.com"

        st.sidebar.success(f"Sesión activa: {email}")
        if st.sidebar.button("Cerrar sesión"):
            st.session_state.clear()

        if es_admin:
            st.markdown("## 🛠 Panel del Administrador")
            menu = st.sidebar.radio("Selecciona una opción", ["📋 Gestionar Canchas", "📖 Ver Reservas de Usuarios"])
            if menu == "📋 Gestionar Canchas":
                gestion_canchas()
            else:
                ver_reservas()
        else:
            st.markdown("## 🙋 Menú del Usuario")
            menu = st.sidebar.radio("Selecciona una opción", ["📅 Reservar Cancha", "📖 Ver Mis Reservas"])
            if menu == "📅 Reservar Cancha":
                reservar_cancha()
            else:
                ver_reservas()

main()



