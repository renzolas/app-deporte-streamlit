import streamlit as st
from users import registrar_usuario, login_usuario
from fields import gestion_canchas
from reservas import reservar_cancha, ver_reservas

st.set_page_config(page_title="App de Reservas Deportivas", layout="wide")

def main():
    st.markdown("<h1 style='text-align: center; color: #2C3E50;'>⚽ App de Reservas Deportivas</h1>", unsafe_allow_html=True)

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

    elif opcion == "Login":
        st.subheader("🔐 Iniciar sesión")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Contraseña", type="password", key="login_pass")

        if st.button("Entrar"):
            if login_usuario(email, password):
                st.session_state["logueado"] = True
                st.session_state["email"] = email
                st.success(f"Bienvenido, {email}!")
                st.experimental_rerun()  # Refresca para mostrar menú
            else:
                st.error("Email o contraseña incorrectos.")

# Verifica si hay sesión activa
if "logueado" in st.session_state and st.session_state["logueado"]:
    email = st.session_state["email"]
    es_admin = email == "admin@cancha.com"

    st.sidebar.success(f"Sesión activa: {email}")
    st.sidebar.button("Cerrar sesión", on_click=lambda: st.session_state.clear())

    if es_admin:
        st.markdown("## 🛠 Panel del Administrador")
        col1, col2 = st.columns(2)

        with col1:
            if st.button("📋 Gestionar Canchas", use_container_width=True):
                gestion_canchas()

        with col2:
            if st.button("📅 Ver Reservas de Usuarios", use_container_width=True):
                ver_reservas()  # Por ahora muestra todas

    else:
        st.markdown("## 🙋 Menú del Usuario")
        col1, col2 = st.columns(2)

        with col1:
            if st.button("📅 Reservar Cancha", use_container_width=True):
                reservar_cancha()

        with col2:
            if st.button("📖 Ver Mis Reservas", use_container_width=True):
                ver_reservas()

else:
    main()


