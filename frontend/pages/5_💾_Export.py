import json

import streamlit as st
import api_client
from api_client import ApiError

st.header("💾 Export / Import")

if not st.session_state.get("active_profile"):
    st.warning("Selecione um perfil na página de Perfis primeiro.")
    st.stop()

profile = st.session_state.active_profile

# Export
st.subheader("📤 Exportar Perfil")
st.markdown(f"Exportar todos os dados do perfil **{profile['name']}** em JSON.")

if st.button("Gerar Export"):
    try:
        data = api_client.export_profile(profile["id"])
        json_str = json.dumps(data, indent=2, ensure_ascii=False)
        st.download_button(
            label="⬇️ Download JSON",
            data=json_str,
            file_name=f"d2r_runs_{profile['name'].replace(' ', '_')}.json",
            mime="application/json",
        )
        st.json(data)
    except ApiError as e:
        st.error(e.message)

st.divider()

# Import
st.subheader("📥 Importar Perfil")
st.markdown("Faça upload de um arquivo JSON exportado para criar um novo perfil com todas as runs.")

uploaded = st.file_uploader("Upload JSON", type=["json"])
if uploaded:
    try:
        data = json.loads(uploaded.read())
        st.json(data.get("profile", {}))
        st.caption(f"{len(data.get('runs', []))} runs no arquivo")

        if st.button("🚀 Importar", type="primary"):
            result = api_client.import_profile(data)
            st.success(f"✅ Perfil importado! ID: {result['profile_id']}, {result['runs_imported']} runs.")
    except json.JSONDecodeError:
        st.error("Arquivo JSON inválido.")
    except ApiError as e:
        st.error(e.message)
