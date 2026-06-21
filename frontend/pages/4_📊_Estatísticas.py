import streamlit as st
import api_client
from api_client import ApiError
from constants import LOCATIONS

st.header("📊 Estatísticas")

if not st.session_state.get("active_profile"):
    st.warning("Selecione um perfil na página de Perfis primeiro.")
    st.stop()

profile = st.session_state.active_profile

try:
    stats = api_client.get_stats(profile["id"])
except ApiError as e:
    st.error(e.message)
    st.stop()

if stats["total_runs"] == 0:
    st.info("Nenhuma run registrada ainda.")
    st.stop()

# Metrics
col1, col2, col3 = st.columns(3)
total_time = stats["total_time_seconds"]
col1.metric("Total Runs", stats["total_runs"])
col2.metric("Tempo Total", f"{total_time // 3600}h {(total_time % 3600) // 60}m")
col3.metric("Itens Encontrados", stats["total_items_found"])

st.divider()

# Runs per location
st.subheader("Runs por Local")
chart_data = {
    LOCATIONS.get(k, k): v["total_runs"]
    for k, v in sorted(stats["locations"].items(), key=lambda x: -x[1]["total_runs"])
}
st.bar_chart(chart_data)

# Avg time per location
st.subheader("Tempo Médio por Local (segundos)")
avg_data = {
    LOCATIONS.get(k, k): v["avg_time_seconds"]
    for k, v in stats["locations"].items()
}
st.bar_chart(avg_data)

# Top items
st.subheader("Top 20 Itens Encontrados")
if stats["top_items"]:
    for item in stats["top_items"]:
        st.markdown(f"- **{item['name']}** — {item['count']}x")
else:
    st.caption("Nenhum item registrado ainda.")
