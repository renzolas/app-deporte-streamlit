import streamlit as st
from database import get_db
from datetime import date, timedelta

TIME_SLOTS = [
    "08:00-09:30", "09:30-11:00", "11:00-12:30",
    "12:30-14:00", "14:00-15:30", "15:30-17:00"
]

def book_field():
    if not st.session_state.get("logged_in"):
        st.warning("Debes iniciar sesión para reservar")
        return
    
    st.title("Reservar Cancha")
    
    conn = get_db()
    
    # Obtener canchas disponibles
    fields = conn.execute(
        "SELECT id, name, sport_type, price FROM fields WHERE is_available = TRUE"
    ).fetchall()
    
    if not fields:
        st.info("No hay canchas disponibles")
        return
    
    # Seleccionar cancha
    field_id = st.selectbox(
        "Seleccionar Cancha",
        options=[f[0] for f in fields],
        format_func=lambda x: next(f[1] for f in fields if f[0] == x)
    
    # Seleccionar fecha
    booking_date = st.date_input(
        "Fecha",
        min_value=date.today(),
        max_value=date.today() + timedelta(days=14))
    
    # Mostrar horarios disponibles
    st.subheader("Horarios Disponibles")
    
    # Verificar disponibilidad
    booked_slots = conn.execute(
        "SELECT time_slot FROM bookings WHERE field_id = ? AND date = ?",
        (field_id, str(booking_date))).fetchall()
    
    booked_slots = [b[0] for b in booked_slots]
    
    cols = st.columns(3)
    for i, slot in enumerate(TIME_SLOTS):
        with cols[i % 3]:
            if slot in booked_slots:
                st.button(slot, disabled=True)
            else:
                if st.button(slot):
                    conn.execute(
                        "INSERT INTO bookings (user_id, field_id, date, time_slot) VALUES (?, ?, ?, ?)",
                        (st.session_state["user_id"], field_id, str(booking_date), slot))
                    conn.commit()
                    st.success(f"Reserva confirmada para {slot}")

