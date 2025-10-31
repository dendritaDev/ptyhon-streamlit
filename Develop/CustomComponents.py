import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(page_title="Custom Components", page_icon=":material/sdk:")

st.title("Custom Components")
st.header("Custom piece of HTML")

components.html(
    """
    <canvas id="c" width="300" height="300" style="background:#111; display:block; margin:auto; border-radius:8px;"></canvas>
    <script>
      const canvas = document.getElementById('c');
      const ctx = canvas.getContext('2d');
      let angle = 0;

      function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        ctx.save();
        ctx.translate(canvas.width/2, canvas.height/2);
        ctx.rotate(angle);

        ctx.fillStyle = '#0af';
        ctx.fillRect(-60, -60, 120, 120);

        ctx.restore();

        angle += 0.02;
        requestAnimationFrame(draw);
      }

      draw();
    </script>
    """,
    height=320,
)






st.header("iframe components")
components.iframe(
    "https://www.openstreetmap.org/export/embed.html?bbox=2.14%2C41.38%2C2.19%2C41.41&layer=mapnik",
    height=400,
)
