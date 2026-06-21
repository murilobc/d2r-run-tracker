import time

import streamlit as st
import api_client
from api_client import ApiError
from constants import LOCATIONS

st.header("🎮 Run Tracker")

if not st.session_state.get("active_profile"):
    st.warning("Selecione um perfil na página de Perfis primeiro.")
    st.stop()

profile = st.session_state.active_profile

# Timer state
if "timer_running" not in st.session_state:
    st.session_state.timer_running = False
    st.session_state.timer_paused = False
    st.session_state.timer_start = 0.0
    st.session_state.timer_elapsed = 0.0
    st.session_state.timer_finished = False
    st.session_state.run_items = []

# Location selection
col1, col2 = st.columns([3, 1])
location = col1.selectbox(
    "Local da Run",
    options=list(LOCATIONS.keys()),
    format_func=lambda x: LOCATIONS[x],
    disabled=st.session_state.timer_running or st.session_state.timer_finished,
)

tz_note = None
if location == "terror_zone":
    tz_note = st.text_input("Qual Terror Zone?", placeholder="Ex: Tal Rasha's Tombs")

# Cache next_run_number to avoid API call on every timer rerun
cache_key = f"next_num_{profile['id']}_{location}"
if not st.session_state.timer_running or cache_key not in st.session_state:
    try:
        next_num = api_client.get_next_run_number(profile["id"], location)
        st.session_state[cache_key] = next_num
    except ApiError:
        next_num = st.session_state.get(cache_key, "?")
else:
    next_num = st.session_state.get(cache_key, "?")
col2.metric("Run #", next_num)


def format_time(seconds: float) -> str:
    m, s = divmod(int(seconds), 60)
    return f"{m:02d}:{s:02d}"


def get_elapsed() -> float:
    if st.session_state.timer_running and not st.session_state.timer_paused:
        return st.session_state.timer_elapsed + (time.time() - st.session_state.timer_start)
    return st.session_state.timer_elapsed


elapsed = get_elapsed()
st.markdown(f"## ⏱️ {format_time(elapsed)}")

col1, col2, col3 = st.columns(3)

if not st.session_state.timer_running and not st.session_state.timer_finished:
    if col1.button("▶️ Start", use_container_width=True):
        st.session_state.timer_running = True
        st.session_state.timer_paused = False
        st.session_state.timer_start = time.time()
        st.session_state.timer_elapsed = 0.0
        st.rerun()

elif st.session_state.timer_running:
    if st.session_state.timer_paused:
        if col1.button("▶️ Resume", use_container_width=True):
            st.session_state.timer_paused = False
            st.session_state.timer_start = time.time()
            st.rerun()
    else:
        if col2.button("⏸️ Pause", use_container_width=True):
            st.session_state.timer_elapsed += time.time() - st.session_state.timer_start
            st.session_state.timer_paused = True
            st.rerun()

    if col3.button("⏹️ Finish", use_container_width=True):
        if not st.session_state.timer_paused:
            st.session_state.timer_elapsed += time.time() - st.session_state.timer_start
        st.session_state.timer_running = False
        st.session_state.timer_finished = True
        st.rerun()

if st.session_state.timer_running and not st.session_state.timer_paused:
    time.sleep(1)
    st.rerun()

# Item registration
if st.session_state.timer_finished:
    st.divider()
    st.subheader("📦 Registrar Itens Encontrados")
    st.markdown(f"**Tempo da run:** {format_time(st.session_state.timer_elapsed)}")

    search_term = st.text_input("🔍 Buscar item", placeholder="Digite nome ou apelido do item...")
    if search_term:
        try:
            results = api_client.search_items(search=search_term, limit=20)
        except ApiError:
            results = []
        if results:
            options = {f"{item['name']} [{item['category']}]": item for item in results}
            selected = st.selectbox("Selecione o item", options=list(options.keys()))
            if st.button("➕ Adicionar item"):
                st.session_state.run_items.append(options[selected])
                st.rerun()
        else:
            st.caption("Nenhum item encontrado.")

    if st.session_state.run_items:
        st.markdown("**Itens adicionados:**")
        for i, item in enumerate(st.session_state.run_items):
            col1, col2 = st.columns([5, 1])
            badge = "🆕" if item.get("is_rotw") else ""
            col1.markdown(f"- {item['name']} `{item['category']}` {badge}")
            if col2.button("❌", key=f"rm_{i}"):
                st.session_state.run_items.pop(i)
                st.rerun()

    st.divider()
    col1, col2 = st.columns(2)

    def _save_run(item_ids: list[int]):
        try:
            api_client.create_run(
                profile_id=profile["id"],
                location=location,
                duration_seconds=max(1, int(st.session_state.timer_elapsed)),
                item_ids=item_ids,
                terror_zone_note=tz_note,
            )
            st.session_state.timer_finished = False
            st.session_state.timer_elapsed = 0.0
            st.session_state.run_items = []
            # Invalidate cached run number so it refreshes
            st.session_state.pop(f"next_num_{profile['id']}_{location}", None)
            st.success(f"✅ Run #{next_num} salva!")
            time.sleep(1)
            st.rerun()
        except ApiError as e:
            st.error(e.message)

    if col1.button("💾 Salvar Run", use_container_width=True, type="primary"):
        _save_run([item["id"] for item in st.session_state.run_items])

    if col2.button("⏭️ Nenhum item (pular)", use_container_width=True):
        _save_run([])
