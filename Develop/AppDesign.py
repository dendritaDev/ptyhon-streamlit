import streamlit as st
import pandas as pd
import numpy as np
import time
from threading import Thread
from models import Product, ApiClient

st.set_page_config(page_title="AppDesign", page_icon=":material/brush:")

st.title("AppDesign")
st.write("Librería de iconos:")
#icons: https://fonts.google.com/icons?icon.set=Material+Symbols&icon.style=Rounded
st.markdown(
    "**here:** "
    "[Material Symbols Rounded](https://fonts.google.com/icons?icon.set=Material+Symbols&icon.style=Rounded)"
)


st.link_button(
    "Abrir Material Symbols",
    "https://fonts.google.com/icons?icon.set=Material+Symbols&icon.style=Rounded"
)


st.header("1.Animate and update elements")
st.write("st.empty() sirve para renderizar algo en tiempo real y ver el progreso sin tener que hacer rerun de toda la página ")


# st.header("3.Dataframes")
if st.button("Iniciar simulación"):
    # 1) Panel de estado (actualizable)
    status = st.status("Inicializando...", expanded=True)
    status.update(label="Descargando datos...", state="running")

    # 2) Barra de progreso (actualizable)
    prog = st.progress(0)

    # 3) Placeholder para un bloque reescribible (métrica + pequeña tabla)
    ph = st.empty()

    # 4) Gráfico incremental con .add_rows()
    chart = st.line_chart(pd.DataFrame({"y": []}))

    # Simulación de datos/avance
    vals = []
    for i in range(101):
        # Simula trabajo
        time.sleep(0.02)

        # Actualiza progreso
        prog.progress(i)

        # Genera un nuevo dato
        new_val = (np.sin(i/10) + np.random.randn()*0.05) * 10 + 50
        vals.append(new_val)

        # dataframe y tablas se pueden actualizar sin rerun con add_rows
        chart.add_rows(pd.DataFrame({"y": [new_val]}))

        # 3) Reescribe un bloque completo dentro de st.empty()
        with ph.container():
            st.metric("Iteración", i)
            # Tabla pequeña con últimas 5 observaciones
            last = pd.DataFrame({"y": vals[-5:]})
            st.table(last)

        if i == 1:
            status.update(label="Procesando...", state="running")
        if i == 50:
            status.update(label="Mitad del proceso", state="running", expanded=False)

    # Cierre: limpia barra y marca estado completo
    status.update(label="Completado", state="complete", expanded=False)
    prog.empty()

    # 5) Toasts 
    st.toast("Proceso finalizado.")
    time.sleep(0.5)
    st.toast("Gráfico y tabla actualizados.")

else:
    st.info("Pulsa **Iniciar simulación** para ver las actualizaciones en vivo.")


st.header("2.Buttons")

st.write("Los buttons devuelven True o False. Cuando hacemos click se hace rerun y devuelve True, al siguiente rerun dará falso. Así que " \
"información que deba persistir en la pantalla, es mejor **no hacerla dependiente** de un click de un button: if st.button(...)")

st.subheader("Patrones recomendados")
st.write("1.Mensaje temporal")

animal_shelter = ['cat', 'dog', 'rabbit', 'bird']
animal = st.text_input('Type an animal')

if st.button('Check availability'):
    have_it = animal.lower() in animal_shelter
    if have_it:
        st.success('We have that animal!')

if st.button('pulsa este botón que no hace nada, pero como es un botón y se pulsa hace rerun y desaparece lo previo'): #si pulsamos este boton el mensaje st.success desaparece
    a = 1

st.write("2.Botón con estado usando st.session_state (PERSISTENTE)")
st.write("El botón cambia un flag en session_state, el contenido persiste aunque se pulse otro botón")

st.session_state.setdefault("clicked", False)

def click_button():
    st.session_state.clicked = True

st.button('Click me', on_click=click_button)

if st.session_state.clicked:
    st.write('Button clicked!')
    st.slider('Select a value')

st.write("3.Checkbox: Alterna un flag persistente y en base a esto se muestra o no algo")
st.session_state.setdefault("show_controls", False)

def toggle():
    st.session_state.show_controls = not st.session_state.show_controls

st.button("Toggle controls", on_click=toggle)

if st.session_state.show_controls:
    st.write("Controls ON")
    st.slider("Value")
else:
    st.write("Controls OFF")

st.subheader("Problemas Típicos:")
st.write("Leer un persistent data y despues usar un botón que lo modifica. Si no usamos callback o st.rerun(), el button al pulsarlo devuelve True y se re ejecuta la página de nuevo de arriba abajo, pero como primero leemos y printamos el persistent data y no se cambia hasta volver al buttón por eso permanece con el valor inicial y necesitamos otro rerun")
st.write("Solucion: Dos maneras de que un botón desencadene un rerun, callback o st.rerun. Recomendación --> usar callbacks")
st.session_state.setdefault("name", "John Doe")
st.subheader("nombre en persistent data: "+st.session_state["name"])

st.write("Callback:")

def change_name(name): 
    st.session_state["name"] = name

#callback hace el cambio del persistent data antes de que se actualice la página
st.button("Jane", on_click=change_name, args=("Jane Doe",))
st.button("John", on_click=change_name, kwargs={"name":"John Doe"})


st.write("button sin st.rerun():")
if st.button("Jane - without rerun"):
    st.session_state["name"] = "Jane Doe"
    
if st.button("John - without rerun"):
    st.session_state["name"] = "John Doe"
    
st.write("button con st.rerun():")
if st.button("Jane - with rerun"):
    st.session_state["name"] = "Jane Doe"
    st.rerun()
    
if st.button("John - with rerun"):
    st.session_state["name"] = "John Doe"
    st.rerun()


st.subheader("Botones que modificarn el valor de un widget")
st.write("si ya hemos renderizado un wdget, no podemos actualizar su clave y esperar que se modifique, con un botón que viene después de este widget")
st.write("solución: callback again")

left, right = st.columns(2)

with left:
    st.markdown("**Caso incorrecto (provoca excepción al pulsar):**")
    st.write("1) Se crea un text_input con key='name_widget_wrong'.")
    st.write("2) El botón intenta cambiar esa misma key DESPUÉS en este rerun.")
    st.text_input("Name (wrong)", key="name_widget_wrong")
    if st.button("Clear name (wrong)"):
        # Esto intenta modificar la clave del widget ya renderizado en este rerun.
        # Streamlit debería lanzar una StreamlitAPIException.
        st.session_state["name_widget_wrong"] = ""

with right:
    st.markdown("**Corrección 1 — Callback (recomendado):**")
    st.write("El callback se ejecuta antes del rerun, por lo que el widget ya arranca con el valor actualizado.")
    st.text_input("Name (callback)", key="name_widget_cb") 

    def set_empty_cb():
        st.session_state["name_widget_cb"] = ""

    st.button("Clear (callback)", on_click=set_empty_cb)

st.subheader("Proceso costoso → botón + session_state")
st.write("Cualquier cambio en un widget hace que se ejecute de arriba a abajo de nuevo todo, esto es un inconveniente cuando tenemos análisis pesados." \
"Par estos casos, lo mejor es guardar los resultados en data persistente y hacer que este proceso pesado de calculo solo se ejecute cuando se pulsa " \
"un botón, por ejemplo")

# Parámetros (cambian a menudo y provocan reruns)
size = st.selectbox("Tamaño", [1000, 5000, 20000])
add  = st.number_input("Sumar", 0, 10, 0)
_    = st.text_input("Notas (provoca reruns pero no recalcula nada)")

# Clave única del resultado para estos parámetros
run_key = f"{size}|{add}"

st.session_state.setdefault("results", {})  # dict: run_key -> DataFrame

def expensive(size, add):
    with st.spinner("Procesando..."):
        time.sleep(2)  # simula trabajo pesado
    # resultado cualquiera (p. ej., columna con rango + offset)
    return pd.DataFrame({"x": range(size), "y": [add]*size})

# 1) Ejecutar solo al pulsar el botón, guardar resultado
if st.button("Procesar"):
    st.session_state["results"][run_key] = expensive(size, add)
    st.success("Resultado guardado en session_state.")

# 2) Mostrar resultado si existe (reutiliza, no recalcula)
if run_key in st.session_state["results"]:
    st.info("Usando resultado guardado para estos parámetros.")
    st.dataframe(st.session_state["results"][run_key].head(10), use_container_width=True)
else:
    st.warning("Aún no hay resultado para estos parámetros. Pulsa Procesar.")

# (Opcional) limpiar todo
if st.button("Limpiar resultados"):
    st.session_state["results"].clear()
    st.rerun()

st.header("3.Dataframes")
st.subheader("Se pueden hacer un monton de cosas con dataframes, enseñar info, modificar, ver las modificaciones hechas...")
df = pd.DataFrame([
    {"command": "st.selectbox", "rating": 4, "is_widget": True,  "color": "red",  "when": pd.Timestamp("2025-10-30 09:00:00")},
    {"command": "st.balloons",  "rating": 5, "is_widget": False, "color": "blue", "when": pd.Timestamp("2025-10-31 18:30:00")},
    {"command": "st.time_input","rating": 3, "is_widget": True,  "color": "red",  "when": pd.Timestamp("2025-11-01 12:00:00")},
])

st.write("Dataframe **no editable**: st.dataframe")
st.dataframe(df, hide_index=True ,use_container_width=True)

st.write("Dataframe **editable**: st.data_editor, columnas obligatorias de escribir, min y max value para rating")

st.data_editor(
    df,
    column_config={
    "command":   st.column_config.TextColumn("Command", required=True, width="medium"),
    "rating":    st.column_config.NumberColumn("Rating", min_value=0, max_value=5, step=1),
    "is_widget": st.column_config.CheckboxColumn("Is widget?"),
    "color":     st.column_config.SelectboxColumn("Color", options=["red","blue","green"]),
    "when":      st.column_config.DatetimeColumn("When (Europe/Madrid)", timezone="Europe/Madrid"),
    },
    hide_index=True,
    use_container_width=True,
    num_rows="dynamic",  # permite +/− filas
)

st.subheader("También podemos printar listas, listas de diccionarios y diccionarios")
colors = st.data_editor(["red","green","blue"], num_rows="dynamic")
st.write("Colores:", colors)

# Lista de dicts
records = st.data_editor([
    {"name":"st.text_area","type":"widget"},
    {"name":"st.markdown","type":"element"},
])
st.write(records)

# Diccionario
d = st.data_editor({"st.text_area":"widget","st.markdown":"element"})
st.write(d)

st.header("4. Multithreading")
st.markdown("""
**A tener en cuenta:**
- No llames `st.*` dentro de hilos propios.
- Úsalo para `IO` o `cálculos pesados`
- Une los hilos con `join()` y no dejes hilos vivos tras el rerun.
""")


col_left, col_right = st.columns(2, gap="large")

with col_left:
    st.subheader("Tarea A")
    a_status = st.empty() 
with col_right:
    st.subheader("Tarea B")
    b_status = st.empty()

# --- Worker sin llamadas a st.* ---
class Worker(Thread):
    def __init__(self, label: str, delay: float):
        super().__init__(daemon=True)
        self.label = label
        self.delay = delay
        self.result = None

    def run(self):
        # Simula trabajo de IO (no llamar st.* aquí)
        total = 0
        for i in range(1, 6):
            time.sleep(self.delay)  # espera "red"
            total += i
        self.result = f"{self.label}: total={total}, delay={self.delay}s"

# --- Lanzar tareas al pulsar el botón ---
if st.button("Ejecutar tareas en paralelo"):
    a = Worker("A", 0.2)
    b = Worker("B", 0.3)
    a.start() 
    b.start()


    a_open, b_open = True, True
    while a_open or b_open:
        if a_open:
            if not a.is_alive():
                a_status.success(a.result)
                a_open = False
            else:
                a_status.info("trabajando")
        if b_open:
            if not b.is_alive():
                b_status.success(b.result)
                b_open = False
            else:
                b_status.info("trabajando")

        time.sleep(0.1)

    # Garantiza que no quedan hilos vivos:
    a.join()
    b.join()

    st.success("Tareas finalizadas.")


st.subheader("5. Using custom Python classes in your Streamlit app")
st.markdown("""
- **Mueve tus clases a un módulo externo.** Si la clase viene de módulo externo (y no la editas durante la sesión), puedes guardar instancias en `st.session_state`.
- **Clases de datos:** guarda **valores** (dict/JSON) en Session State y **reconstruye** la instancia cuando la necesites.
- **Patrón Singleton:** usa `@st.cache_resource` para clientes/conexiones (recurso único por parámetros).
""")

# === A) Módulo externo: isinstance estable ===
st.markdown("**A) Módulo externo**")
if "p_obj" not in st.session_state:
    st.session_state.p_obj = Product(1, "Widget", 9.90)   # OK: clase en módulo externo
st.write("isinstance estable:", isinstance(st.session_state.p_obj, Product))

st.divider()

# === B) Serializa valores (dict) y reconstruye ===
st.markdown("**B) Serializa valores (dict) y reconstruye**")
if "p_data" not in st.session_state:
    st.session_state.p_data = Product(2, "Gadget", 14.50).to_dict()  # guardar dict

c1, c2, c3 = st.columns(3)
st.session_state.p_data["name"]  = c1.text_input("Nombre",  st.session_state.p_data["name"])
st.session_state.p_data["price"] = c2.number_input("Precio", 0.0, 10_000.0, float(st.session_state.p_data["price"]), 0.1)
st.session_state.p_data["id"]    = c3.number_input("ID", 0, 1_000_000, int(st.session_state.p_data["id"]), 1)

# Reconstruir cuando haga falta
restored = Product.from_dict(st.session_state.p_data)
st.write("Restaurado (Product):", restored.to_dict())

st.divider()

# === C) Singleton con cache_resource ===
st.markdown("**C) Singleton `@st.cache_resource`**")
client = ApiClient.get("https://api.example.com")
st.write("id(cliente):", id(client))
