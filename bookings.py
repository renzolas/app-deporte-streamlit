import streamlit as st
from database import get_db
from datetime import date, timedelta

TIME_SLOTS = [
    "08:00 - 09:30", "09:30 - 11:00", "11:00 - 12:30",
    "12:30 - 14:00", "14:00 - 15:30", "15:30 - 17:00"
]

def book_field():
    st.title("📅 Reservar Cancha")
    
    conn = get_db()
    
    # Obtener canchas disponibles
    fields = conn.execute(
        "SELECT id, name, sport_type, price FROM fields WHERE is_available = TRUE"
    ).fetchall()
    
    if not fields:
        st.warning("No hay canchas disponibles")
        return
    
    # Seleccionar cancha
    field_id = st.selectbox(
        "Seleccionar cancha",
        options=[f[0] for f in fields],
        format_func=lambda x: next(f[1] for f in fields if f[0] == x)
    
    # Seleccionar fecha
    booking_date = st.date_input(
        "Fecha de reserva",
        min_value=date.today(),
        max_value=date.today() + timedelta(days=30))
    
    # Mostrar horarios
    st.subheader("Horarios disponibles:")
    
    cols = st.columns(3)
    for i, slot in enumerate(TIME_SLOTS):
        with cols[i % 3]:
            if st.button(slot):
                try:
                    conn.execute(
                        "INSERT INTO bookings (user_email, field_id, date, time_slot) VALUES (?, ?, ?, ?)",
                        (st.session_state.email, field_id, str(booking_date), slot))
                    conn.commit()
                    st.success(f"✅ Reservado: {slot}")
                except sqlite3.IntegrityError:
                    st.error("⛔ Este horario ya está ocupado")

