import streamlit as st

HORARIOS = [
    "09:00 - 10:00", "10:00 - 11:00", "11:00 - 12:00",
    "12:00 - 13:00", "13:00 - 14:00", "14:00 - 15:00",
    "15:00 - 16:00", "16:00 - 17:00", "17:00 - 18:00"
]

def reservar_cancha():
    st.subheader("📅 Reservar una Cancha")

    email_usuario = st.session_state.get("email", "")
    if not email_usuario:
        st.warning("Debes iniciar sesión para reservar.")
        return

    st.markdown(f"👤 Usuario: **{email_usuario}**")

    canchas = st.session_state.get("canchas", [])
    reservas = st.session_state.get("reservas", [])

    if not canchas:
        st.info("No hay canchas disponibles aún. Intenta más tarde.")
        return

    nombres_canchas = [c["nombre"] for c in canchas if c.get("disponible", True)]
    if not nombres_canchas:
        st.warning("Actualmente no hay canchas disponibles.")
        return

    cancha_seleccionada = st.selectbox("Selecciona una cancha", nombres_canchas)
    dia = st.date_input("Selecciona un día")

    st.markdown("### 🕒 Selecciona un horario disponible:")

    col1, col2, col3 = st.columns(3)

    for i, horario in enumerate(HORARIOS):
        columna = [col1, col2, col3][i % 3]
        ocupado = any(
            r["dia"] == str(dia) and r["horario"] == horario and r["cancha"] == cancha_seleccionada
            for r in reservas
        )
        if ocupado:
            columna.button(f"❌ {horario}", key=f"disabled_{i}", disabled=True)
        else:
            if columna.button(f"✅ {horario}", key=f"btn_{i}"):
                nueva_reserva = {
                    "usuario": email_usuario,
                    "dia": str(dia),
                    "horario": horario,
                    "cancha": cancha_seleccionada
                }
                reservas.append(nueva_reserva)
                st.session_state["reservas"] = reservas
                st.success(f"Reserva confirmada en {cancha_seleccionada} para {horario} el {dia}")
                st.balloons()

def ver_reservas():
    email_actual = st.session_state.get("email", "")
    es_admin = email_actual == "admin@cancha.com"
    reservas = st.session_state.get("reservas", [])

    if not reservas:
        st.info("No hay reservas registradas aún.")
        return

    if es_admin:
        st.subheader("📖 Reservas de Todos los Usuarios")
        for r in reservas:
            st.markdown(f"""
            👤 **Usuario:** {r['usuario']}  
            🏟️ **Cancha:** {r['cancha']}  
            📅 **Día:** {r['dia']}  
            🕒 **Horario:** {r['horario']}
            ---
            """)
    else:
        st.subheader("📖 Mis Reservas")
        reservas_usuario = [r for r in reservas if r["usuario"] == email_actual]

        if not reservas_usuario:
            st.info("No tienes reservas aún.")
        else:
            for r in reservas_usuario:
                st.markdown(f"""
                🏟️ Cancha: **{r['cancha']}**  
                📅 Día: **{r['dia']}**  
                🕒 Horario: **{r['horario']}**
                ---
                """)



