from database import get_db
from datetime import date, timedelta
import streamlit as st

TIME_SLOTS = [
    "08:00-09:30", "09:30-11:00", "11:00-12:30",
    "12:30-14:00", "14:00-15:30", "15:30-17:00"
]

def book_field():
    st.header("Reservar Cancha")
    
    conn = get_db()
    
    # Obtener canchas disponibles
    fields = conn.execute(
        "SELECT id, name, sport_type FROM fields WHERE is_available = TRUE"
    ).fetchall()
    
    if not fields:
        st.warning("No hay canchas disponibles")
        return
    
    field_id = st.selectbox(
        "Seleccionar cancha",
        options=[f[0] for f in fields],
        format_func=lambda x: next(f[1] for f in fields if f[0] == x)
    
    booking_date = st.date_input(
        "Fecha",
        min_value=date.today(),
        max_value=date.today() + timedelta(days=14))
    
    st.subheader("Horarios disponibles:")
    
    # Verificar disponibilidad
    booked = conn.execute(
        "SELECT time_slot FROM bookings WHERE field_id = ? AND date = ?",
        (field_id, str(booking_date))).fetchall()
    booked_slots = [b[0] for b in booked]
    
    cols = st.columns(3)
    for i, slot in enumerate(TIME_SLOTS):
        with cols[i % 3]:
            if slot in booked_slots:
                st.button(slot, disabled=True)
            elif st.button(slot):
                conn.execute(
                    "INSERT INTO bookings (user_email, field_id, date, time_slot) VALUES (?, ?, ?, ?)",
                    (st.session_state.auth["email"], field_id, str(booking_date), slot))
                conn.commit()
                st.success(f"Reserva confirmada: {slot}")
                st.rerun()

def view_bookings(admin_mode=False):
    st.header("Reservas" + (" (Administrador)" if admin_mode else ""))
    
    conn = get_db()
    
    if admin_mode:
        bookings = conn.execute("""
            SELECT b.id, b.user_email, f.name, b.date, b.time_slot 
            FROM bookings b JOIN fields f ON b.field_id = f.id
            ORDER BY b.date DESC
        """).fetchall()
    else:
        bookings = conn.execute("""
            SELECT b.id, f.name, b.date, b.time_slot 
            FROM bookings b JOIN fields f ON b.field_id = f.id
            WHERE b.user_email = ?
            ORDER BY b.date DESC
        """, (st.session_state.auth["email"],)).fetchall()
    
    if not bookings:
        st.info("No hay reservas registradas")
        return
    
    for booking in bookings:
        with st.expander(f"{booking[2]} - {booking[3]}"):
            if admin_mode:
                st.markdown(f"""
                **Usuario:** {booking[1]}  
                **Cancha:** {booking[2]}  
                **Fecha:** {booking[3]}  
                **Horario:** {booking[4]}
                """)
            else:
                st.markdown(f"""
                **Cancha:** {booking[1]}  
                **Fecha:** {booking[2]}  
                **Horario:** {booking[3]}
                """)
            
            if st.button("Cancelar", key=f"cancel_{booking[0]}"):
                conn.execute("DELETE FROM bookings WHERE id = ?", (booking[0],))
                conn.commit()
                st.success("Reserva cancelada")
                st.rerun()

