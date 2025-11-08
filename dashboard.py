import streamlit as st
import time
import pandas as pd
import plotly.express as px
import datetime
import pydeck as pdk
import requests



st.set_page_config(page_title="Dashboard de Movilidad", layout="wide")

# las URLs 
API_BASE_URL = "http://54.159.51.246:8000"
API_URL_FILTROS = f"{API_BASE_URL}/filters/options"
API_URL_KPI = f"{API_BASE_URL}/options/kpi"
API_URL_MAPA_CALOR = f"{API_BASE_URL}/heatmap/pickup"
API_URL_MAPA_CALOR_DROP = f"{API_BASE_URL}/heatmap/dropoff"
API_URL_MAPA_FLOW= f"{API_BASE_URL}/flow"

@st.cache_data
def cargar_opciones_filtros():
    """llama a la API para obtener las opciones de los filtros"""
    try:
        response = requests.get(API_URL_FILTROS)
        response.raise_for_status()
        print("Filtros cargados desde la API")
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error al cargar filtros desde la API: {e}")
        return None
    

st.markdown("""
    <style>
    /* Fondo espacial muy tenue para toda la aplicación */
    .stApp {
        background: linear-gradient(135deg, #1a1d29 0%, #2d3250 50%, #1f2937 100%);
        background-size: 400% 400%;
        animation: gradientShift 20s ease infinite;
    }
    
    /* Animación muy sutil del fondo */
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Estrellas muy tenues */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(1px 1px at 20% 30%, rgba(255, 255, 255, 0.3), transparent),
            radial-gradient(1px 1px at 60% 70%, rgba(255, 255, 255, 0.2), transparent),
            radial-gradient(1px 1px at 50% 50%, rgba(255, 255, 255, 0.3), transparent),
            radial-gradient(1px 1px at 80% 10%, rgba(255, 255, 255, 0.2), transparent),
            radial-gradient(1px 1px at 90% 60%, rgba(255, 255, 255, 0.3), transparent),
            radial-gradient(1px 1px at 33% 90%, rgba(255, 255, 255, 0.2), transparent),
            radial-gradient(1px 1px at 10% 80%, rgba(255, 255, 255, 0.2), transparent);
        background-size: 200% 200%;
        opacity: 0.15;
        pointer-events: none;
        z-index: 0;
    }

    /* Fondo del sidebar más claro */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2c3142 0%, #353b52 100%);
        border-right: 2px solid #4a5568;
        padding: 1.5rem 1rem;
        box-shadow: 2px 0 10px rgba(0, 0, 0, 0.3);
    }

    /* Títulos del sidebar con mejor contraste */
    .sidebar-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 0.5rem;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.5);
    }

    /* Subtítulos más claros */
    .sidebar-subtitle {
        font-size: 1.5rem;
        font-weight: 600;
        color: #e0f2fe;
        margin-top: 1rem;
        margin-bottom: 0.2rem;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
    }

    /* Textos descriptivos con buen contraste */
    .sidebar-text {
        font-size: 0.9rem;
        color: #cbd5e1;
        margin-bottom: 0.8rem;
    }

    /* Mejorar visibilidad de labels en el sidebar */
    section[data-testid="stSidebar"] label {
        color: #e2e8f0 !important;
        font-weight: 500;
    }

    /* Slider y selectbox */
    div[data-baseweb="slider"], div[data-baseweb="select"] {
        margin-top: 0.3rem;
        margin-bottom: 1rem;
    }

    /* Divisores más visibles */
    hr {
        border: 1px solid #475569;
        box-shadow: 0 0 3px rgba(71, 85, 105, 0.5);
        margin-top: 1rem;
        margin-bottom: 1rem;
    }

    /* Botón con mejor contraste */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }

    div.stButton > button:first-child:hover {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        transform: scale(1.03);
        box-shadow: 0 6px 16px rgba(99, 102, 241, 0.4);
    }

    /* Mejorar espaciado general del sidebar */
    section[data-testid="stSidebar"] .block-container {
        padding-top: 1rem !important;
    }

    /* Header principal con mejor contraste */
    .main-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #6366f1 100%);
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        color: white;
        box-shadow: 0px 10px 25px rgba(59, 130, 246, 0.3);
        margin-bottom: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .main-header h1 {
        font-size: 42px;
        font-weight: bold;
        margin-bottom: 5px;
        text-shadow: 2px 2px 6px rgba(0, 0, 0, 0.4);
        color: #ffffff;
    }
    
    .main-header h3 {
        font-weight: normal;
        color: #fde047;
        margin-top: 0;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.4);
    }

    .main-header p {
        color: #f0f9ff !important;
    }

    /* Mejorar las métricas KPI con fondo más visible */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(51, 65, 85, 0.8), rgba(71, 85, 105, 0.8));
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid rgba(148, 163, 184, 0.3);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }

    /* Mejorar color de texto de métricas */
    div[data-testid="stMetric"] label {
        color: #e2e8f0 !important;
    }

    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #ffffff !important;
    }

    /* Tabs con mejor contraste */
    button[data-baseweb="tab"] {
        background-color: rgba(51, 65, 85, 0.6) !important;
        color: #e0f2fe !important;
        border-radius: 8px 8px 0 0;
        font-weight: 500;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(180deg, #3b82f6, #6366f1) !important;
        color: white !important;
    }

    /* Mejorar subtítulos en el contenido principal */
    .stApp h2, .stApp h3 {
        color: #f1f5f9 !important;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.3);
    }

    /* Mejorar texto general */
    .stApp p, .stApp span {
        color: #e2e8f0;
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


# --- Cabecera Sidebar ---
data_filtros = cargar_opciones_filtros()

fecha_min = pd.to_datetime(data_filtros["fecha_min"])
fecha_max = pd.to_datetime(data_filtros["fecha_max"])
zonas_disponibles = data_filtros["zonas_disponibles"]
pass_min, pass_max = data_filtros["pass_min"], data_filtros["pass_max"]

st.sidebar.markdown('<p class="sidebar-subtitle">📊 Filtros para KPI</p>', unsafe_allow_html=True)
rango_fechas = st.sidebar.date_input("Rango de fechas:", (fecha_min, fecha_max))
hora_sel = st.sidebar.slider("Selecciona la hora del día:", 0, 23, 8)
p_min, p_max = st.sidebar.slider("Número de pasajeros:", pass_min, pass_max, (1, 4))

# --- Sección Mapas ---
st.sidebar.markdown("<hr>", unsafe_allow_html=True)
st.sidebar.markdown('<p class="sidebar-subtitle">🗺️ Filtros para Mapa de flujos</p>', unsafe_allow_html=True)
zona_sel = st.sidebar.selectbox("📍 Zona de Origen:", zonas_disponibles, index=0)
inicio, fin = rango_fechas

params = {
        "start_date": str(inicio),
        "end_date": str(fin),
        "hour": hora_sel,
        "pass_min": p_min,
        "pass_max": p_max
}

params1 = {
        "zona": zona_sel,
        "limite": 1000
}

try:
    response_datos = requests.get(API_URL_KPI, params=params)
    response_datos.raise_for_status()
    kpi_data = response_datos.json()
    if kpi_data and kpi_data["total_viajes"] > 0:
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        kpi1.metric("Total de Viajes", f"{kpi_data['total_viajes']:,}")
        kpi2.metric("Distancia Promedio (mi)", f"{kpi_data['promedio_distancia']:.2f}")
        kpi3.metric("Duración Promedio (min)", f"{kpi_data['duracion_promedio']:.1f}")
        kpi4.metric("Pasajeros Promedio", f"{kpi_data['pasajeros_promedio']:.1f}")
    else:
        st.warning("No hay datos para calcular los KPI.")
    
except requests.exceptions.RequestException as e:
    st.error(f"Error al cargar datos del EDA desde la API: {e}")

tab1, tab2, tab3 = st.tabs(["🔥 Mapa de Calor origen hora seleccionada","🔥 Mapa de Calor destino hora seleccionada", "🧭 Mapa de Flujos"])

# --- TAB 1: Mapa de Calor ---
with tab1:   
# ------------------------------------------------------
# VISUALIZACIÓN 1: MAPA DE CALOR (PICKUPS)
# ------------------------------------------------------
    st.subheader(f"🔥 Puntos de origen - Hora: {hora_sel}:00")
    try:
        response_datos = requests.get(API_URL_MAPA_CALOR, params=params)
        if response_datos.status_code == 200:
            data = response_datos.json()
            df_calor =  pd.DataFrame(data["data"])
        else:
            st.error(f"❌ Error {response_datos.status_code}: {response_datos.text}")
            df_calor = pd.DataFrame()
        
        if not df_calor.empty:
            view_state = pdk.ViewState(latitude=40.7128, longitude=-74.0060, zoom=11, pitch=40)

            heatmap_layer = pdk.Layer(
                "HeatmapLayer",
                data=df_calor,
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


    except requests.exceptions.RequestException as e:
        st.error(f"Error al cargar datos del EDA desde la API: {e}") 
        
with tab2:
    st.subheader(f"🔥 Puntos de destino - Hora: {hora_sel}:00")
    try:
        response_datos_drop = requests.get(API_URL_MAPA_CALOR_DROP, params=params)
        if response_datos_drop.status_code == 200:
            data = response_datos_drop.json()
            df_calor_destino =  pd.DataFrame(data["data"])
        else:
            st.error(f"❌ Error {response_datos_drop.status_code}: {response_datos_drop.text}")
            df_calor_destino = pd.DataFrame()
        
        if not df_calor_destino.empty:
            view_state = pdk.ViewState(latitude=40.7128, longitude=-74.0060, zoom=11, pitch=40)

            heatmap_layer = pdk.Layer(
                "HeatmapLayer",
                data=df_calor_destino,
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


    except requests.exceptions.RequestException as e:
        st.error(f"Error al cargar datos del EDA desde la API: {e}") 

with tab3:
    st.subheader(f"🧭 Flujos desde la zona seleccionada: {zona_sel}")
    try:
        response_datos_flow = requests.get(API_URL_MAPA_FLOW, params=params1)
        if response_datos_flow.status_code == 200:
            data = response_datos_flow.json()
            df_flow =  pd.DataFrame(data["data"])
        else:
            st.error(f"❌ Error {response_datos_flow.status_code}: {response_datos_flow.text}")
            df_flow = pd.DataFrame()
        
        if not df_flow.empty:
            arc_layer = pdk.Layer(
                "ArcLayer",
                data=df_flow,
                get_source_position=["lon_origen", "lat_origen"],
                get_target_position=["lon_destino", "lat_destino"],
                get_source_color=[0, 128, 255, 100],
                get_target_color=[255, 0, 128, 100],
                auto_highlight=True,
                width_scale=0.0005,
                width_min_pixels=1,
            )
            
            view_state = pdk.ViewState(latitude=40.7128, longitude=-74.0060, zoom=11, pitch=45)
            r2 = pdk.Deck(layers=[arc_layer], initial_view_state=view_state,
                        map_style="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json")
            st.pydeck_chart(r2)

    except requests.exceptions.RequestException as e:
        st.error(f"Error al cargar datos del EDA desde la API: {e}")