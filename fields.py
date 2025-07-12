import streamlit as st
from database import get_db

def manage_fields():
    st.title("🏟️ Gestión de Canchas")
    
    with st.form("add_field"):
        name = st.text_input("Nombre de la cancha")
        sport = st.selectbox("Deporte", ["Fútbol", "Básquetbol", "Tenis", "Vóleibol"])
        price = st.number_input("Precio por hora ($)", min_value=0.0)
        
        if st.form_submit_button("Agregar cancha"):
            conn = get_db()
            conn.execute(
                "INSERT INTO fields (name, sport_type, price) VALUES (?, ?, ?)",
                (name, sport, price))
            conn.commit()
            st.success("✅ Cancha agregada exitosamente")
