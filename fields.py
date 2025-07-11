import streamlit as st

def gestion_canchas():
    st.subheader("⚙️ Gestión de Canchas")

    canchas = st.session_state.get("canchas", [])

    with st.form("form_cancha"):
        nombre = st.text_input("Nombre de la nueva cancha")
        ubicacion = st.text_input("Ubicación (opcional)")
        precio = st.number_input("Precio por hora ($)", min_value=0.0, step=5.0)
        disponible = st.checkbox("Disponible", value=True)
        submitted = st.form_submit_button("➕ Agregar Cancha")

        if submitted:
            if nombre:
                nueva_cancha = {
                    "nombre": nombre,
                    "ubicacion": ubicacion,
                    "precio": precio,
                    "disponible": disponible
                }
                canchas.append(nueva_cancha)
                st.session_state["canchas"] = canchas
                st.success(f"✅ Cancha '{nombre}' agregada correctamente.")
            else:
                st.warning("⚠️ El nombre de la cancha es obligatorio.")

    st.markdown("---")
    st.markdown("### 🏟️ Canchas Registradas")

    if not canchas:
        st.info("Aún no hay canchas registradas.")
        return

    for idx, cancha in enumerate(canchas):
        col1, col2, col3 = st.columns([4, 1, 1])
        estado = "✅ Disponible" if cancha.get("disponible", True) else "❌ No disponible"

        col1.markdown(f"""
        **{idx + 1}. {cancha['nombre']}**  
        📍 {cancha['ubicacion'] or 'Ubicación no especificada'}  
        💰 ${cancha['precio']} por hora  
        🔄 Estado: {estado}
        """)

        if col2.button("🟡 Cambiar", key=f"toggle_disp_{idx}"):
            canchas[idx]["disponible"] = not cancha.get("disponible", True)
            st.session_state["canchas"] = canchas
            st.experimental_rerun()

        if col3.button("🗑 Eliminar", key=f"eliminar_{idx}"):
            canchas.pop(idx)
            st.session_state["canchas"] = canchas
            st.experimental_rerun()



