import streamlit as st
from utils.state_sync import init_global
# INSTALLATION:
#python <= 3.12
#pip install streamlit
#streamlit run MyApp.py


# VARIABLES GLOBALES (COMPARTIDAS ENTRE PÁGINAS)
init_global("global_group", "A")
init_global("global_threshold", 50)
 
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    if st.button("Log in"):
        st.session_state.logged_in = True
        st.rerun()

def logout():
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()

login_page = st.Page(login, title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")

#Get started
fundamentals_page = st.Page("Get started/Fundamentals.py", title="Fundamentals", default=True)

#Develop
architecture_page = st.Page("Develop/Architecture_and_Execution.py", title="Architecture", icon=":material/dashboard:")
appdesign_page = st.Page("Develop/AppDesign.py", title="AppDesign", icon=":material/brush:")

if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Account": [logout_page],
            "Get started": [fundamentals_page],
            "Develop": [architecture_page, appdesign_page],
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