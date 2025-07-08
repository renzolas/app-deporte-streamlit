import streamlit as st

# Simulación de base de datos de canchas
canchas = []

def gestion_canchas():
    st.subheader("⚙️ Gestión de Canchas")

    nombre = st.text_input("Nombre de la nueva cancha")
    ubicacion = st.text_input("Ubicación (opcional)")
    precio = st.number_input("Precio por hora ($)", min_value=0.0, step=5.0)

    if st.button("Agregar Cancha"):
        if nombre:
            cancha = {
                "nombre": nombre,
                "ubicacion": ubicacion,
                "precio": precio
            }
            canchas.append(cancha)
            st.success(f"Cancha '{nombre}' agregada correctamente.")
        else:
            st.warning("El nombre de la cancha es obligatorio.")

    st.markdown("### 🏟️ Canchas Registradas")
    if canchas:
        for i, c in enumerate(canchas):
            st.markdown(f"""
            **{i+1}. {c['nombre']}**  
            📍 {c['ubicacion'] or 'Ubicación no especificada'}  
            💰 ${c['precio']} por hora  
            ---
            """)
    else:
        st.info("No hay canchas registradas aún.")

