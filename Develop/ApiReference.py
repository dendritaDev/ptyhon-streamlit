import io
import json
import time
import numpy as np
import pandas as pd
import streamlit as st
from annotated_text import annotated_text #pip install st-annotated-text
import plotly.express as px #pip install plotly

st.set_page_config(page_title="API Reference", page_icon=":material/dictionary:")
st.header("API REFERENCE")

# Datos de ejemplo
df = pd.DataFrame({
    "category": list("ABCDEFGH"),
    "value": [7, 5, 6, 3, 8, -3 ,4, 6],
})
df_map = pd.DataFrame({
    "lat": [40.4168, 41.3879, 37.3891], 
    "lon": [-3.7038, 2.1699, -5.9845],
    "name": ["Madrid", "Barcelona", "Sevilla"],
})

# Helpers para imports opcionales sin romper la página
def _try_import(mod, pip_hint):
    try:
        return __import__(mod)
    except Exception as e:
        st.info(f"Para ejecutar este ejemplo instala: `{pip_hint}`")
        return None

# ---------------------------------------
# WRITE & MAGIC
# ---------------------------------------
st.subheader("Write & Magic")

st.write("**st.write** acepta casi cualquier cosa:")
st.write("Hola **mundo** desde `st.write`")
st.write({"clave": 123, "otra": [1,2,3]})
st.write(df)

st.write("**st.write_stream** con un generador (typewriter):")
def _gen():
    for ch in "Streaming… listo! Refresca la página para ver el efecto animacion escritura":
        yield ch
        time.sleep(0.02)
st.write_stream(_gen)

# ---------------------------------------
# TEXT ELEMENTS
# ---------------------------------------
st.subheader("Text elements")
st.title("st.title — Título")
st.header("st.header — Cabecera")
st.subheader("st.subheader — Subcabecera")
st.badge("st.badge('New')")

st.caption("st.caption — texto pequeño:")
st.code("a = 1234  # st.code", language="python")

st.write("st.latex — para expresiones matemáticas:")
st.latex(r"\int a x^2 \, dx = \frac{a}{3}x^3 + C")

st.write("st.help — escribe la documentacion del st. que le pases dentro")
st.help(st.write)

st.write("st.html — render HTML simple (no JS externo):")
st.html("<p><strong>HTML</strong> básico en Streamlit.</p>")

st.write("st.divider display a horizontal rule:")
st.divider()

st.write("st.annotated_text:")
annotated_text(
    "This ",
    ("is", "verb"),
    " some ",
    ("annotated", "adj"),
    ("text", "noun"),
    " for those of ",
    ("you", "pronoun"),
    " who ",
    ("like", "verb"),
    " this sort of ",
    ("thing", "noun"),
    "."
)


# ---------------------------------------
# DATA ELEMENTS
# ---------------------------------------
st.subheader("Data elements")
st.write("st.dataframe — tabla interactiva:")
st.dataframe(df, hide_index=True)

st.write("st.data_editor — editable, con filas dinámicas:")
edited = st.data_editor(
    df.copy(),
    num_rows="dynamic",
    key="api_editor",
    column_config={"value": st.column_config.NumberColumn("Value", min_value=0)}
)
st.json({"edited_rows": len(edited)})

st.write("st.table — tabla estática:")
st.table(df.head(3))

st.write("st.metric — KPIs:")
col1, col2, col3 = st.columns(3)
col1.metric("Ventas", 420, 12)
col2.metric("NPS", 56, -3)
col3.metric("Users", "1.2k", "32")

st.write("st.json — JSON pretty-print")
st.json({"key": "value", "nested": {"a": 1}})

st.write("**important third components: streamlit-extras:**")
st.markdown(
    "[streamlit-extras](https://extras.streamlit.app/)"
)

st.write("st.code:")
st.code("""
if not st.user.is_logged_in:
    st.button("Log in with Google", on_click=st.login)
    st.stop()
st.button("Log out", on_click=st.logout)
st.write(f"Welcome! {st.user.name}")
""", language="python")
# ---------------------------------------
# CHART ELEMENTS
# ---------------------------------------
st.subheader("Chart elements")

st.write("Charts simples (usan datos tabulares):")
st.area_chart(df, x="category", y="value", height=180)
st.bar_chart(df, x="category", y="value", height=180)
st.line_chart(df, x="category", y="value", height=180)
st.scatter_chart(df.assign(x=np.arange(len(df))), x="x", y="value", height=180)

st.write("st.map — puntos en mapa")
st.map(df_map, size=10)

# Matplotlib (opcional)
mpl = _try_import("matplotlib.pyplot", "pip install matplotlib")
if mpl:
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    ax.plot(df["value"], marker="o")
    ax.set_title("Matplotlib figure")
    st.pyplot(fig, clear_figure=True)

# Vega-Lite (sin dependencias; spec directa)
st.write("st.vega_lite_chart — spec sin Altair")
spec = {
    "mark": "bar",
    "encoding": {
        "x": {"field": "category", "type": "nominal"},
        "y": {"field": "value", "type": "quantitative"},
        "color": {"field": "category", "type": "nominal"},
    },
    "data": {"values": df.to_dict(orient="records")},
}
st.vega_lite_chart(spec, use_container_width=True)

# Plotly (opcional)
st.write("Plotly chart:")
if px:
    fig = px.bar(df, x="category", y="value", color="category")
    st.plotly_chart(fig, use_container_width=True)

# PyDeck (opcional)
pydeck = _try_import("pydeck", "pip install pydeck")
if pydeck:
    import pydeck as pdk
    layer = pdk.Layer("ScatterplotLayer", data=df_map, get_position="[lon, lat]", get_radius=5_000)
    view_state = pdk.ViewState(latitude=40.4, longitude=-3.7, zoom=4)
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state), use_container_width=True)

# GraphViz (no requiere instalar python-graphviz)
st.graphviz_chart("""
digraph {
  A -> B; B -> C; A -> C;
}
""")

# ---------------------------------------
# INPUT WIDGETS
# ---------------------------------------
st.subheader("Input widgets")

st.write("Botones, links y navegación:")
clicked = st.button("st.button — Click me", key="api_btn")
st.link_button("st.link_button — Ir a Streamlit", "https://streamlit.io")
st.page_link("Develop/AppDesign.py", label="st.page_link — AppDesign", icon="🏠")

st.write("Checks, radios, selects:")
agree = st.checkbox("st.checkbox — Acepto", key="api_chk")
color = st.color_picker("st.color_picker — Color:", key="api_color")
rating = st.feedback("stars", key="api_feedback")  # 1..5 o None

tags = st.pills("st.pills — Tags:", ["Sports", "AI", "Politics"], key="api_pills")
choice_radio = st.radio("st.radio — Pick one:", ["cats", "dogs"], key="api_radio")
options = ["North", "East", "South", "West"]
st.write("st.segmented_control:")
selection = st.segmented_control(
    "Directions", options, selection_mode="multi"
)
choice_select = st.selectbox("st.selectbox — Pick one:", ["cats", "dogs"], key="api_select")
st.write("st.multiselect:")
options = st.multiselect(
    "What are your favorite colors?",
    ["Green", "Yellow", "Red", "Blue"],
    default=["Yellow", "Red"],
)
size = st.select_slider("st.select_slider — Talla:", ["S", "M", "L"], key="api_sel_slider")
activated = st.toggle("st.toggle — Activate:", key="api_toggle")

num = st.number_input("st.number_input — número", 0, 10, key="api_num")
rng = st.slider("st.slider — rango", 0, 100, (25, 75), key="api_slider")

date = st.date_input("st.date_input — fecha", key="api_date")
tm = st.time_input("st.time_input — hora", key="api_time")

prompt = st.chat_input("st.chat_input — di algo")
if prompt:
    st.write(f"Usuario envía: {prompt}")

text_area = st.text_area("st.text_area — multi-línea", key="api_text_area")
text_input = st.text_input("st.text_input — single-line", key="api_text_input")

st.write("Archivos / media desde input:")
uploaded = st.file_uploader("st.file_uploader — CSV", type=["csv"], key="api_upl")
if uploaded is not None:
    st.write(f"Subido: {uploaded.name} ({uploaded.size} bytes)")

# Audio / cámara (pueden depender del navegador)
st.audio_input("st.audio_input — grabar micrófono", key="api_audio_in")
st.camera_input("st.camera_input — tomar foto", key="api_cam")

# ---------------------------------------
# MEDIA ELEMENTS
# ---------------------------------------
st.subheader("Media elements")

st.write("st.image — desde array")
arr = (np.random.rand(120, 160, 3) * 255).astype(np.uint8)
st.image(arr, caption="Imagen random 160x120")

# Logo (usa ./static/cat.png si existe)
st.write("st.logo — requiere un archivo o URL")
import os
if os.path.exists("static/cat.png"):
    st.logo("static/cat.png")
else:
    st.info("Pon una imagen en `static/cat.png` para ver `st.logo`.")

# PDF (usa ./static/sample.pdf si existe)
if os.path.exists("static/sample.pdf"):
    st.pdf("static/sample.pdf")
else:
    st.info("Crea `static/sample.pdf` (por ejemplo, cualquier PDF) para ver `st.pdf`.")

# Audio — generamos un tono 440Hz 0.5s
sr = 16_000
t = np.linspace(0, 0.5, int(sr*0.5), endpoint=False)
wave = (0.1*np.sin(2*np.pi*440*t)).astype(np.float32)
st.audio(wave, sample_rate=sr)

# Video — normalmente usas archivo o URL
st.info("Para `st.video`, pasa una ruta local o URL a un mp4. Ej.: `st.video('app/static/demo.mp4')`")

# ---------------------------------------
# LAYOUTS & CONTAINERS
# ---------------------------------------
st.subheader("Layouts & containers")

st.write("st.columns")
c1, c2 = st.columns(2)
c1.write("Columna 1")
c2.write("Columna 2")

st.write("st.container (orden controlado)")
ct = st.container()
st.write("Esto se muestra después")
ct.write("Esto se mostró primeroo")
ct.write("…y esto segundo")

st.write("st.dialog (modal)")
@st.dialog("Sign up")
def _modal():
    st.text_input("Name", key="api_modal_name")
    st.text_input("Email", key="api_modal_email")
if st.button("Abrir modal", key="api_open_modal"):
    _modal()

st.write("st.empty — placeholder")
placeholder = st.empty()
placeholder.write("Esto será reemplazado en 1s…")
time.sleep(0.2)
placeholder.write("Reemplazado.")

st.write("st.expander")
with st.expander("Abrir para ver más"):
    st.write("Contenido extra")

st.write("st.popover")
with st.popover("Settings"):
    st.checkbox("Show completed", key="api_popover_chk")

st.sidebar.write("st.sidebar — vive en la barra lateral")
st.sidebar.button("Click me!", key="api_sidebar_btn")

# st.write("st.space — separaciones")
# st.space(size="small")

st.write("st.tabs")
tab1, tab2 = st.tabs(["Tab 1", "Tab 2"])
tab1.write("Contenido de Tab 1")
tab2.write("Contenido de Tab 2")

# ---------------------------------------
# CHAT ELEMENTS
# ---------------------------------------
st.subheader("Chat elements")
with st.chat_message("user"):
    st.write("Hola 👋 (mensaje del usuario)")

st.write("st.status — progreso de tareas largas")
with st.status("Procesando…", expanded=False) as status:
    for _ in range(3):
        time.sleep(0.2)
    status.update(label="Listo", state="complete")

# ---------------------------------------
# STATUS ELEMENTS
# ---------------------------------------
st.subheader("Status elements")

st.write("st.progress (rápido para la demo)")
prog = st.progress(0)
for i in range(0, 101, 20):
    time.sleep(0.05)
    prog.progress(i)

with st.spinner("st.spinner — espera breve…"):
    time.sleep(0.8)

st.toast("st.toast — ¡Hola!", icon="✅")
st.success("st.success — OK")
st.info("st.info — Info")
st.warning("st.warning — Atención")
st.error("st.error — Error")

try:
    raise RuntimeError("Ejemplo de excepción")
except Exception as e:
    st.exception(e)

st.balloons()
st.snow()

# ---------------------------------------
# APP LOGIC & CONFIG
# ---------------------------------------
st.subheader("App logic & configuration")

st.write("st.switch_page (snippet):")
st.code("st.switch_page('pages/my_page.py')", language="python")

st.write("st.dialog, st.form, st.fragment — ejemplo mínimo de fragment con refresco:")
@st.fragment(run_every="2s")
def small_fragment():
    st.write(f"Tick: {int(time.time()) % 100}")
small_fragment()

st.write("st.rerun / st.stop — *opt-in*:")
if st.button("Demo st.rerun()", key="api_rerun_btn"):
    st.rerun()
# No hacemos st.stop aquí para no detener toda la página
