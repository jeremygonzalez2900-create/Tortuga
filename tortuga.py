import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# 1. Configuración de la página estilo cómic / manga
st.set_page_config(
    page_title="Medidor de Poder - Saitama",
    page_icon="👊",
    layout="wide"
)

# 2. Ícono SVG personalizado estilo Saitama + Encabezado
saitama_svg = """
<div style="display: flex; align-items: center; gap: 20px; background-color: #1E1E1E; padding: 20px; border-radius: 15px; border-left: 8px solid #FFD700;">
    <svg width="85" height="95" viewBox="0 0 100 115" xmlns="http://w3.org">
        <!-- Capa blanca y cuello negro -->
        <path d="M15 110 Q50 90 85 110 L95 115 L5 115 Z" fill="#FFFFFF"/>
        <rect x="35" y="80" width="30" height="20" fill="#FFE0BD"/>
        <path d="M30 92 L70 92 L75 105 L25 105 Z" fill="#111111"/>
        <!-- Cabeza calva brillante -->
        <ellipse cx="50" cy="48" rx="30" ry="38" fill="#FFE0BD" stroke="#222" stroke-width="2.5"/>
        <!-- Brillo de la calva -->
        <ellipse cx="38" cy="24" rx="6" ry="11" transform="rotate(-25 38 24)" fill="#FFFFFF" opacity="0.85"/>
        <!-- Ojos inexpresivos clásicos ("OK") -->
        <ellipse cx="37" cy="48" rx="6" ry="3.5" fill="#FFFFFF" stroke="#111" stroke-width="2"/>
        <circle cx="37" cy="48" r="1.5" fill="#111"/>
        <ellipse cx="63" cy="48" rx="6" ry="3.5" fill="#FFFFFF" stroke="#111" stroke-width="2"/>
        <circle cx="63" cy="48" r="1.5" fill="#111"/>
        <!-- Cejas planas -->
        <line x1="29" y1="41" x2="44" y2="41" stroke="#111" stroke-width="2"/>
        <line x1="56" y1="41" x2="71" y2="41" stroke="#111" stroke-width="2"/>
        <!-- Nariz y boca sencilla -->
        <path d="M50 48 L48 58 L52 58" fill="none" stroke="#111" stroke-width="1.8"/>
        <line x1="43" y1="68" x2="57" y2="68" stroke="#111" stroke-width="2"/>
    </svg>
    <div>
        <h1 style="margin: 0; color: #FFD700; font-family: sans-serif;">👊 Gráfica de Crecimiento Exponencial: SAITAMA</h1>
        <p style="margin: 5px 0 0 0; color: #CCCCCC; font-size: 16px;">
            Simulador interactivo basado en el capítulo 168 del manga (Batalla en Ío, luna de Júpiter).
        </p>
    </div>
</div>
"""
st.markdown(saitama_svg, unsafe_allow_html=True)
st.write("")

# 3. Controles interactivos en columnas
col_ctrl1, col_ctrl2, col_ctrl3 = st.columns(3)

with col_ctrl1:
    segundos = st.slider(
        "⏱️ Duración del combate (segundos):",
        min_value=5,
        max_value=30,
        value=15,
        step=1
    )

with col_ctrl2:
    factor_emocion = st.slider(
        "🔥 Nivel de emoción / intensidad:",
        min_value=1.2,
        max_value=2.0,
        value=1.55,
        step=0.05
    )

with col_ctrl3:
    escala_log = st.checkbox("Usar escala logarítmica", value=False)

# 4. Cálculo matemático del crecimiento exponencial
tiempo = np.linspace(0, segundos, 100)
poder_base = 100

# Curva de Saitama (crecimiento exponencial acelerado)
poder_saitama = poder_base * (factor_emocion ** tiempo)

# Curva de Garou Cósmico (intenta copiarlo pero siempre va un paso atrás)
poder_garou = poder_base * ((factor_emocion - 0.12) ** tiempo)

df = pd.DataFrame({
    "Tiempo (s)": np.concatenate([tiempo, tiempo]),
    "Nivel de Poder": np.concatenate([poder_saitama, poder_garou]),
    "Personaje": ["👊 Saitama (Crecimiento Exponencial)"] * len(tiempo) + ["🌌 Garou Cósmico (Copia)"] * len(tiempo)
})

# Puntos clave para mostrar íconos en la gráfica
puntos_clave = pd.DataFrame({
    "Tiempo (s)": [0, segundos * 0.5, segundos],
    "Nivel de Poder": [
        poder_base,
        poder_base * (factor_emocion ** (segundos * 0.5)),
        poder_saitama[-1]
    ],
    "Icono": ["😐 Inicio", "⚡ Limitador Roto", "👊💥 ¡SERIOUS PUNCH!"]
})

# 5. Creación de la gráfica estilo manga con Altair
tipo_escala = "log" if escala_log else "linear"

linea_poder = alt.Chart(df).mark_line(strokeWidth=4).encode(
    x=alt.X("Tiempo (s):Q", title="Tiempo transcurrido en combate (segundos)"),
    y=alt.Y("Nivel de Poder:Q", title="Nivel de Poder Medido", scale=alt.Scale(type=tipo_escala)),
    color=alt.Color(
        "Personaje:N",
        scale=alt.Scale(
            domain=["👊 Saitama (Crecimiento Exponencial)", "🌌 Garou Cósmico (Copia)"],
            range=["#FFD700", "#00E5FF"]
        ),
        legend=alt.Legend(orient="top", title=None)
    ),
    tooltip=["Personaje", "Tiempo (s)", "Nivel de Poder"]
)

# Capa de puntos con íconos y etiquetas sobre la curva de Saitama
etiquetas_iconos = alt.Chart(puntos_clave).mark_text(
    align="right",
    baseline="bottom",
    dx=-8,
    dy=-8,
    fontSize=15,
    fontWeight="bold",
    color="#FFFFFF"
).encode(
    x="Tiempo (s):Q",
    y="Nivel de Poder:Q",
    text="Icono:N"
)

puntos_marcadores = alt.Chart(puntos_clave).mark_circle(size=120, color="#FF3D00").encode(
    x="Tiempo (s):Q",
    y="Nivel de Poder:Q"
)

grafica_final = (linea_poder + puntos_marcadores + etiquetas_iconos).properties(
    height=480,
    title="Comparativa de Evolución de Poder en Tiempo Real"
).configure_view(
    strokeWidth=0
)

# 6. Mostrar gráfica y métricas finales
st.altair_chart(grafica_final, use_container_width=True)

st.divider()

# Tarjetas de resumen inferior
m1, m2, m3 = st.columns(3)
poder_final_saitama = poder_saitama[-1]
poder_final_garou = poder_garou[-1]
diferencia_veces = poder_final_saitama / poder_final_garou

with m1:
    st.metric(
        label="👊 Poder Final de Saitama",
        value=f"{poder_final_saitama:,.0f} pts",
        delta=f"x{poder_final_saitama / poder_base:,.1f} respecto al inicio"
    )

with m2:
    st.metric(
        label="🌌 Poder Final de Garou",
        value=f"{poder_final_garou:,.0f} pts",
        delta="Incapaz de alcanzarlo",
        delta_color="off"
    )

with m3:
    st.metric(
        label="🚀 Ventaja de Saitama",
        value=f"{diferencia_veces:,.1f} veces más fuerte",
        delta="Crecimiento infinito"
    )
