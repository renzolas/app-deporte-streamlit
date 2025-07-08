import streamlit as st
from users import registrar_usuario, login_usuario
from fields import gestion_canchas
from reservas import reservar_cancha, ver_reservas

def main():
    st.set_page_config(page_title="App de Reservas", layout="wide")
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
                st.success(f"Bienvenido, {email}!")

                # Detectar si es admin
                es_admin = email == "admin@cancha.com"

                if es_admin:
                    mostrar_menu_admin()
                else:
                    mostrar_menu_usuario()
            else:
                st.error("Email o contraseña incorrectos.")

def mostrar_menu_admin():
    st.markdown("## 🛠 Panel del Administrador")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("📋 Gestionar Canchas", use_container_width=True):
            gestion_canchas()

    with col2:
        if st.button("📅 Ver Reservas de Usuarios", use_container_width=True):
            ver_reservas()  # Puedes luego crear una función especial para admins

def mostrar_menu_usuario():
    st.markdown("## 🙋 Menú del Usuario")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("📅 Reservar Cancha", use_container_width=True):
            reservar_cancha()

    with col2:
        if st.button("📖 Ver Mis Reservas", use_container_width=True):
            ver_reservas()

if __name__ == "__main__":
    main()

