import streamlit as st
from users import registrar_usuario, login_usuario
from fields import gestion_canchas
from reservas import reservar_cancha, ver_reservas

def main():
    st.title("🎾 App de Reservas Deportivas")

    menu = ["Login", "Registro"]
    opcion = st.sidebar.selectbox("Selecciona una opción", menu)

    if opcion == "Registro":
        st.subheader("Registro")
        email = st.text_input("Email")
        password = st.text_input("Contraseña", type="password")

        if st.button("Registrar"):
            registrar_usuario(email, password)

    elif opcion == "Login":
        st.subheader("Iniciar sesión")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Contraseña", type="password", key="login_pass")

        if st.button("Entrar"):
            if login_usuario(email, password):
                st.success(f"Bienvenido, {email}!")

                # Menú interno (después del login)
                menu_interno = ["Canchas", "Reservar", "Perfil"]
                eleccion = st.sidebar.selectbox("Menú", menu_interno)

                if eleccion == "Canchas":
                    gestion_canchas()

                elif eleccion == "Reservar":
                    reservar_cancha()

                elif eleccion == "Perfil":
                    ver_reservas()
            else:
                st.error("Email o contraseña incorrectos.")

if __name__ == "__main__":
    main()

