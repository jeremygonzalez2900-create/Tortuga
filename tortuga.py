import streamlit as st
import pandas as pd

# 1. Configuración general de la página
st.set_page_config(
    page_title="Calculadora de Porcentajes Pro",
    page_icon="📊",
    layout="wide"
)

# 2. Barra lateral (Sidebar) para controles globales
with st.sidebar:
    st.header("⚙️ Configuración")
    moneda = st.selectbox("Selecciona tu moneda:", ["$", "€", "MXN $", "USD $"])
    decimales = st.slider("Cantidad de decimales:", min_value=0, max_value=4, value=2)
    st.divider()
    st.info("Ajusta los valores en cada pestaña para ver los cálculos y gráficas en tiempo real.")

# 3. Encabezado principal
st.title("📊 Calculadora Avanzada de Porcentajes")
st.markdown("Herramienta interactiva para calcular **aumentos, descuentos, IVA y proyecciones**.")
st.divider()

# 4. Organización en pestañas (Tabs)
tab1, tab2, tab3 = st.tabs([
    "🧮 Calculadora Rápida", 
    "📈 Proyección de Crecimiento", 
    "📋 Tabla Comparativa"
])

# ==========================================
# PESTAÑA 1: CALCULADORA DE AUMENTO Y DESCUENTO
# ==========================================
with tab1:
    st.subheader("Cálculo directo")
    
    # Dividimos la pantalla en dos columnas para los controles
    col_input1, col_input2 = st.columns(2)
    
    with col_input1:
        monto = st.number_input(
            "Ingresa el valor base:", 
            min_value=1.0, 
            max_value=1000000.0, 
            value=1000.0, 
            step=50.0
        )
        
    with col_input2:
        porcentaje = st.slider(
            "Selecciona el porcentaje (%):", 
            min_value=1, 
            max_value=100, 
            value=10, 
            step=1
        )
        
    tipo_operacion = st.radio(
        "¿Qué deseas calcular?",
        ["Sumar porcentaje (Aumento / IVA)", "Restar porcentaje (Descuento)"],
        horizontal=True
    )

    # Cálculos matemáticos
    diferencia = monto * (porcentaje / 100)
    
    if "Sumar" in tipo_operacion:
        resultado_final = monto + diferencia
        texto_delta = f"+{porcentaje}% ({moneda}{diferencia:,.{decimales}f})"
        color_delta = "normal"
    else:
        resultado_final = monto - diferencia
        texto_delta = f"-{porcentaje}% (-{moneda}{diferencia:,.{decimales}f})"
        color_delta = "inverse"

    st.divider()

    # Mostrar resultados en tarjetas grandes (st.metric)
    col_res1, col_res2, col_res3 = st.columns(3)
    
    with col_res1:
        st.metric(
            label="Monto Original", 
            value=f"{moneda}{monto:,.{decimales}f}"
        )
    with col_res2:
        st.metric(
            label=f"Equivalente al {porcentaje}%", 
            value=f"{moneda}{diferencia:,.{decimales}f}"
        )
    with col_res3:
        st.metric(
            label="Resultado Final", 
            value=f"{moneda}{resultado_final:,.{decimales}f}", 
            delta=texto_delta,
            delta_color=color_delta
        )

    # Resultado destacado en texto grande como pediste antes
    st.success(f"### El resultado final con el {porcentaje}% aplicado es: **{moneda}{resultado_final:,.{decimales}f}**")

# ==========================================
# PESTAÑA 2: PROYECCIÓN DE INTERÉS / CRECIMIENTO
# ==========================================
with tab2:
    st.subheader("Simulador de crecimiento acumulativo")
    st.write("Visualiza cómo crece tu monto si aplicas ese porcentaje repetidamente durante varios periodos.")
    
    periodos = st.slider("Número de periodos (meses o años):", min_value=2, max_value=36, value=12)
    
    # Generar datos para la gráfica
    datos_proyeccion = []
    valor_actual = monto
    
    for p in range(0, periodos + 1):
        datos_proyeccion.append({
            "Periodo": p,
            "Valor Acumulado": round(valor_actual, decimales),
            "Monto Base": round(monto, decimales)
        })
        valor_actual = valor_actual + (valor_actual * (porcentaje / 100))
        
    df_proyeccion = pd.DataFrame(datos_proyeccion).set_index("Periodo")
    
    # Gráfica nativa de líneas
    st.line_chart(df_proyeccion)
    
    valor_final_proy = datos_proyeccion[-1]["Valor Acumulado"]
    st.markdown(f"#### Al final de **{periodos} periodos**, tu monto inicial crecerá a **{moneda}{valor_final_proy:,.{decimales}f}**.")

# ==========================================
# PESTAÑA 3: TABLA DE PORCENTAJES COMUNES
# ==========================================
with tab3:
    st.subheader(f"Tabla de referencia rápida para {moneda}{monto:,.{decimales}f}")
    
    porcentajes_comunes = [5, 10, 15, 16, 20, 25, 30, 50, 75]
    filas_tabla = []
    
    for pct in porcentajes_comunes:
        calc = monto * (pct / 100)
        filas_tabla.append({
            "Porcentaje": f"{pct}%",
            "Monto del Porcentaje": f"{moneda}{calc:,.{decimales}f}",
            "Total con Aumento (+)": f"{moneda}{monto + calc:,.{decimales}f}",
            "Total con Descuento (-)": f"{moneda}{monto - calc:,.{decimales}f}"
        })
        
    df_tabla = pd.DataFrame(filas_tabla)
    
    # Mostrar tabla interactiva ocupando todo el ancho
    st.dataframe(df_tabla, use_container_width=True, hide_index=True)
    
    # Botón para descargar los datos en CSV
    csv = df_tabla.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar tabla en Excel / CSV",
        data=csv,
        file_name="tabla_porcentajes.csv",
        mime="text/csv"
    )
