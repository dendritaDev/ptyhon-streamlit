import streamlit as st

def init_global(global_key: str, default):
    """Asegura que la clave global exista con un valor por defecto."""
    st.session_state.setdefault(global_key, default) #setDefault solo escribe si no existe ya la clave

def mirror_global_to_local(local_key: str, global_key: str):
    """
    Copia SIEMPRE el valor global al local.
    LLAMAR ANTES de renderizar el widget con key=local_key.
    """
    st.session_state[local_key] = st.session_state[global_key]

def bind_local_to_global(local_key: str, global_key: str):
    """
    Callback para widgets locales: al cambiar, copia local -> global.
    El siguiente rerun volverá a hacer global -> local (mirror),
    garantizando que el widget muestre el valor correcto en cualquier página.
    """
    def _sync():
        st.session_state[global_key] = st.session_state[local_key]
    return _sync