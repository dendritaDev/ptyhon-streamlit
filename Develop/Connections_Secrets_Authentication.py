import streamlit as st
from utils.bq import get_bq_project_id, run_bq


#pip install google-cloud-bigquery google-auth


st.set_page_config(page_title="Connections, Secrets & Authentication", page_icon=":material/account_circle:")

st.title("Connections, Secrets & Authentication")


try:
    project_id = get_bq_project_id()
except KeyError:
    st.error("Falta [gcp_service_account] o el campo json en .streamlit/secrets.toml")
    st.stop()

st.success(f"Credenciales cargadas para el proyecto: {project_id}")

#query de prueba
default_sql = """
SELECT
    *
FROM
    
LIMIT 20
""".strip()

sql = st.text_area("SQL a ejecutar en BigQuery", value=default_sql, height=160, key="bq_sql")

if st.button("Ejecutar", type="primary"):
    df = run_bq(sql)
    st.write(f"Filas devueltas: {len(df)}")
    st.dataframe(df, hide_index=True)
else:
    st.info("Escribe una SQL o pulsa Ejecutar.")