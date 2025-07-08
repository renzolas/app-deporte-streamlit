import streamlit as st

# Simulación de reservas en memoria
reservas = []

# Lista de horarios disponibles
HORARIOS = [
    "09:00 - 10:00", "10:00 - 11:00", "11:00 - 12:00",
    "12:00 - 13:00", "13:00 - 14:00", "14:00 - 15:00",
    "15:00 - 16:00", "16:00 - 17:00", "17:00 - 18:00"
]

def reservar_cancha():
    st.subheader("📅 Reservar Cancha - Cancha Norte")

    email_usuario = st.session_state.get("email", "")
    if not email_usuario:
        st.warning("Debes iniciar sesión para reservar.")
        return

    st.markdown(f"👤 Usuario: **{email_usuario}**")
    dia = st.date_input("Selecciona un día")

    st.markdown("### 🕒 Selecciona un horario disponible:")

    col1, col2, col3 = st.columns(3)

    for i, horario in enumerate(HORARIOS):
        columna = [col1, col2, col3][i % 3]
        ocupado = any(r["dia"] == dia and r["horario"] == horario for r in reservas)
        if ocupado:
            columna.button(f"❌ {horario}", key=f"disabled_{i}", disabled=True)
        else:
            if columna.button(f"✅ {horario}", key=f"btn_{i}"):
                reservas.append({
                    "usuario": email_usuario,
                    "dia": dia,
                    "horario": horario
                })
                st.success(f"Reserva confirmada para {horario} el {dia}")
                st.balloons()

def ver_reservas():
    st.subheader("📖 Tus Reservas")
    email_actual = st.session_state.get("email", "")

    reservas_usuario = [r for r in reservas if r["usuario"] == email_actual]

    if reservas_usuario:
        for r in reservas_usuario:
            st.markdown(f"""
            🔹 **{r['usuario']}**  
            🏟️ Cancha: *Norte*  
            📅 Día: **{r['dia']}**  
            🕒 Horario: **{r['horario']}**
            ---
            """)
    else:
        st.info("No tienes reservas aún.")



