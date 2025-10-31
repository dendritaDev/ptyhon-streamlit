import streamlit as st
from google.cloud import bigquery
from utils.bq import run_bq_params

ALLOWED_USERS_TABLE = st.secrets["auth"]["ALLOWED_USERS_TABLE"]

def is_allowed_email(email: str) -> bool:
    if not email:
        return False
    
    email = email.strip().lower()

    sql = f"""
    SELECT 1
    FROM `{ALLOWED_USERS_TABLE}`
    WHERE LOWER(email) = @email
    LIMIT 1
    """
    
    params = [
        bigquery.ScalarQueryParameter("email", "STRING", email)
    ]
    
    result = run_bq_params(sql, params)

    return result.total_rows > 0
