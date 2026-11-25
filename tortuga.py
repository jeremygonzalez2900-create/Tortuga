import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# 1. Configuración general de la página
st.set_page_config(
    page_title="Medidor de Poder - Xeno",
    page_icon="💎",
    layout="wide"
)

# 2. Banner con Ícono SVG personalizado de Xeno
xeno_svg = """
<div style="display: flex; align-items: center; gap: 20px; background: linear-gradient(90deg, #1a0b2e 0%, #3b0d36 50%, #0d2b45 100%); padding: 20px; border-radius: 15px; border-left: 8px solid #00E5FF; box-shadow: 0 4px 15px rgba(0,0,0,0.4);">
    <svg width="90" height="100" viewBox="0 0 100 110" xmlns="http://w3.org">
        <!-- Aura energética exterior -->
        <path d="M50 5 L68 30 L90 25 L80 55 L95 85 L50 100 L5 85 L20 55 L10 25 L32 30 Z" fill="#E0115F" opacity="0.35"/>
        <path d="M50 12 L64 34 L82 30 L74 55 L86 80 L50 93 L14 80 L26 55 L18 30 L36 34 Z" fill="#00E5FF" opacity="0.45"/>
        <!-- Cabello erizado estilo guerrero -->
        <polygon points="50,10 35,35 65,35" fill="#111111"/>
        <polygon points="25,22 38,42 20,48" fill="#111111"/>
        <polygon points="75,22 62,42 80,48" fill="#111111"/>
        <polygon points="18,45 35,52 22,65" fill="#111111"/>
        <polygon points="82,45 65,52 78,65" fill="#111111"/>
        <!-- Rostro -->
        <path d="M30 40 L70 40 L65 75 L50 88 L35 75 Z" fill="#F5CBA7" stroke="#111" stroke-width="2"/>
        <!-- Gema Diamante/Rubí en la frente -->
        <polygon points="50,36 55,43 50,50 45,43" fill="#00E5FF" stroke="#FFFFFF" stroke-width="1.2"/>
        <!-- Cejas intensas y ojos brillantes -->
        <line x1="33" y1="53" x2="46" y2="57" stroke="#111" stroke-width="3"/>
        <line x1="67" y1="53" x2="54" y2="57" stroke="#111" stroke-width="3"/>
        <polygon points="35,57 45,59 42,63 35,61" fill="#E0115F"/>
        <polygon points="65,57 55,59 58,63 65,61" fill="#E0115F"/>
        <!-- Expresión seria -->
        <line x1="43" y1="74" x2="57" y2="74" stroke="#111" stroke-width="2"/>
    </svg>
    <div>
        <h1 style="margin: 0; color: #FFFFFF; font-family: sans-serif;">💎 Simulador de Poder: <span style="color: #00E5FF;">XENO</span></h1>
        <p style="margin: 6px 0 0 0; color: #E0E0E0; font-size: 16px;">
            Calcula su escala de poder combinando <b>Fase Rubí (x10)</b>, <b>Fase Diamante (x50)</b> y la técnica <b>Kaioken</b>.
        </p>
    </div>
</div>
"""
st.markdown(xeno_svg, unsafe_allow_html=True)
st.write("")

# 3. Panel de configuración de Xeno (Controles)
st.subheader("⚙️ Configuración de Estado de Xeno")
col1, col2, col3 = st.columns(3)

with col1:
    poder_base = st.number_input(
        "⚡ Poder Base de Xeno:",
        min_value=1,
        max_value=1000000000,
        value=1000,
        step=100
    )

with col2:
    fase = st.selectbox(
        "🔮 Transformación activa:",
        [
            "Estado Base (x1)",
            "Fase Rubí (x10)",
            "Fase Diamante (x5 sobre Rubí = x50)"
        ]
    )

with col3:
    usar_kaioken = st.checkbox("🔥 Activar Kaioken", value=True)
    if usar_kaioken:
        nivel_kaioken = st.slider(
            "Multiplicador Kaioken:",
            min_value=2,
            max_value=20,
            value=2,
            step=1,
            format="x%d"
        )
    else:
        nivel_kaioken = 1

# 4. Cálculos de multiplicadores
if "Rubí" in fase:
    mult_fase = 10
    color_curva = "#E0115F"  # Rojo Rubí
    icono_fase = "♦️ Rubí"
elif "Diamante" in fase:
    mult_fase = 10 * 5  # x10 del Rubí multiplicado x5 = x50
    color_curva = "#00E5FF"  # Azul Diamante
    icono_fase = "💎 Diamante"
else:
    mult_fase = 1
    color_curva = "#FFD700"  # Dorado Base
    icono_fase = "⚡ Base"

multiplicador_total = mult_fase * nivel_kaioken
poder_actual_xeno = poder_base * multiplicador_total

st.divider()

# 5. Tarjetas de Resultados Instantáneos
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric(
        label="⚡ Poder Base",
        value=f"{poder_base:,.0f}"
    )

with m2:
    st.metric(
        label="🔮 Bono de Fase",
        value=f"x{mult_fase}",
        delta=icono_fase
    )

with m3:
    st.metric(
        label="🔥 Bono Kaioken",
        value=f"x{nivel_kaioken}" if usar_kaioken else "Desactivado",
        delta=f"Multiplicador total: x{multiplicador_total}"
    )

with m4:
    st.metric(
        label="💥 PODER TOTAL DE XENO",
        value=f"{poder_actual_xeno:,.0f}",
        delta=f"+{((multiplicador_total - 1) * 100):,.0f}% de aumento"
    )

# 6. Gráfica Exponencial de Combate
st.divider()
st.subheader("📈 Curva de Despliegue Exponencial en Combate")

col_g1, col_g2 = st.columns([3, 1])
with col_g2:
    segundos = st.slider("⏱️ Segundos de carga de Ki:", min_value=5, max_value=20, value=10)
    escala_log = st.checkbox("Escala logarítmica", value=False)

# Generación de la curva exponencial desde el poder base hasta el poder máximo alcanzado
tiempo = np.linspace(0, segundos, 100)

# Fórmula exponencial que parte exactamente de poder_base en t=0 y llega a poder_actual_xeno en t=segundos
if multiplicador_total > 1:
    tasa_crecimiento = (multiplicador_total) ** (1 / segundos)
    curva_xeno = poder_base * (tasa_crecimiento ** tiempo)
else:
    curva_xeno = np.full_like(tiempo, poder_base, dtype=float)

# Curva de referencia sin Kaioken para comparar el impacto de la técnica
poder_sin_kaioken = poder_base * mult_fase
if mult_fase > 1:
    tasa_sin_kk = (mult_fase) ** (1 / segundos)
    curva_sin_kaioken = poder_base * (tasa_sin_kk ** tiempo)
else:
    curva_sin_kaioken = np.full_like(tiempo, poder_base, dtype=float)

df_grafica = pd.DataFrame({
    "Tiempo (s)": np.concatenate([tiempo, tiempo]),
    "Poder": np.concatenate([curva_xeno, curva_sin_kaioken]),
    "Estado": [f"Xeno ({icono_fase} + Kaioken x{nivel_kaioken})"] * len(tiempo) + [f"Xeno ({icono_fase} sin Kaioken)"] * len(tiempo)
})

# Puntos clave de transformación en la gráfica
puntos_hitos = pd.DataFrame({
    "Tiempo (s)": [0, segundos * 0.45, segundos * 0.75, segundos],
    "Poder": [
        poder_base,
        poder_base * (tasa_crecimiento ** (segundos * 0.45)) if multiplicador_total > 1 else poder_base,
        poder_base * (tasa_crecimiento ** (segundos * 0.75)) if multiplicador_total > 1 else poder_base,
        poder_actual_xeno
    ],
    "Etiqueta": [
        f"⚡ Base ({poder_base:,.0f})",
        "♦️ Rubí (x10)",
        "💎 Diamante (x50)",
        f"🔥 MAX: {poder_actual_xeno:,.0f}"
    ]
})

tipo_escala = "log" if escala_log else "linear"

linea = alt.Chart(df_grafica).mark_line(strokeWidth=4).encode(
    x=alt.X("Tiempo (s):Q", title="Tiempo de elevación de Ki (segundos)"),
    y=alt.Y("Poder:Q", title="Nivel de Poder", scale=alt.Scale(type=tipo_escala)),
    color=alt.Color(
        "Estado:N",
        scale=alt.Scale(range=[color_curva, "#888888"]),
        legend=alt.Legend(orient="top", title=None)
    ),
    tooltip=["Estado", "Tiempo (s)", "Poder"]
)

marcadores = alt.Chart(puntos_hitos).mark_circle(size=130, color="#FF3D00").encode(
    x="Tiempo (s):Q",
    y="Poder:Q"
)

textos = alt.Chart(puntos_hitos).mark_text(
    align="right",
    baseline="bottom",
    dx=-10,
    dy=-8,
    fontSize=14,
    fontWeight="bold",
    color="#FFFFFF"
).encode(
    x="Tiempo (s):Q",
    y="Poder:Q",
    text="Etiqueta:N"
)

with col_g1:
    st.altair_chart((linea + marcadores + textos).properties(height=430), use_container_width=True)
