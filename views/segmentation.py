import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.cluster import KMeans


def segmentation_view():
    st.subheader("Metodología de Segmentación de Clientes")

    st.write("""
    Para realizar esta segmentación, se ha utilizado un enfoque basado en **clustering** mediante el algoritmo de machine learnin **K-Means**. 
    Este método permite agrupar a los clientes en distintos segmentos según similitudes en sus características.
    
    Los datos considerados en este análisis incluyen:
    
    ✅ **Edad** del cliente  
    ✅ **Ingresos anuales**  
    ✅ **Gasto promedio por compra**  
    ✅ **Frecuencia de compra mensual**  
      
    """)

    # Generar datos de maqueta
    np.random.seed(42)
    n_clients = 200
    data = pd.DataFrame({
        "Cliente_ID": range(1, n_clients + 1),
        "Edad": np.random.randint(18, 70, n_clients),
        "Ingresos": np.random.randint(15000, 120000, n_clients),
        "Gasto_Promedio": np.random.randint(500, 5000, n_clients),
        "Frecuencia_Compra": np.random.randint(1, 30, n_clients)
    })

    # Aplicar clustering (KMeans con 4 clusters)
    X = data[["Edad", "Ingresos", "Gasto_Promedio", "Frecuencia_Compra"]]
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    data["Segmento"] = kmeans.fit_predict(X)

    # Gráfico 3D de Segmentación de Clientes
    fig1 = px.scatter_3d(data, x="Edad", y="Ingresos", z="Gasto_Promedio",
                         color=data["Segmento"].astype(str),
                         size="Frecuencia_Compra",
                         title="Segmentación de Clientes (Clustering)",
                         labels={"Segmento": "Grupo de Clientes"},
                         opacity=0.8)

    # Gráfico de dispersión 2D Edad vs Ingresos
    fig2 = px.scatter(data, x="Edad", y="Ingresos", color=data["Segmento"].astype(str),
                      title="Edad vs Ingresos por Segmento", labels={"Segmento": "Grupo de Clientes"},
                      size="Gasto_Promedio", opacity=0.8)

    # Mostrar gráficos en Streamlit
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        st.plotly_chart(fig2, use_container_width=True)

    st.write("""
        A partir de estas variables, se aplicó **normalización y clustering**, identificando **cuatro grupos principales de clientes** con patrones de comportamiento similares.  
    
    ### 🔍 Principales conclusiones:
    🔹 **Clientes con alto poder adquisitivo y baja frecuencia de compra.**  
    🔹 **Clientes con alta recurrencia pero gasto moderado.**  
    🔹 **Identificación de oportunidades para fidelización y personalización de ofertas.**  
    
    Gracias a este enfoque, las empresas pueden **personalizar sus estrategias de marketing**, mejorar la **retención de clientes** y optimizar su **rentabilidad**. 🚀
    """)

    # Mostrar tabla de datos
    st.subheader("📋 Datos de Clientes Segmentados")
    st.dataframe(data)
