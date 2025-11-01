import streamlit as st
from utils.state_sync import init_global
from utils.auth import is_allowed_email

# INSTALLATION:
#python <= 3.12
#pip install streamlit
#streamlit run MyApp.py

st.set_page_config(page_title="MyApp", page_icon=":material/apps:")

# VARIABLES GLOBALES (COMPARTIDAS ENTRE PÁGINAS)
init_global("global_group", "A")
init_global("global_threshold", 50)
 
if "user_email" not in st.session_state:
    st.session_state.user_email = None

def login_page():
    st.title("Log in")
    email = st.text_input("Correo corporativo / Gmail", key="login_email")
    if st.button("Entrar", type="primary"):
        if is_allowed_email(email):
            st.session_state.user_email = email.strip()
            st.rerun()
        else:
            st.error("Este correo no está autorizado.")

def logout_page():
    st.title("Log out")
    st.write(f"Sesión: {st.session_state.user_email}")
    if st.button("Log out"):
        st.session_state.user_email = None
        st.rerun()

#Get started
fundamentals_page = st.Page("Get started/Fundamentals.py", title="Fundamentals", default=True)

#Develop
architecture_page = st.Page("Develop/Architecture_and_Execution.py", title="Architecture", icon=":material/dashboard:")
appdesign_page = st.Page("Develop/AppDesign.py", title="AppDesign", icon=":material/brush:")
connectionSecretsAuth_page = st.Page("Develop/Connections_Secrets_Authentication.py", title="Connections, Secrets & Authentication", icon=":material/account_circle:")
customComponents_page = st.Page("Develop/CustomComponents.py", title="Custom Components", icon=":material/sdk:")
configurationAndTheming_page = st.Page("Develop/ConfigurationAndTheming.py", title="Configuration & Theming", icon=":material/settings:")
apiRefence_page = st.Page("Develop/ApiReference.py", title="API Reference", icon=":material/dictionary:")

if st.session_state.user_email:
    pg = st.navigation(
        {
            "Account": [logout_page],
            "Get started": [fundamentals_page],
            "Develop": [
                        architecture_page, 
                        appdesign_page, 
                        connectionSecretsAuth_page, 
                        customComponents_page, 
                        configurationAndTheming_page, 
                        apiRefence_page,
                        ],
        },
        position="sidebar",
        expanded=True
    )
else:
    pg = st.navigation([login_page])

pg.run()

#MULTIPAGE DOCUMENTATION:
#https://docs.streamlit.io/develop/concepts/multipage-apps/page-and-navigation 
#https://docs.streamlit.io/develop/concepts/multipage-apps/widgets 