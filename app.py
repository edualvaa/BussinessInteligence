import streamlit as st
import streamlit_antd_components as sac
from views import insights, reporting, segmentation, recommendations

# Configurar la página
st.set_page_config(page_title="Business Intelligence", layout="wide")

menu = sac.tabs(
    items=[
        # {"icon": "bar-chart", "label": "Insights", "key": "Insights"},

        {"icon": "lightbulb", "label": "Recomendaciones", "key": "recommendations"},
        {"icon": "file-text", "label": "Reporting", "key": "Reporting"},

        {"icon": "database", "label": "Segmentación", "key": "Segmentation"}
    ],
    index=1,
    format_func=lambda x: x.title(),
    align="center",
    use_container_width=True
)

if menu == "Insights":
    insights.insights_view()

elif menu == "Recomendaciones":
    recommendations.recommendations_view()

elif menu == "Reporting":
    reporting.reporting_view()

elif menu == "Segmentación":
    segmentation.segmentation_view()

else:
    pass
