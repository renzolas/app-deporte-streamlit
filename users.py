import streamlit as st

def registrar_usuario(email, password):
    """
    Registra un nuevo usuario si no existe.
    """
    usuarios = st.session_state.get("usuarios", [])

    for u in usuarios:
        if u["email"] == email:
            return False, "El usuario ya está registrado."

    usuarios.append({"email": email, "password": password})
    st.session_state["usuarios"] = usuarios
    return True, "Usuario registrado con éxito."

def login_usuario(email, password):
    """
    Verifica credenciales de login.
    """
    usuarios = st.session_state.get("usuarios", [])

    for u in usuarios:
        if u["email"] == email and u["password"] == password:
            return True

    # También se permite el acceso del admin por defecto
    if email == "admin@cancha.com" and password == "admin":
        return True

    return False

def reset_usuarios():
    """
    Limpia la lista de usuarios.
    """
    st.session_state["usuarios"] = []


