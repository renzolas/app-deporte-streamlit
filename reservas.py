import streamlit as st

# Simulación de reservas en memoria (más adelante podemos usar JSON)
reservas = []

# Lista de horarios disponibles
HORARIOS = [
    "09:00 - 10:00", "10:00 - 11:00", "11:00 - 12:00",
    "12:00 - 13:00", "13:00 - 14:00", "14:00 - 15:00",
    "15:00 - 16:00", "16:00 - 17:00", "17:00 - 18:00"
]

def reservar_cancha():
    st.subheader("📅 Reservar Cancha - Cancha Norte")
    nombre = st.text_input("Tu nombre")
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
                if nombre:
                    reservas.append({
                        "nombre": nombre,
                        "dia": dia,
                        "horario": horario
                    })
                    st.success(f"Reserva confirmada para {horario} el {dia}")
                    st.balloons()
                else:
                    st.warning("Por favor, escribe tu nombre.")

def ver_reservas():
    st.subheader("📖 Tus Reservas")

    if reservas:
        for r in reservas:
            st.markdown(f"""
            🔹 **{r['nombre']}** reservó  
            🏟️ *Cancha Norte*  
            📅 Día: **{r['dia']}**  
            🕒 Horario: **{r['horario']}**
            ---
            """)
    else:
        st.info("No hay reservas aún.")


