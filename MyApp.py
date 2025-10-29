import streamlit as st
import pandas as pd
import numpy as np
import time


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


st.title("2.Develop - Concepts") #https://docs.streamlit.io/develop/concepts/architecture 
st.title("Architecture and execution")


# Casos típicos para st.cache_data:

    # Cargar CSVs grandes.

    # Consultar una API externa con requests.

    # Ejecutar una inferencia cara de ML y devolver resultados (listas, dicts).

    # Hacer transformaciones pesadas de pandas


# Casos típicos para st.cache_resources:

    # Cosas no serializables o objetos que permanecen vivos: conexión a BD, modelos de ML cargados en memoria, fichero abierto I/O...

# st.cache_data devuelve copias de algo en vez de recalcularlo, mientras que
# st.cache_resources utiliza el mismo objeto, SINGLETON

#st.session_state es un diccionario donde se puedne guardar valores que persisten en esa sesión (tab), cada tab es una sesión nueva. P.e una variable local que queremos que cada vez que se ejecuta algo sume un +1
#también hay callbacks para la UI:
if "count" not in st.session_state:
    st.session_state.count = 0

def change_counter(delta=0):
    st.session_state.count += delta

st.button("Añadir 5", on_click=change_counter, kwargs={"delta": 5}) #tmb se podria args=(5). Args -> parametros por posicion. kwargs -> parametros por nombre de parametro explicito
st.button("Añadir valor actual", on_click=change_counter, kwargs={"delta": st.session_state.count})
st.button("Restar 1", on_click=change_counter, kwargs={"delta": -1})

st.write("Count =", st.session_state.count)

#también se pueden guardar informacion de widgets en reruns con session_state:
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

#FORMS
#Para evitar que cada vez que se cambia un widget se actualice todo, hay los forms quepermiten cambiar varios valores 
#y hasta que no se le da a enviar no se vuelve a ejecutar el script.

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

#podemos guardar los valores con session_state y usar callback en el submit button del form (solo este tipo de button puede usar callbacks en un form):
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

#widget behavior: dos widgets idénticos con los mismos argumentos (misma etiqueta, mismos límites, mismo key o sin key, etc.) en la misma página, Streamlit no sabe diferenciarlos y lanza DuplicateWidgetID. Solución: darles key distintos. 
# ERROR:
# st.button("OK")
# st.button("OK")

# CORRECTO
st.button("OK", key="privacy")
st.button("OK", key="terms")

# Order of operations:
# When a user interacts with a widget, the order of logic is:
    # Its value in st.session_state is updated.
    # The callback function (if any) is executed.
    # The page reruns with the widget function returning its new value.
# If the callback function writes anything to the screen, that content will appear above the rest of the page. 
# A callback function runs as a prefix to the script rerunning. Consequently, that means anything written 
# via a callback function will disappear as soon as the user performs their next action. Other widgets 
# should generally not be created within a callback function.

#Using a callback function with a form requires consideration of this order of operations.

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



#Reseteo de los Widgets:
#Un widget recuerda su valor mientras:
    # Siga existiendo en la página en cada rerun.
    # Sus parámetros clave (etiqueta, rango, key, etc.) no cambien.
    # Si cambias alguno de esos parámetros, Streamlit interpreta que es “otro” widget, 
    # y lo resetea al valor por defecto. Ejemplo:
minimum = st.number_input("Mínimo", 1, 5)
maximum = st.number_input("Máximo", 6, 10, 10)

# st.slider("Sin default, sin key", minimum, maximum)
st.slider("Sin default, con key", minimum, maximum, key="a1")
# st.slider("Con default, sin key", minimum, maximum, value=5)
st.slider("Con default, con key", minimum, maximum, value=5, key="b1")


#Vida y limpieza de los widgets~: Importante para varias paginas
#Si en un rerun NO llamas a un widget que antes sí existía, Streamlit lo elimina de memoria 
# y también borra su valor asociado en st.session_state.

#Eso quiere decir que si escondes temporalmente un widget (por ejemplo cambias de página o 
# entras en una if que ya no lo muestra), cuando vuelva a aparecer, será “nuevo” y habrá 
# perdido su valor anterior.

    #Para solucionar esto, arriba de todo de los scripts podemos inicializar de nuevo los valores, para que
    #streamlit detecte como que los estamos "usando", aunque pueda ser que no y no lo elimine. P.e:
st.session_state.count = st.session_state.count

    #Posiblemente lo ideal seria llamar a una función y en esa función meter todas las session_state que vayamos creando
    #así lo tenemos todo centralizado

#Slider dinámico sin perder valor:
    #Si hacemos que min y max sean dinamicas, para que el valor no se resetee cuando queda fuera del slider
    #tenemos que:
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



#NEXT -> https://docs.streamlit.io/develop/concepts/multipage-apps 