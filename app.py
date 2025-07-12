import streamlit as st
from app.auth import login_user, register_user
from app.fields import manage_fields
from app.bookings import book_field

def main():
    st.set_page_config(page_title="Sistema de Reservas", layout="wide")
    
    if "logged_in" not in st.session_state:
        st.session_state.update({
            "logged_in": False,
            "is_admin": False,
            "email": ""
        })
    
    if not st.session_state.logged_in:
        show_auth()
    else:
        show_main()

def show_auth():
    st.title("Bienvenido al Sistema de Reservas")
    
    tab1, tab2 = st.tabs(["Iniciar Sesión", "Registrarse"])
    
    with tab1:
        with st.form("login"):
            email = st.text_input("Email")
            password = st.text_input("Contraseña", type="password")
            
            if st.form_submit_button("Ingresar"):
                if login_user(email, password):
                    st.success("Sesión iniciada correctamente")
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas")
    
    with tab2:
        with st.form("register"):
            email = st.text_input("Email")
            password = st.text_input("Contraseña", type="password")
            
            if st.form_submit_button("Registrarse"):
                if register_user(email, password):
                    st.success("Registro exitoso. Por favor inicia sesión.")
                else:
                    st.error("El email ya está registrado")

def show_main():
    st.sidebar.title(f"Bienvenido, {st.session_state.email}")
    
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.clear()
        st.rerun()
    
    if st.session_state.is_admin:
        manage_fields()
    else:
        book_field()

if __name__ == "__main__":
    main()

