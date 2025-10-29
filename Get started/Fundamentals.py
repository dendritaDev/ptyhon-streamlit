import streamlit as st
import pandas as pd
import numpy as np
import time
from utils.state_sync import bind_local_to_global, init_global, mirror_global_to_local

st.set_page_config(page_title="Fundamentals", page_icon=":material/school:")

st.title("Fundamentals")
st.write("Esta página tiene **controles locales** que sincronizan con el **estado global**.")

#---------------------------------
#SINCRONIZACIÓN VARIABLES GLOBALES

# --- Garantiza que existen las claves globales (por si se entra directo por URL) ---
init_global("global_group", "A")
init_global("global_threshold", 50)

# --- ANTES de dibujar widgets: copia global -> local SIEMPRE ---
mirror_global_to_local("_local_group", "global_group")
mirror_global_to_local("_local_threshold", "global_threshold")


with st.expander("Controles locales (sincronizados con el estado global)", expanded=True):
    st.selectbox(
        "Group (local)",
        ["A", "B", "C"],
        key="_local_group",
        on_change=bind_local_to_global("_local_group", "global_group")
    )
    st.slider(
        "Threshold (local)",
        0, 100,
        key="_local_threshold",
        on_change=bind_local_to_global("_local_threshold", "global_threshold")
    )
    st.caption("Cambiar aquí actualiza el estado global y afectará a otras páginas.")

st.write("---")
st.subheader("Datos dependientes del estado global")
np.random.seed(0)
df = pd.DataFrame({
    "group": np.random.choice(["A","B","C"], size=200),
    "score": np.random.randint(0, 101, size=200),
})

mask = (df["group"] == st.session_state["global_group"]) & (df["score"] >= st.session_state["global_threshold"])
st.write(f"Filtro activo → group = **{st.session_state['global_group']}**, threshold ≥ **{st.session_state['global_threshold']}**")
st.dataframe(df[mask].head(20), use_container_width=True)



#---------------------------------

st.title("1.Get started - Fundamentals") #https://docs.streamlit.io/get-started/fundamentals
st.write("Esta es mi primera app.")
st.line_chart({"series A": [1, 5, 2, 6, 3, 9]})

st.title("Tabla con magia")

df = pd.DataFrame({
    "Columna 1": [1, 2, 3, 4],
    "Columna 2": [10, 20, 30, 40]
})

df

st.header("Ejemplo visualización rápida")

# Datos aleatorios
df = pd.DataFrame(
    np.random.randn(20, 2),
    columns=["x", "y"]
)

st.subheader("DataFrame interactivo")
st.dataframe(df)
st.subheader("Tabla estática")
st.table(df)

st.subheader("Line chart de la columna x")
st.line_chart(df["x"])

st.subheader("Bar chart de la columna y")
st.bar_chart(df["y"])

dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))

st.dataframe(dataframe.style.highlight_max(axis=0))

map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

st.map(map_data)

x = st.slider('x')  # 👈 this is a widget
st.write(x, 'squared is', x * x)

st.text_input("Your name", key="name")

# You can access the value at any point with:
st.session_state.name


asd = st.checkbox('Show dataframe')

if asd:
    chart_data = pd.DataFrame(
       np.random.randn(20, 3),
       columns=['a', 'b', 'c'])

    chart_data

df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
    })

option = st.selectbox(
    'Which number do you like best?',
     df['first column'])

'You selected: ', option

# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home phone', 'Mobile phone')
)

# Add a slider to the sidebar:
add_slider = st.sidebar.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0)
)

left_column, right_column = st.columns(2)
# You can use a column just like st.sidebar:
left_column.button('Press me!')

# Or even better, call Streamlit functions inside a "with" block:
with right_column:
    chosen = st.radio(
        'Sorting hat',
        ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
    st.write(f"You are in {chosen} house!")

'Starting a long computation...'

# Add a placeholder
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(10):
  # Update the progress bar with each iteration.
  latest_iteration.text(f'Iteration {i+1}')
  bar.progress((i + 1)*10)
  time.sleep(0.1)

'...and now we\'re done!'

#Cache (st.cache_data) guarda resultados de funciones caras y los comparte entre usuarios/sesiones con la misma entrada. -->
#Session State guarda datos específicos de una sesión concreta de un usuario y no se comparte entre otros usuarios/sesiones.


