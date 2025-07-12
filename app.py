import streamlit as st
from auth import login_user, register_user

def main():
    st.title("Prueba de Auth")
    
    if st.button("Test Register"):
        if register_user("test@test.com", "password123"):
            st.success("Registro exitoso")
        else:
            st.error("Error en registro")
    
    if st.button("Test Login"):
        if login_user("admin@admin.com", "admin"):
            st.success("Login exitoso")
        else:
            st.error("Error en login")

if __name__ == "__main__":
    main()
