import streamlit as st

# Inicializar canchas si no existe en la sesión
if "canchas" not in st.session_state:
    st.session_state["canchas"] = []

def gestion_canchas():
    st.subheader("⚙️ Gestión de Canchas")

    nombre = st.text_input("Nombre de la nueva cancha")
    ubicacion = st.text_input("Ubicación (opcional)")
    precio = st.number_input("Precio por hora ($)", min_value=0.0, step=5.0)
    disponible = st.checkbox("Disponible", value=True)

    if st.button("Agregar Cancha"):
        if nombre:
            cancha = {
                "nombre": nombre,
                "ubicacion": ubicacion,
                "precio": precio,
                "disponible": disponible
            }
            st.session_state["canchas"].append(cancha)
            st.success(f"Cancha '{nombre}' agregada correctamente.")
        else:
            st.warning("El nombre de la cancha es obligatorio.")

    st.markdown("### 🏟️ Canchas Registradas")
    if st.session_state["canchas"]:
        for i, c in enumerate(st.session_state["canchas"]):
            col1, col2, col3 = st.columns([4, 1, 1])
            estado = "✅ Disponible" if c.get("disponible", True) else "❌ No disponible"

            col1.markdown(f"""
            **{i+1}. {c['nombre']}**  
            📍 {c['ubicacion'] or 'Ubicación no especificada'}  
            💰 ${c['precio']} por hora  
            🔄 Estado: {estado}
            """)

            if col2.button("❌ Ocultar", key=f"ocultar_{i}"):
                st.session_state["canchas"][i]["disponible"] = False

            if col3.button("🗑 Eliminar", key=f"eliminar_{i}"):
                st.session_state["canchas"].pop(i)
                st.experimental_rerun()
    else:
        st.info("No hay canchas registradas aún.")


