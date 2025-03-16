import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

def generar_datos(n=100):
    np.random.seed(42)

    # Variables con relaciones más realistas
    precio = np.random.uniform(5, 50, n)
    stock = np.random.randint(10, 500, n)
    demanda_esperada = np.random.randint(5, 300, n) + np.random.normal(0, 20, n)
    publicidad = np.random.uniform(100, 5000, n)
    clientes_en_tienda = np.random.randint(50, 2000, n)
    compradores = clientes_en_tienda * np.random.uniform(0.05, 0.5, n)
    descuentos = np.random.uniform(0, 30, n)  # Descuento en porcentaje
    dia_de_la_semana = np.random.choice(range(1, 8), n)  # 1: Lunes, 7: Domingo

    # Construcción del DataFrame
    df = pd.DataFrame({
        "Precio": precio,
        "Stock": stock,
        "Demanda Esperada": demanda_esperada,
        "Gasto en Publicidad": publicidad,
        "Clientes en Tienda": clientes_en_tienda,
        "Compradores": compradores,
        # "Descuentos Aplicados": descuentos,
        "Día de la Semana": dia_de_la_semana
    })

    return df


def insights_view():
    st.title("🔍 Heatmap Interactivo de Correlación de Ventas 📊")

    # Control deslizante para ajustar la cantidad de datos
    n_datos = st.slider("🔢 Selecciona el número de registros:", min_value=50, max_value=500, value=200, step=50)

    # Generar los datos
    df = generar_datos(n_datos)

    # Calcular la matriz de correlación con 2 decimales
    corr_matrix = df.corr().round(2)


    # Crear el heatmap interactivo con Plotly
    fig = px.imshow(corr_matrix,
                    labels=dict(color="Correlación"),
                    x=corr_matrix.columns,
                    y=corr_matrix.columns,
                    color_continuous_scale="RdBu_r",
                    zmin=-1, zmax=1,
                    text_auto=".2f")  # Mostrar solo 2 decimales

    # Ajustar tamaño de los textos para mejor visibilidad
    fig.update_traces(
        textfont=dict(size=14),  # Tamaño más grande
        hovertemplate="Correlación: %{z:.2f}"  # Mostrar valores con 2 decimales en hover
    )
    # Ajustar tamaño de la figura para que se expanda en pantalla
    fig.update_layout(
        autosize=True,
        height=600,  # Altura del gráfico
        margin=dict(l=10, r=10, t=50, b=10),  # Reducir márgenes
    )

    # Mostrar la gráfica en Streamlit
    st.plotly_chart(fig, use_container_width=True)

    # Mostrar la tabla de datos generados
    if st.checkbox("👀 Mostrar datos generados"):
        st.dataframe(df)
