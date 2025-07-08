import streamlit as st

# Simulamos una "base de datos" con un diccionario (solo para ejemplo)
usuarios = {
    "usuario1@example.com": "password123",
    "admin@example.com": "adminpass"
}

def registrar_usuario(email, password):
    if email in usuarios:
        st.error("El usuario ya existe.")
    else:
        usuarios[email] = password
        st.success("Usuario registrado con éxito.")

def login_usuario(email, password):
    if email in usuarios and usuarios[email] == password:
        return True
    else:
        return False

def main():
    st.title("App de Reservas - Registro y Login")

    menu = ["Login", "Registro"]
    opcion = st.sidebar.selectbox("Selecciona opción", menu)

    if opcion == "Registro":
        st.subheader("Crear nueva cuenta")
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
                st.write("Aquí va el menú principal y opciones para el usuario...")
            else:
                st.error("Email o contraseña incorrectos.")

if __name__ == "__main__":
    main()

