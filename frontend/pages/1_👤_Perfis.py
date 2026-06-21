import streamlit as st
import api_client
from api_client import ApiError
from constants import GAME_MODES, CLASSES

st.header("👤 Perfis")

with st.expander("➕ Criar novo perfil", expanded=not st.session_state.get("active_profile")):
    with st.form("create_profile"):
        name = st.text_input("Nome do perfil", placeholder="Ex: Sorceress Ladder S14")
        col1, col2 = st.columns(2)
        game_mode = col1.selectbox("Modo de jogo", options=list(GAME_MODES.keys()), format_func=lambda x: GAME_MODES[x])
        char_class = col2.selectbox("Classe", options=CLASSES, format_func=str.capitalize)
        if st.form_submit_button("Criar"):
            if name.strip():
                try:
                    api_client.create_profile(name.strip(), game_mode, char_class)
                    st.rerun()
                except ApiError as e:
                    st.error(e.message)

st.subheader("Perfis existentes")
try:
    profiles = api_client.list_profiles()
except ApiError as e:
    st.error(e.message)
    st.stop()

if not profiles:
    st.info("Nenhum perfil criado ainda.")
else:
    for p in profiles:
        col1, col2, col3 = st.columns([4, 2, 1])
        col1.markdown(f"**{p['name']}** — {p['character_class'].capitalize()} • {GAME_MODES.get(p['game_mode'], p['game_mode'])}")

        is_active = st.session_state.get("active_profile") and st.session_state.active_profile["id"] == p["id"]
        if is_active:
            col2.success("✅ Ativo")
        else:
            if col2.button("Selecionar", key=f"sel_{p['id']}"):
                st.session_state.active_profile = p
                st.rerun()

        if col3.button("🗑️", key=f"del_{p['id']}"):
            try:
                api_client.delete_profile(p["id"])
                if is_active:
                    st.session_state.active_profile = None
                st.rerun()
            except ApiError as e:
                st.error(e.message)
