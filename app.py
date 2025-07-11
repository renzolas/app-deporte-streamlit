import streamlit as st
from users import registrar_usuario, login_usuario
from fields import gestion_canchas
from reservas import reservar_cancha, ver_reservas

# ✅ Inicialización segura de reservas
if "reservas" not in st.session_state:
    st.session_state["reservas"] = []

st.set_page_config(page_title="App de Reservas Deportivas", layout="wide")

def main():
    st.markdown("<h1 style='text-align: center; color: #2C3E50;'>⚽ App de Reservas Deportivas</h1>", unsafe_allow_html=True)

    # Inicializar estado
    if "logueado" not in st.session_state:
        st.session_state["logueado"] = False

    # MENÚ INICIAL SI NO ESTÁ LOGUEADO
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

        elif opcion == "Login":
            st.subheader("🔐 Iniciar sesión")
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Contraseña", type="password", key="login_pass")

            if st.button("Entrar") and not st.session_state["logueado"]:
                if login_usuario(email, password):
                    st.session_state["logueado"] = True
                    st.session_state["email"] = email
                    st.success("Login exitoso. Usa el menú lateral para continuar...")
                    st.experimental_rerun()  # 🔁 Refresca para mostrar el menú de usuario
                else:
                    st.error("Email o contraseña incorrectos.")

    # MENÚ POST LOGIN
    else:
        email = st.session_state["email"]
        es_admin = email == "admin@cancha.com"       

        st.sidebar.success(f"Sesión activa: {email}")
        if st.sidebar.button("Cerrar sesión"):
            st.session_state.clear()
            st.experimental_rerun()  # 🔁 Refresca para volver al menú de login

        if es_admin:
            st.markdown("## 🛠 Panel del Administrador")
            menu = st.sidebar.radio("Selecciona una opción", ["📋 Gestionar Canchas", "📖 Ver Reservas de Usuarios"])
            if menu == "📋 Gestionar Canchas":
                gestion_canchas()
            elif menu == "📖 Ver Reservas de Usuarios":
                ver_reservas()
        else:
            st.markdown("## 🙋 Menú del Usuario")
            menu = st.sidebar.radio("Selecciona una opción", ["📅 Reservar Cancha", "📖 Ver Mis Reservas"])
            if menu == "📅 Reservar Cancha":
                reservar_cancha()
            elif menu == "📖 Ver Mis Reservas":
                ver_reservas()

# Ejecutar la app
main()


