import streamlit as st
import streamlit.components.v1 as components
import json
import plotly.express as px #pip install plotly 
import pandas as pd

st.set_page_config(page_title="Configuration & Theming", page_icon=":material/tune:")
st.title("Configuration & Theming")


st.write("Tema base: ", st.get_option("theme.base"))
st.subheader("Theme")
with st.container(border=True):
    st.markdown(
        """
        **Resumen**  
        Las claves del tema se definen en `[theme]` de `.streamlit/config.toml`:  
        `base`, `primaryColor`, `backgroundColor`, `secondaryBackgroundColor`, `textColor`, `font`.

        **Buenas prácticas**
        - Cambios de _theme_ se reflejan **al instante** (no hace falta reiniciar).
        - Mantén buen contraste (WCAG): comprueba que `textColor` contrasta con `backgroundColor`.
        - Usa `st.get_option` para acceder a la informacion de config.toml
        """
    )

    st.info(
        "Para cambiar estos valores de forma persistente, edita `.streamlit/config.toml`. "
    )

opts = {
    "theme.base": st.get_option("theme.base"),
    "theme.primaryColor": st.get_option("theme.primaryColor"),
    "theme.backgroundColor": st.get_option("theme.backgroundColor"),
    "theme.secondaryBackgroundColor": st.get_option("theme.secondaryBackgroundColor"),
    "theme.codeBackgroundColor": st.get_option("theme.codeBackgroundColor"),
    "theme.textColor": st.get_option("theme.textColor"),
    "theme.linkColor": st.get_option("theme.linkColor"),
    "theme.linkUnderline": st.get_option("theme.linkUnderline"),
    "theme.baseRadius": st.get_option("theme.baseRadius"),
    "theme.buttonRadius": st.get_option("theme.buttonRadius"),
    "theme.borderColor": st.get_option("theme.borderColor"),
    "theme.dataframeBorderColor": st.get_option("theme.dataframeBorderColor"),
    "theme.showWidgetBorder": st.get_option("theme.showWidgetBorder"),
    "theme.showSidebarBorder": st.get_option("theme.showSidebarBorder"),
    "theme.chartCategoricalColors": st.get_option("theme.chartCategoricalColors"),
    "theme.chartSequentialColors": st.get_option("theme.chartSequentialColors"),
    "theme.font": st.get_option("theme.font"),
    "theme.headingFont": st.get_option("theme.headingFont"),
    "theme.codeFont": st.get_option("theme.codeFont"),
    "theme.baseFontSize": st.get_option("theme.baseFontSize"),
    "theme.baseFontWeight": st.get_option("theme.baseFontWeight"),
}
st.caption("Opciones de tema activas (fuente: st.get_option)")
st.code(json.dumps(opts, indent=2), language="json")

st.subheader("Bordes, radios y estados de widgets")

c1, c2 = st.columns(2)
with c1:
    st.text_input("Text input (borde en focus)", key="demo_ti")
    st.number_input("Number input", value=42, key="demo_ni")
    st.selectbox("Select", ["A", "B", "C"], key="demo_sel")
with c2:
    st.button("Primary", type="primary", key="demo_btn_primary")
    st.button("Secondary", key="demo_btn_secondary")
    

st.info(
    "Modifica en `.streamlit/config.toml` → `[theme]`/`[theme.sidebar]` "
    "valores como `borderColor`, `showWidgetBorder`, `baseRadius`, `buttonRadius` y recarga."
)


st.subheader("Colores de gráficos (categorical/sequential) — Plotly")

# Categórico: usará theme.chartCategoricalColors
df_cat = pd.DataFrame({
    "category": list("ABCDEFG"),
    "value":    [7, 5, 6, 3, 8, 4, 6],
})
fig_cat = px.bar(
    df_cat,
    x="category",
    y="value",
    color="category",     # Categórico -> tema usa chartCategoricalColors
    height=260            # No indicamos template ni secuencias de color
)
st.plotly_chart(fig_cat, use_container_width=True)

# Continuo: usará theme.chartSequentialColors
import numpy as np
np.random.seed(0)
df_seq = pd.DataFrame({
    "x": np.linspace(0, 10, 120),
    "y": np.sin(np.linspace(0, 5*np.pi, 120)) + np.random.normal(0, 0.15, 120),
})
df_seq["z"] = (df_seq["y"] - df_seq["y"].min()) / (df_seq["y"].max() - df_seq["y"].min())

fig_seq = px.scatter(
    df_seq,
    x="x",
    y="y",
    color="z",            # Continuo -> tema usa chartSequentialColors
    height=260
)
st.plotly_chart(fig_seq, use_container_width=True)

st.caption(
    "Los colores de serie provienen del tema: "
    "`theme.chartCategoricalColors` (categórico) y `theme.chartSequentialColors` (continuo)."
)

# (Opcional) Mostrar los arrays que está leyendo el tema ahora mismo:
st.code({
    "theme.chartCategoricalColors": st.get_option("theme.chartCategoricalColors"),
}, language="json")

st.code({
    "theme.chartSequentialColors": st.get_option("theme.chartSequentialColors"),
}, language="json")

