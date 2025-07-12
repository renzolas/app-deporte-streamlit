import streamlit as st
from database import get_db

def manage_fields():
    if not st.session_state.get("is_admin"):
        st.warning("Acceso restringido a administradores")
        return
    
    st.title("Gestión de Canchas")
    
    # Formulario para agregar cancha
    with st.form("add_field"):
        name = st.text_input("Nombre de la cancha")
        sport = st.selectbox("Deporte", ["Fútbol", "Básquet", "Tenis", "Vóleibol"])
        price = st.number_input("Precio por hora", min_value=0.0)
        
        if st.form_submit_button("Agregar Cancha"):
            conn = get_db()
            conn.execute(
                "INSERT INTO fields (name, sport_type, price) VALUES (?, ?, ?)",
                (name, sport, price))
            conn.commit()
            st.success("Cancha agregada exitosamente")
