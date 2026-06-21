import streamlit as st
import api_client
from api_client import ApiError
from constants import LOCATIONS_WITH_ALL, LOCATIONS

st.header("📋 Histórico de Runs")

if not st.session_state.get("active_profile"):
    st.warning("Selecione um perfil na página de Perfis primeiro.")
    st.stop()

profile = st.session_state.active_profile

col1, col2 = st.columns([3, 1])
location_filter = col1.selectbox("Filtrar por local", options=list(LOCATIONS_WITH_ALL.keys()), format_func=lambda x: LOCATIONS_WITH_ALL[x])

# Pagination
if "history_page" not in st.session_state:
    st.session_state.history_page = 1

PAGE_SIZE = 50

try:
    runs = api_client.list_runs(
        profile_id=profile["id"],
        location=location_filter if location_filter else None,
        page=st.session_state.history_page,
        size=PAGE_SIZE,
    )
except ApiError as e:
    st.error(e.message)
    st.stop()

if not runs:
    st.info("Nenhuma run registrada ainda.")
else:
    st.markdown(f"**Página {st.session_state.history_page}** — {len(runs)} runs")

    for run in runs:
        m, s = divmod(run["duration_seconds"], 60)
        time_str = f"{m:02d}:{s:02d}"
        items_str = ", ".join(item["item"]["name"] for item in run["items"]) or "Nenhum"
        loc_label = LOCATIONS.get(run["location"], run["location"])
        tz = f" ({run['terror_zone_note']})" if run.get("terror_zone_note") else ""

        col_info, col_del = st.columns([9, 1])
        col_info.markdown(
            f"**#{run['run_number']}** | {loc_label}{tz} | ⏱️ {time_str} | "
            f"🎁 {items_str} | 📅 {run['created_at'][:16]}"
        )
        if col_del.button("🗑️", key=f"del_run_{run['id']}"):
            try:
                api_client.delete_run(run["id"])
                st.rerun()
            except ApiError as e:
                st.error(e.message)

    # Pagination controls
    col1, col2 = st.columns(2)
    if st.session_state.history_page > 1:
        if col1.button("⬅️ Anterior"):
            st.session_state.history_page -= 1
            st.rerun()
    if len(runs) == PAGE_SIZE:
        if col2.button("Próxima ➡️"):
            st.session_state.history_page += 1
            st.rerun()

    # Summary
    st.divider()
    total_seconds = sum(run["duration_seconds"] for run in runs)
    total_items = sum(len(run["items"]) for run in runs)
    h, remainder = divmod(total_seconds, 3600)
    m, s = divmod(remainder, 60)
    time_total = f"{h}h {m:02d}m {s:02d}s" if h else f"{m:02d}m {s:02d}s"

    col1, col2, col3 = st.columns(3)
    col1.metric("🕐 Tempo total", time_total)
    col2.metric("🎁 Total de achados", total_items)
    col3.metric("🏃 Total de runs", len(runs))
