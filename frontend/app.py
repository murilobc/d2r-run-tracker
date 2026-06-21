import streamlit as st

st.set_page_config(page_title="D2R MF Run Tracker", page_icon="🎮", layout="wide")

st.sidebar.title("🎮 D2R MF Tracker")
st.sidebar.markdown("Diablo 2 Resurrected v3.2")
st.sidebar.markdown("*Reign of the Warlock*")
st.sidebar.divider()

if "active_profile" not in st.session_state:
    st.session_state.active_profile = None

if st.session_state.active_profile:
    p = st.session_state.active_profile
    st.sidebar.success(f"**{p['name']}**\n\n{p['character_class']} • {p['game_mode']}")
else:
    st.sidebar.warning("Nenhum perfil selecionado")

st.title("🎮 D2R Magic Find Run Tracker")
st.markdown("Rastreie suas runs de Magic Find no Diablo 2 Resurrected (v3.2 - Reign of the Warlock)")
st.markdown("Use o menu lateral para navegar entre as páginas.")
