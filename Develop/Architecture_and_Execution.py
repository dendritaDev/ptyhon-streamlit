import streamlit as st
import pandas as pd
import numpy as np
from utils.state_sync import mirror_global_to_local, bind_local_to_global, init_global


st.set_page_config(page_title="Architecture", page_icon=":material/dashboard:")

st.title("Architecture")
st.write("Esta página tiene **sus propios controles locales**, sincronizados con el **mismo estado global**.")

#---------------------------------
# SINCRONIZACIÓN VARIABLES GLOBALES → TEXTO EN PANTALLA
st.subheader("Sincronización con estado global")
st.markdown("""
Esta página usa un patrón **global ↔ local** para que varios módulos compartan filtros:

- `init_global(key, default)`: garantiza que la clave **global** exista (una sola vez por sesión).
- `mirror_global_to_local(local_key, global_key)`: **antes de dibujar** los widgets, copia **global → local** para que la UI muestre el último valor consolidado.
- `bind_local_to_global(local_key, global_key)`: callback `on_change` que sube cambios **local → global** cuando el usuario interactúa.
""")
# --- Garantiza claves globales (por acceso directo) ---
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

st.write("---")
st.subheader("Resumen por grupo condicionado por el estado global")
np.random.seed(0)
df = pd.DataFrame({
    "group": np.random.choice(["A","B","C"], size=300),
    "score": np.random.randint(0, 101, size=300),
})

st.write(f"Threshold global ≥ **{st.session_state['global_threshold']}**. Grupo global actual: **{st.session_state['global_group']}**.")

st.write("Vista específica del grupo global:")
st.dataframe(
    df[(df["group"] == st.session_state["global_group"]) & (df["score"] >= st.session_state["global_threshold"])].head(15),
    use_container_width=True
)


#---------------------------------
# CACHE: CUÁNDO USAR CADA UNA → TEXTO EN PANTALLA
st.subheader("Caching: `st.cache_data` vs `st.cache_resource`")
st.markdown("""
**Casos típicos para `st.cache_data`** (devuelve **copias** memoizadas):
- Cargar **CSVs** grandes.
- Consultar una **API** externa con `requests`.
- Ejecutar una inferencia **costosa** de ML (listas/dicts como resultado).
- Transformaciones **pesadas** de pandas.

**Casos típicos para `st.cache_resource`** (mantiene un **objeto vivo** / singleton):
- Conexiones a **BD**, clientes de API persistentes.
- **Modelos** de ML cargados en memoria.
- Manejadores de **ficheros**/I/O u otros recursos no serializables.

**Diferencia clave**: `cache_data` evita recomputar **datos** devolviendo copias; `cache_resource` reutiliza **el mismo objeto** (patrón **singleton**).
""")

# SESSION STATE + CALLBACKS → TEXTO EN PANTALLA
st.subheader("Session State: contador y callbacks")
st.markdown("""
- `st.session_state` guarda valores **persistentes por pestaña** (una sesión por tab).
- Los **callbacks** (`on_click`, `on_change`) mutan estado **antes** del rerun.
- `args` pasa argumentos **por posición**; `kwargs` por **nombre** (útil para claridad).
""")

if "count" not in st.session_state:
    st.session_state.count = 0

def change_counter(delta=0):
    st.session_state.count += delta

st.button("Añadir 5", on_click=change_counter, kwargs={"delta": 5}) #tmb se podria args=(5). Args -> parametros por posicion. kwargs -> parametros por nombre de parametro explicito
st.button("Añadir valor actual", on_click=change_counter, kwargs={"delta": st.session_state.count})
st.button("Restar 1", on_click=change_counter, kwargs={"delta": -1})

st.write("Count =", st.session_state.count)


# WIDGETS CON MEMORIA (key) → TEXTO EN PANTALLA
st.subheader("Guardar el valor de un widget entre reruns (key)")
st.markdown("""
Asigna `key` al widget cuando:
- Deba **recordar su valor** entre reruns.
- Quieras **modificarlo desde callbacks**.
- Su valor se use en **múltiples sitios**.
""")

if "celsius" not in st.session_state:
    # set the initial default value of the slider widget
    st.session_state.celsius = 50.0

st.slider(
    "Temperature in Celsius",
    min_value=-100.0,
    max_value=100.0,
    key="celsius" # Guardamos una key para widget de UI, cuando: necesitamos que el widget tenga memoria entre reruns, cuando lo queramos modificar desde callbaks o cuando su valor se use en múltiples sitios. Si los guardamos todos, podemos tener boton de reset despues y resetear todo
)

# This will get the value of the slider widget
st.write(st.session_state.celsius)

# FORMS → TEXTO EN PANTALLA
st.subheader("Forms: agrupar cambios y enviar de una vez")
st.markdown("""
Los **forms** retrasan el rerun hasta pulsar **Submit**. Útiles para confirmar varios cambios a la vez.
El bloque `with st.form(...):` es un **context manager** (gestiona apertura/cierre automáticamente).
""")

with st.form("suma"): #with manera de python de manejar automaticamente memoryleaks rollo cuando abres cierras un doc de I/O. Se usa para: forms, columnas y container
    a = st.number_input("a", step=1.0)
    b = st.number_input("b", step=1.0)
    submitted = st.form_submit_button("Sumar")

if submitted:
    st.write("Resultado:", a + b)

# --

def get_data():
    df = pd.DataFrame({
        "lat": np.random.randn(200) / 50 + 37.76,
        "lon": np.random.randn(200) / 50 + -122.4,
        "team": ['A','B']*100
    })
    return df

if st.button('Generate new points'):
    st.session_state.df = get_data()
if 'df' not in st.session_state:
    st.session_state.df = get_data()
df = st.session_state.df

with st.form("my_form"):
    header = st.columns([1,2,2])
    header[0].subheader('Color')
    header[1].subheader('Opacity')
    header[2].subheader('Size')

    row1 = st.columns([1,2,2])
    colorA = row1[0].color_picker('Team A', '#0000FF')
    opacityA = row1[1].slider('A opacity', 20, 100, 50, label_visibility='hidden')
    sizeA = row1[2].slider('A size', 50, 200, 100, step=10, label_visibility='hidden')

    row2 = st.columns([1,2,2])
    colorB = row2[0].color_picker('Team B', '#FF0000')
    opacityB = row2[1].slider('B opacity', 20, 100, 50, label_visibility='hidden')
    sizeB = row2[2].slider('B size', 50, 200, 100, step=10, label_visibility='hidden')

    st.form_submit_button('Update map')

alphaA = int(opacityA*255/100)
alphaB = int(opacityB*255/100)

df['color'] = np.where(df.team=='A',colorA+f'{alphaA:02x}',colorB+f'{alphaB:02x}')
df['size'] = np.where(df.team=='A',sizeA, sizeB)

st.map(df, size='size', color='color')

# CALLBACK EN SUBMIT DE FORM → TEXTO EN PANTALLA
st.subheader("Callback en submit de form")
st.markdown("""
Los **form_submit_button** admiten `on_click`. Ejemplo: calcular y **persistir** una suma en `session_state`.
""")

if 'sum' not in st.session_state:
    st.session_state.sum = ''

def sum():
    result = st.session_state.a + st.session_state.b
    st.session_state.sum = result

col1,col2 = st.columns(2)
col1.title('Sum:')
if isinstance(st.session_state.sum, float):
    col2.title(f'{st.session_state.sum:.2f}')

with st.form('addition'):
    st.number_input('a', key = 'a')
    st.number_input('b', key = 'b')
    st.form_submit_button('add', on_click=sum)

# WIDGET BEHAVIOR: CLAVES ÚNICAS → TEXTO EN PANTALLA
st.subheader("Widget behavior: evita DuplicateWidgetID")
st.markdown("""
Dos widgets **idénticos** (misma etiqueta, mismos límites, **misma key** o sin key) en la misma página → **DuplicateWidgetID**.  
**Solución**: asigna **keys distintas**.
""")

# ERROR:
# st.button("OK")
# st.button("OK")

# CORRECTO
st.button("OK", key="privacy")
st.button("OK", key="terms")

# ORDEN DE EJECUCIÓN → TEXTO EN PANTALLA
st.subheader("Orden de operaciones en widgets")
st.markdown("""
1. Se actualiza el valor en `st.session_state`.
2. Se ejecuta el **callback** (si existe).
3. La página **rerun** y la función del widget devuelve el nuevo valor.

**Nota**: Lo que escribas **desde un callback** aparece **antes** del resto de la página y **desaparece** con la siguiente interacción.  
Evita **crear widgets dentro de callbacks**.
""")
st.caption("En forms, recuerda este orden: el callback del submit ocurre antes del rerun.")

# Ejemplo de asistencia (callback + session_state)
if "attendance" not in st.session_state:
    st.session_state.attendance = set()


def take_attendance():
    if st.session_state.namee in st.session_state.attendance:
        st.info(f"{st.session_state.namee} has already been counted.")
    else:
        st.session_state.attendance.add(st.session_state.namee)


with st.form(key="my_form2"):
    st.text_input("Name", key="namee")
    st.form_submit_button("I'm here!", on_click=take_attendance)



# RESETEO DE WIDGETS → TEXTO EN PANTALLA
st.subheader("Reseteo de widgets: cuándo pierden el valor")
st.markdown("""
Un widget conserva su valor mientras:
- **Siga existiendo** en la página en cada rerun.
- Sus parámetros clave (etiqueta, rango, `key`, etc.) **no cambien**.

Si alguno cambia, Streamlit lo trata como **otro widget** y lo resetea.
""")
minimum = st.number_input("Mínimo", 1, 5)
maximum = st.number_input("Máximo", 6, 10, 10)

# st.slider("Sin default, sin key", minimum, maximum)
st.slider("Sin default, con key", minimum, maximum, key="a1")
# st.slider("Con default, sin key", minimum, maximum, value=5)
st.slider("Con default, con key", minimum, maximum, value=5, key="b1")


#Vida y limpieza de los widgets~: Importante para varias paginas
# VIDA Y LIMPIEZA DE WIDGETS ENTRE RERUNS/PÁGINAS → TEXTO EN PANTALLA
st.subheader("Vida y limpieza de widgets (entre páginas/condiciones)")
st.markdown("""
Si en un rerun **no** creas un widget que **antes sí existía**, Streamlit lo **borra de memoria** y también su valor en `st.session_state`.  
Al volver a mostrarlo, será **nuevo** (valor por defecto).

**Sugerencia**: inicializa valores de `session_state` al comienzo de tus scripts o centraliza esta lógica en una función común.
""")
st.session_state.count = st.session_state.count
st.caption("Ejemplo de 'tocar' una clave para que Streamlit la considere usada en este rerun.")


# SLIDER DINÁMICO SIN PERDER VALOR → TEXTO EN PANTALLA
st.subheader("Slider dinámico sin perder valor cuando cambian min/max")
st.markdown("""
Si `min` y `max` cambian dinámicamente, el valor del slider puede quedar fuera de rango y **resetearse**.  
**Solución**: **ajusta (clamp)** el valor a `[min, max]` **antes** de dibujar el slider.
""")
# Valor por defecto
if "z" not in st.session_state:
    st.session_state.z = 5

min_val = st.number_input("Min", 1, 5, key="min_z")
max_val = st.number_input("Max", 6, 10, 10, key="max_z")

def clamp_slider_value():
    # Nos aseguramos de que st.session_state.a esté dentro de [min_val, max_val]
    st.session_state.z = max(min_val, min(max_val, st.session_state.z))

# Ajusta antes de dibujar el slider
clamp_slider_value()

st.slider("A", min_val, max_val, key="z") 
