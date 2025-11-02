import streamlit as st
import time
import pandas as pd
import plotly.express as px
import datetime
import pydeck as pdk

st.set_page_config(layout="wide")

DATA_PATH = r"C:\git\Grupo9_MovilidadUrbanaCaso\data\processed\tripdata_cleaned.csv"
@st.cache_data
def load_data(path):
    data = pd.read_csv(path)
    data['pickup_date'] = pd.to_datetime(data['pickup_date'], errors='coerce')
    return data 

df_clean = load_data(DATA_PATH)

st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #004e92, #000428);
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        color: white;
        box-shadow: 0px 0px 15px rgba(0,0,0,0.4);
        margin-bottom: 20px;
    }
    .main-header h1 {
        font-size: 42px;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .main-header h3 {
        font-weight: normal;
        color: #FFD700;
        margin-top: 0;
    }
    </style>

    <div class="main-header">
        <h1>🚖 Dashboard de Análisis Geoespacial - NYC Yellow Taxi</h1>
        <h3>Proyecto de Caso de Estudio – Grupo 9</h3>
        <p style='font-size:18px; max-width:900px; margin:auto;'>
        <b>Objetivo:</b> Construir un sistema de análisis geoespacial que permita a los 
        planificadores urbanos visualizar y comprender los patrones de movilidad de taxis en la ciudad de Nueva York,
        mediante mapas de calor, flujos de viaje y métricas clave sobre distancia, duración y pasajeros.
        </p>
    </div>
""", unsafe_allow_html=True)


st.sidebar.markdown("## Filtros de Análisis")
st.sidebar.markdown("Ajusta los parámetros para actualizar los resultados y visualizaciones:")
st.sidebar.divider()

# Fecha
fecha_min, fecha_max = df_clean['pickup_date'].min(), df_clean['pickup_date'].max()
rango_fechas = st.sidebar.date_input(
    "Rango de fechas:",
    value=(fecha_min, fecha_max),
    min_value=fecha_min,
    max_value=fecha_max
)

st.sidebar.markdown("### 📅 Fecha y Hora")

hora_min, hora_max = st.sidebar.slider("Rango de horas:", 0, 23, (6, 20))

st.sidebar.markdown("### 👥 Pasajeros")
p_min, p_max = st.sidebar.slider("Número de pasajeros:", 1, int(df_clean['passengers'].max()), (1, 4))

inicio, fin = rango_fechas
df_filtrado = df_clean[
    (df_clean['pickup_date'].between(pd.to_datetime(inicio), pd.to_datetime(fin))) &
    (df_clean['pickup_hour'].between(hora_min, hora_max)) &
    (df_clean['passengers'].between(p_min, p_max))
]

if len(df_filtrado) > 0:
    total_viajes = len(df_filtrado)
    promedio_distancia = df_filtrado['distance'].mean()
    duracion_promedio = df_filtrado['trip_duration'].mean()
    pasajeros_promedio = df_filtrado['passengers'].mean()

    kpi1, kpi2, kpi3, kpi4= st.columns(4)
    kpi1.metric("Total de Viajes", f"{total_viajes:,}")
    kpi2.metric("Distancia Promedio (mi)", f"{promedio_distancia:.2f}")
    kpi3.metric("Duración Promedio (min)", f"{duracion_promedio:.1f}")
    kpi4.metric("Pasajeros Promedio", f"{pasajeros_promedio:.1f}")
else:
    st.warning("No hay datos para calcular KPIs en el rango seleccionado.")
    

tab1, tab2, tab3 = st.tabs(["🔥 Mapa de Calor origen","🔥 Mapa de Calor destino", "🧭 Mapa de Flujos"])
 
# --- TAB 1: Mapa de Calor ---
with tab1:   
# ------------------------------------------------------
# VISUALIZACIÓN 1: MAPA DE CALOR (PICKUPS)
# ------------------------------------------------------
    st.subheader("🔥 Mapa de Calor de Puntos de origen")
    # Validar columnas necesarias
    if 'pickup_latitude' in df_filtrado.columns and 'pickup_longitude' in df_filtrado.columns:
        MAX_PUNTOS = 20000
        if len(df_filtrado) > MAX_PUNTOS:
            df_mapa = df_filtrado.sample(MAX_PUNTOS, random_state=42)
        else:
            df_mapa = df_filtrado.copy()

        df_mapa = df_mapa.rename(columns={'pickup_latitude': 'lat', 'pickup_longitude': 'lon'})

        view_state = pdk.ViewState(latitude=40.7128, longitude=-74.0060, zoom=11, pitch=40)

        heatmap_layer = pdk.Layer(
            "HeatmapLayer",
            data=df_mapa,
            get_position='[lon, lat]',
            radius_pixels=40,
            intensity=1,
            opacity=0.9,
        )

        r = pdk.Deck(
            layers=[heatmap_layer],
            initial_view_state=view_state,
            map_style="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json"
        )

        st.pydeck_chart(r)
    else:
        st.error("❌ No se encontraron columnas de coordenadas válidas.")
with tab2:
      st.subheader("🔥 Mapa de Calor de Puntos de destino")
with tab3:
      st.subheader("🧭 Mapa de Flujos")
      
with tab2:
    st.subheader("🔥 Mapa de Calor de Puntos de Destino")
    
    # Validar columnas necesarias
    if 'dropoff_latitude' in df_filtrado.columns and 'dropoff_longitude' in df_filtrado.columns:
        MAX_PUNTOS = 20000
        if len(df_filtrado) > MAX_PUNTOS:
            df_mapa_destino = df_filtrado.sample(MAX_PUNTOS, random_state=42)
        else:
            df_mapa_destino = df_filtrado.copy()

        df_mapa_destino = df_mapa_destino.rename(columns={'dropoff_latitude': 'lat', 'dropoff_longitude': 'lon'})

        view_state = pdk.ViewState(latitude=40.7128, longitude=-74.0060, zoom=11, pitch=40)

        heatmap_layer = pdk.Layer(
            "HeatmapLayer",
            data=df_mapa_destino,
            get_position='[lon, lat]',
            radius_pixels=40,
            intensity=1,
            opacity=0.9,
        )

        r = pdk.Deck(
            layers=[heatmap_layer],
            initial_view_state=view_state,
            map_style="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json"
        )

        st.pydeck_chart(r)
    else:
        st.error("❌ No se encontraron columnas de coordenadas válidas para destinos.")
  