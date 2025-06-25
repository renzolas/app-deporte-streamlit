import streamlit as st
from data.datos_ejemplo import sports_data

st.title("👤 Vista de Usuario")

# Mostrar el deporte a seleccionar
selected_sport = st.selectbox("Selecciona un deporte", list(sports_data.keys()))

if selected_sport:
    st.subheader(f"Entrenadores de {selected_sport}")
    trainers = sports_data[selected_sport]

    for trainer, horarios in trainers.items():
        with st.expander(f"{trainer}"):
            st.markdown("**Horarios disponibles:**")
            for h in horarios:
                st.markdown(f"- 🕒 {h}")

if st.button("Volver a Home"):
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.experimental_rerun()

