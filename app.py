import streamlit as st
from auth import login_user, register_user
from fields import manage_fields
from bookings import book_field, view_bookings

# Configuración inicial
def init_session():
    if "auth" not in st.session_state:
        st.session_state.auth = {
            "logged_in": False,
            "is_admin": False,
            "email": ""
        }

# Interfaz de autenticación
def auth_interface():
    st.title("⚽ Club Deportivo Las Águilas")
    
    tab1, tab2 = st.tabs(["Iniciar Sesión", "Registrarse"])
    
    with tab1:
        with st.form("login_form"):
            email = st.text_input("Correo electrónico")
            password = st.text_input("Contraseña", type="password")
            
            if st.form_submit_button("Ingresar"):
                if login_user(email, password):
                    st.session_state.auth.update({
                        "logged_in": True,
                        "email": email,
                        "is_admin": email == "admin@admin.com"
                    })
                    st.success("¡Bienvenido!")
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas")

    with tab2:
        with st.form("register_form"):
            email = st.text_input("Correo (registro)")
            password = st.text_input("Contraseña (registro)", type="password")
            
            if st.form_submit_button("Crear cuenta"):
                if register_user(email, password):
                    st.success("¡Registro exitoso! Por favor inicia sesión")
                else:
                    st.error("El correo ya está registrado")

# Interfaz principal
def main_interface():
    st.sidebar.title(f"👤 {st.session_state.auth['email']}")
    
    if st.sidebar.button("🚪 Cerrar sesión"):
        st.session_state.clear()
        st.rerun()
    
    if st.session_state.auth["is_admin"]:
        menu = st.sidebar.radio("Menú", ["🏟️ Gestionar Canchas", "📋 Ver Reservas"])
        if menu == "🏟️ Gestionar Canchas":
            manage_fields()
        else:
            view_bookings(admin_mode=True)
    else:
        menu = st.sidebar.radio("Menú", ["📅 Reservar Cancha", "🗓 Mis Reservas"])
        if menu == "📅 Reservar Cancha":
            book_field()
        else:
            view_bookings()

# App principal
def main():
    st.set_page_config(page_title="Sistema de Reservas", layout="wide")
    init_session()
    
    if not st.session_state.auth["logged_in"]:
        auth_interface()
    else:
        main_interface()

if __name__ == "__main__":
    main()
