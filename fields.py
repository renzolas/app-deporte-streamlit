import streamlit as st

# Simulamos una base de datos de canchas
canchas = [
    {
        "id": 1,
        "nombre": "Cancha Fútbol Norte",
        "deporte": "Fútbol",
        "precio": 30,
        "disponible": True
    },
    {
        "id": 2,
        "nombre": "Cancha Tenis Central",
        "deporte": "Tenis",
        "precio": 25,
        "disponible": True
    }
]

def mostrar_canchas():
    st.subheader("Canchas disponibles")
    for cancha in canchas:
        if cancha["disponible"]:
            st.markdown(f"""
            **{cancha['nombre']}**  
            Deporte: {cancha['deporte']}  
            Precio por hora: ${cancha['precio']}  
            """)
            st.divider()

def agregar_cancha():
    st.subheader("Agregar nueva cancha")
    nombre = st.text_input("Nombre de la cancha")
    deporte = st.selectbox("Deporte", ["Fútbol", "Tenis", "Padel", "Basket"])
    precio = st.number_input("Precio por hora", min_value=5, step=1)
    disponible = st.checkbox("Disponible", value=True)

    if st.button("Agregar cancha"):
        nueva_cancha = {
            "id": len(canchas) + 1,
            "nombre": nombre,
            "deporte": deporte,
            "precio": precio,
            "disponible": disponible
        }
        canchas.append(nueva_cancha)
        st.success("Cancha agregada correctamente.")

def gestion_canchas():
    st.header("Gestión de Canchas")
    seccion = st.radio("Selecciona acción", ["Ver canchas", "Agregar cancha"])
    
    if seccion == "Ver canchas":
        mostrar_canchas()
    elif seccion == "Agregar cancha":
        agregar_cancha()

