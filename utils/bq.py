import json
import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery

#https://docs.streamlit.io/develop/tutorials/databases/bigquery
#pip install db.dtypes para poder hacer to_dataframe()

def _load_sa_info() -> dict:
    sa_json_str = st.secrets["gcp_service_account"]["json"]
    return json.loads(sa_json_str)

def get_bq_project_id() -> str:
    sa_info = _load_sa_info()
    return sa_info["project_id"]

@st.cache_resource
def get_bq_client() -> bigquery.Client:
    sa_info = _load_sa_info()
    credentials = service_account.Credentials.from_service_account_info(sa_info)
    return bigquery.Client(credentials=credentials, project=sa_info["project_id"])

@st.cache_data(ttl=600)
def run_bq(sql: str):
    client = get_bq_client()
    job = client.query(sql)
    return job.result().to_dataframe()

#para auth, no hacemos cache data para q no quede guardado un correo q despues se elimine de la tabla o algo
def run_bq_params(sql: str, params: list[bigquery.ScalarQueryParameter]):
    client = get_bq_client()
    job_config = bigquery.QueryJobConfig(query_parameters=params)
    job = client.query(sql, job_config=job_config)
    return job.result()