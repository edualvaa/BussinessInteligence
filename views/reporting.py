import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta


def reporting_view():
    st.title("⛏️ Reporte Interactivo de Producción Minera")

    # Generar datos de maqueta para producción minera
    np.random.seed(42)
    fechas = pd.date_range(start="2023-01-01", periods=12, freq='M')
    minerales = ["Oro", "Plata", "Cobre", "Hierro"]

    produccion = pd.DataFrame({
        "Fecha": np.tile(fechas, len(minerales)),
        "Mineral": np.repeat(minerales, len(fechas)),
        "Toneladas_Producidas": np.random.randint(500, 5000, len(fechas) * len(minerales)),
        "Costo_Produccion": np.random.randint(100000, 1000000, len(fechas) * len(minerales)),
        "Profit": np.random.randint(50000, 900000, len(fechas) * len(minerales))
    })


    mineral_seleccionado =minerales
    fecha_inicio = fechas.min()
    fecha_fin = fechas.max()

    # Filtrar datos
    filtered_data = produccion[
        (produccion["Fecha"] >= pd.Timestamp(fecha_inicio)) & (produccion["Fecha"] <= pd.Timestamp(fecha_fin))]
    filtered_data = filtered_data[filtered_data["Mineral"].isin(mineral_seleccionado)]

    # KPI Principales
    col1, col2, col3 = st.columns(3)
    total_toneladas = filtered_data["Toneladas_Producidas"].sum()
    total_costo = filtered_data["Costo_Produccion"].sum()
    total_profit = filtered_data["Profit"].sum()

    col1.metric("🔹 Total de Producción", f'{total_toneladas:,} Tn')
    col2.metric("💰 Costo Total", f'$ {total_costo:,}')
    col3.metric("📈 Profit Total", f'$ {total_profit:,}')

    # Gráfico de líneas - Producción en el tiempo
    fig1 = px.line(filtered_data, x="Fecha", y="Toneladas_Producidas", color="Mineral",
                   title="Producción Mensual por Mineral", labels={"Toneladas_Producidas": "Toneladas"})

    # Gráfico de barras - Costos vs. Profit
    fig2 = px.bar(filtered_data, x="Mineral", y=["Costo_Produccion", "Profit"],
                  title="Costos vs. Profit por Mineral", barmode="group", labels={"value": "Monto ($)"})

    # Gráfico de dona - Distribución de Producción
    produccion_por_mineral = filtered_data.groupby("Mineral")["Toneladas_Producidas"].sum().reset_index()
    fig3 = px.pie(produccion_por_mineral, names="Mineral", values="Toneladas_Producidas", hole=0.4,
                  title="Distribución de Producción por Mineral")

    # Gráfico de velocímetro - Profit objetivo
    profit_total = total_profit
    profit_objetivo = 5000000  # Valor arbitrario de meta
    fig4 = go.Figure(go.Indicator(
        mode="gauge+number",
        value=profit_total,
        title={"text": "Profit Total vs. Objetivo"},
        gauge={"axis": {"range": [None, profit_objetivo]}, "bar": {"color": "green"}}
    ))

    # Mostrar gráficos con textos
    st.subheader("📊 Análisis de Producción Minera")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write(
            "Este gráfico muestra la evolución de la producción mensual por mineral, permitiendo observar tendencias y variaciones en la extracción de cada recurso.")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.plotly_chart(fig2, use_container_width=True)
    with col2:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write(
            "Comparación entre costos de producción y profit generado por cada mineral. Un equilibrio adecuado es clave para la rentabilidad de la operación minera.")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.plotly_chart(fig3, use_container_width=True)
    with col2:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write(
            "La distribución de la producción muestra qué porcentaje de las toneladas extraídas corresponde a cada mineral. Esto es útil para evaluar la dependencia de ciertos recursos.")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.plotly_chart(fig4, use_container_width=True)
    with col2:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write(
            "El velocímetro indica el profit total de la minera en comparación con un objetivo definido. Permite evaluar rápidamente el desempeño financiero.")

    # Mostrar tabla de datos
    st.subheader("📋 Datos de Producción Minera")
    st.dataframe(filtered_data)

    # Descarga de Reporte
    st.subheader("📥 Descargar Reporte")

    @st.cache_data
    def convertir_df(df):
        return df.to_csv(index=False).encode('utf-8')

    csv = convertir_df(filtered_data)
    st.download_button(
        label="📥 Descargar CSV",
        data=csv,
        file_name="reporte_produccion_minera.csv",
        mime="text/csv",
    )
