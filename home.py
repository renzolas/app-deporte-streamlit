import streamlit as st

# ----------- DATOS SIMULADOS -----------

# Usuarios simulados (user y admin)
users_db = {
    'user1': {'password': '1234', 'type': 'user'},
    'admin1': {'password': 'admin', 'type': 'admin'},
}

# Deportes y entrenadores
sports_data = {
    'Fútbol': {
        'Entrenador Luis': ['Lunes 10:00', 'Miércoles 12:00'],
        'Entrenadora María': ['Martes 15:00', 'Jueves 10:00']
    },
    'Básquet': {
        'Coach Diego': ['Lunes 18:00', 'Viernes 17:00']
    },
    'Vóley': {
        'Coach Ana': ['Miércoles 09:00', 'Viernes 11:00']
    }
}

# ----------- FUNCIONES -----------

def login(username, password, role):
    user = users_db.get(username)
    if user and user['password'] == password and user['type'] == role:
        return True
    return False

# ----------- INTERFAZ -----------

st.set_page_config(page_title="App Deportiva", layout="centered")
st.title("🏋️‍♀️ App de Clases Deportivas")

# Sesión
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.role = ""
    st.session_state.username = ""

# LOGIN
if not st.session_state.authenticated:
    st.subheader("Iniciar sesión")

    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    role = st.radio("Tipo de acceso", ["user", "admin"], horizontal=True)

    if st.button("Ingresar"):
        if login(username, password, role):
            st.session_state.authenticated = True
            st.session_state.role = role
            st.session_state.username = username
            st.success(f"Bienvenido, {username} ({role})")
            st.experimental_rerun()
        else:
            st.error("Credenciales incorrectas")

# APP PRINCIPAL
else:
    st.success(f"Sesión iniciada como: {st.session_state.username} ({st.session_state.role})")
    st.write("Selecciona un deporte para ver entrenadores disponibles:")

    selected_sport = st.selectbox("🏀 Deportes disponibles", list(sports_data.keys()))

    if selected_sport:
        st.subheader(f"Entrenadores de {selected_sport}")
        trainers = sports_data[selected_sport]

        for trainer, horarios in trainers.items():
            with st.expander(f"{trainer}"):
                st.markdown("**Horarios disponibles:**")
                for h in horarios:
                    st.markdown(f"- 🕒 {h}")

    st.divider()
    if st.button("Cerrar sesión"):
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.experimental_rerun()
