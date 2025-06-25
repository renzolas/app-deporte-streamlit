import streamlit as st
from data.datos_ejemplo import sports_data

st.title("🧑‍🏫 Vista de Administrador")

st.write(f"Bienvenido, {st.session_state.username}")

# Para simplicidad mostramos todos los entrenadores y sus clases reservadas (datos simulados)
for sport, trainers in sports_data.items():
    st.subheader(f"Deporte: {sport}")
    for trainer, horarios in trainers.items():
        with st.expander(f"{trainer} - Clases reservadas"):
            # Datos ficticios de alumnos
            alumnos = [
                {"nombre": "Alumno 1", "fecha": "2025-07-01", "hora": horarios[0]},
                {"nombre": "Alumno 2", "fecha": "2025-07-03", "hora": horarios[1]},
            ]
            for a in alumnos:
                st.markdown(f"- 👤 {a['nombre']} | 📅 {a['fecha']} | ⏰ {a['hora']}")

if st.button("Cerrar sesión"):
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.experimental_rerun()

