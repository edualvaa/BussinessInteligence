import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity


# Función para generar recomendaciones y similitud
def recomendar_items(user_id, ratings_df, top_n=5):
    """Genera recomendaciones de ítems para un usuario utilizando filtrado colaborativo basado en ítems."""
    item_similarity = cosine_similarity(ratings_df.T.fillna(0))
    item_similarity_df = pd.DataFrame(item_similarity, index=ratings_df.columns, columns=ratings_df.columns)

    user_ratings = ratings_df.loc[user_id].dropna()
    scores = {}
    for item, rating in user_ratings.items():
        similar_items = item_similarity_df[item].drop(item) * rating
        for i, score in similar_items.items():
            scores[i] = scores.get(i, 0) + score

    # Ordenar y seleccionar los mejores ítems
    recommended_items = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_n]

    # 🔥 Aplicar un boost al primer ítem recomendado para que destaque más
    if recommended_items:
        recommended_items[0] = (
        recommended_items[0][0], recommended_items[0][1] * 1.4)  # Aumentar el primer score un 40%

    return [item for item, score in recommended_items], item_similarity_df, {item: score for item, score in
                                                                             recommended_items}


# ====== 🔹 Datos de Ejemplo Mejorados 🔹 ======

np.random.seed(42)


def recommendations_view():
    data = {
        "Usuario 1": np.random.randint(1, 10, 5) + np.random.uniform(0, 2, 5),
        "Usuario 2": np.random.randint(1, 10, 5) + np.random.uniform(0, 2, 5),
        "Usuario 3": np.random.randint(1, 10, 5) + np.random.uniform(0, 2, 5),
        "Usuario 4": np.random.randint(1, 10, 5) + np.random.uniform(0, 2, 5),
        "Usuario 5": np.random.randint(1, 10, 5) + np.random.uniform(0, 2, 5),
    }
    ratings_df = pd.DataFrame(data, index=["Pelicula A", "Pelicula B", "Pelicula C", "Pelicula D", "Pelicula E"]).T

    # 🚀 UI de Streamlit
    st.header("Recomendador Interactivo de Películas 🎬")

    st.write("""
    Este sistema usa **Filtrado Colaborativo basado en Ítems. Analizamos cómo los usuarios han calificado diferentes 
    películas y detectamos patrones de similitud para hacer predicciones personalizadas.  
    
    """)

    # Seleccionar usuario
    col1, col2, col3 = st.columns([2, 1, 2])
    user_id = col1.selectbox("🎭 Selecciona un usuario:", ratings_df.index)

    # Número de recomendaciones
    top_n = col3.slider("📌 Número de recomendaciones:", min_value=1, max_value=5, value=3)

    # Generar recomendaciones
    recomendaciones, item_similarity_df, scores = recomendar_items(user_id, ratings_df, top_n)

    # 🔥 Gráfico 1: Heatmap de Similitud entre Ítems
    st.write("## 📊 Similitud entre Películas")
    fig1 = px.imshow(item_similarity_df,
                     labels=dict(color="Similitud"),
                     x=item_similarity_df.columns,
                     y=item_similarity_df.columns,
                     color_continuous_scale="RdBu_r",
                     text_auto=".2f")
    fig1.update_layout(autosize=True, height=600, margin=dict(l=10, r=10, t=50, b=10))
    st.plotly_chart(fig1, use_container_width=True)

    # 🔥 Gráfico 2: Barras de Recomendaciones
    st.write(f"## ✨ Películas Recomendadas para {user_id}")

    if recomendaciones:
        df_recommendations = pd.DataFrame(list(scores.items()), columns=["Película", "Score"])

        # 🔥 Aplicar colores para destacar la película principal
        colors = ["#E63946" if i == 0 else "#1D3557" for i in range(len(df_recommendations))]

        fig2 = px.bar(df_recommendations, x="Película", y="Score",
                      text="Score",
                      labels={"Score": "Puntuación de Recomendación"},
                      title="🎥 Ranking de Películas Recomendadas",
                      color=df_recommendations["Película"],
                      color_discrete_sequence=colors)

        fig2.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig2.update_layout(yaxis=dict(title="Puntuación"), xaxis=dict(title="Película"))
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.write("⚠️ No hay suficientes datos para generar recomendaciones.")

    # 🔎 Mostrar los datos originales si el usuario quiere
    if st.checkbox("👀 Mostrar Datos Originales"):
        st.write("### 📋 Datos Originales de Calificación")
        st.dataframe(ratings_df)
