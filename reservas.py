import streamlit as st
from datetime import datetime, date, time

# Simulación de base de datos de reservas (lista)
reservas = []

# Simulación de canchas (esto se puede conectar luego con fields.py)
canchas_disponibles = [
    {"id": 1, "nombre": "Cancha Fútbol Norte"},
    {"id": 2, "nombre": "Cancha Tenis Central"},
    {"id": 3, "nombre": "Cancha Padel Sur"},
]

def reservar_cancha():
    st.subheader("Reservar una cancha")

    # Seleccionar cancha
    cancha = st.selectbox("Selecciona una cancha", [c["nombre"] for c in canchas_disponibles])

    # Seleccionar fecha
    fecha = st.date_input("Selecciona una fecha", min_value=date.today())

    # Seleccionar hora
    hora = st.selectbox("Selecciona una hora", ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "17:00", "18:00", "19:00"])

    # Confirmar
    if st.button("Reservar"):
        nueva_reserva = {
            "cancha": cancha,
            "fecha": fecha.strftime("%Y-%m-%d"),
            "hora": hora,
            "usuario": "usuario_demo@example.com"  # Por ahora, fijo; luego será dinámico
        }
        reservas.append(nueva_reserva)
        st.success(f"Reserva confirmada para {cancha} el {fecha} a las {hora}")

        # Mostrar resumen
        st.write("Tu reserva:")
        st.json(nueva_reserva)

def ver_reservas():
    st.subheader("Mis reservas (simulado)")
    if reservas:
        for r in reservas:
            st.markdown(f"📌 {r['cancha']} | {r['fecha']} - {r['hora']}")
            st.divider()
    else:
        st.info("Aún no tienes reservas registradas.")

