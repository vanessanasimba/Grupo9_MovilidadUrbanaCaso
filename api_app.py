from fastapi import FastAPI, HTTPException,Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import os

# las rutas para cargar el modelo y el encoder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "tripdata_cleaned.csv")

def load_data(path):
    data = pd.read_csv(path)
    data['pickup_date'] = pd.to_datetime(data['pickup_date'], errors='coerce')
    data['dropoff_date'] = pd.to_datetime(data['dropoff_date'], errors='coerce')
    return data 

df = load_data(DATA_PATH)


# ==================================================
# CONFIGURACIÓN INICIAL DE LA API
# ==================================================
app = FastAPI(
    title="NYC Taxi Geospatial API",
    description="API de viajes de taxi en NYC. generar difernetes filtro por fehc , hora  y zona ",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TripFilter(BaseModel):
    start_date: str
    end_date: str
    hour: int
    pass_min: int
    pass_max: int
    zone: str
    
@app.get("/filters/options")
def get_filter_options():
    """
    Devuelve las opciones disponibles para construir los filtros del dashboard:
    - Rango de fechas (mínima y máxima)
    - Rango de horas (0 a 23)
    - Rango de pasajeros (mínimo y máximo)
    - Lista de zonas disponibles
    """
    if df.empty:
        raise HTTPException(status_code=500, detail="El dataset no está disponible.")

    try:
        fecha_min = df["pickup_date"].min()
        fecha_max = df["pickup_date"].max()
        pass_min = int(df["passengers"].min())
        pass_max = int(df["passengers"].max())

        zonas = ["Todas"]
        if "pickup_zone" in df.columns:
            zonas += sorted(df["pickup_zone"].dropna().unique().tolist())

        return {
            "fecha_min": str(fecha_min.date()),
            "fecha_max": str(fecha_max.date()),
            "hora_min": 0,
            "hora_max": 23,
            "pass_min": pass_min,
            "pass_max": pass_max,
            "zonas_disponibles": zonas
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener filtros: {str(e)}")


@app.get("/options/kpi")
def obtener_kpi(
    start_date: str = Query(..., description="Fecha inicial (YYYY-MM-DD)"),
    end_date: str = Query(..., description="Fecha final (YYYY-MM-DD)"),
    hour: int = Query(..., description="Hora del día (0-23)"),
    pass_min: int = Query(1, description="Cantidad mínima de pasajeros"),
    pass_max: int = Query(6, description="Cantidad máxima de pasajeros")
):
    """
    Calcula los KPI (Indicadores Clave de Rendimiento) en base a los filtros recibidos:
    - Rango de fechas
    - Hora específica
    - Rango de pasajeros
    Retorna:
        - total_viajes
        - promedio_distancia
        - duracion_promedio
        - pasajeros_promedio
    """
    if df.empty:
        raise HTTPException(status_code=500, detail="El dataset no está disponible.")

    try:
        # Convertir fechas a datetime
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        # Filtrar el dataset
        df_filtrado = df[
            (df["pickup_date"].between(start_date, end_date)) &
            (df["pickup_hour"] == hour) &
            (df["passengers"].between(pass_min, pass_max))
        ]

        # Validar si hay datos
        if df_filtrado.empty:
            return {
                "message": "⚠️ No hay datos para calcular KPI con los filtros seleccionados.",
                "total_viajes": 0,
                "promedio_distancia": 0,
                "duracion_promedio": 0,
                "pasajeros_promedio": 0
            }

        # Cálculo de KPIs
        total_viajes = int(len(df_filtrado))
        promedio_distancia = float(df_filtrado["distance"].mean())
        duracion_promedio = float(df_filtrado["trip_duration"].mean())
        pasajeros_promedio = float(df_filtrado["passengers"].mean())

        return {
            "message": f"✅ {total_viajes:,} viajes encontrados.",
            "total_viajes": total_viajes,
            "promedio_distancia": round(promedio_distancia, 2),
            "duracion_promedio": round(duracion_promedio, 1),
            "pasajeros_promedio": round(pasajeros_promedio, 1)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al calcular KPI: {str(e)}")
    
@app.get("/heatmap/pickup")
def obtener_datos_mapa_calor(
    start_date: str = Query(..., description="Fecha inicial (YYYY-MM-DD)"),
    end_date: str = Query(..., description="Fecha final (YYYY-MM-DD)"),
    hour: int = Query(None, description="Hora específica del día (0–23)")
):
    """
    Devuelve una lista de puntos (lat, lon) para construir el mapa de calor
    según el rango de fechas y la hora seleccionada.
    """
    if df.empty:
        raise HTTPException(status_code=500, detail="El dataset no está disponible.")

    try:
        # Convertir fechas
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        # Filtrar por fecha
        df_filtrado = df[
            (df["pickup_date"].between(start_date, end_date))
        ]

        # Filtrar por hora (si se especifica)
        if hour is not None:
            df_filtrado = df_filtrado[df_filtrado["pickup_hour"] == hour]

        # Verificar columnas de coordenadas
        if "pickup_latitude" not in df_filtrado.columns or "pickup_longitude" not in df_filtrado.columns:
            raise HTTPException(status_code=400, detail="El dataset no contiene columnas de coordenadas válidas.")

        # Reducir tamaño del dataset (para rendimiento)
        MAX_PUNTOS = 20000
        if len(df_filtrado) > MAX_PUNTOS:
            df_mapa = df_filtrado.sample(MAX_PUNTOS, random_state=42)
        else:
            df_mapa = df_filtrado.copy()

        # Renombrar columnas para consistencia con PyDeck
        df_mapa = df_mapa.rename(columns={
            "pickup_latitude": "lat",
            "pickup_longitude": "lon"
        })

        # Exportar solo columnas necesarias
        data = df_mapa[["lat", "lon", "pickup_hour", "pickup_date"]].to_dict(orient="records")

        return {
            "message": f"✅ {len(data):,} puntos generados para el mapa de calor.",
            "count": len(data),
            "data": data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar datos del mapa de calor: {str(e)}")
    

@app.get("/heatmap/dropoff")
def obtener_datos_mapa_calor_drop(
    start_date: str = Query(..., description="Fecha inicial (YYYY-MM-DD)"),
    end_date: str = Query(..., description="Fecha final (YYYY-MM-DD)"),
    hour: int = Query(None, description="Hora específica del día (0–23)")
):
    """
    Devuelve una lista de puntos (lat, lon) para construir el mapa de calor
    según el rango de fechas y la hora seleccionada.
    """
    if df.empty:
        raise HTTPException(status_code=500, detail="El dataset no está disponible.")

    try:
        # Convertir fechas
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        # Filtrar por fecha
        df_filtrado = df[
            (df["dropoff_date"].between(start_date, end_date))
        ]

        # Filtrar por hora (si se especifica)
        if hour is not None:
            df_filtrado = df_filtrado[df_filtrado["dropoff_hour"] == hour]

        # Verificar columnas de coordenadas
        if "dropoff_latitude" not in df_filtrado.columns or "dropoff_longitude" not in df_filtrado.columns:
            raise HTTPException(status_code=400, detail="El dataset no contiene columnas de coordenadas válidas.")

        # Reducir tamaño del dataset (para rendimiento)
        MAX_PUNTOS = 20000
        if len(df_filtrado) > MAX_PUNTOS:
            df_mapa = df_filtrado.sample(MAX_PUNTOS, random_state=42)
        else:
            df_mapa = df_filtrado.copy()

        # Renombrar columnas para consistencia con PyDeck
        df_mapa = df_mapa.rename(columns={
            "dropoff_latitude": "lat",
            "dropoff_longitude": "lon"
        })

        # Exportar solo columnas necesarias
        data = df_mapa[["lat", "lon", "dropoff_hour", "dropoff_date"]].to_dict(orient="records")

        return {
            "message": f"✅ {len(data):,} puntos generados para el mapa de calor.",
            "count": len(data),
            "data": data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar datos del mapa de calor: {str(e)}")
    
@app.get("/flow")
def obtener_flujos_por_zona(
    zona: str = Query(..., description="Nombre de la zona de origen"),
    limite: int = Query(1000, ge=100, le=5000, description="Número máximo de flujos a devolver (por defecto 1000)")
):
    """
    Devuelve los flujos de viajes (origen-destino) desde una zona específica.
    Se usa para construir el mapa de flujos con PyDeck.
    """

    try:
        if df.empty:
            raise HTTPException(status_code=500, detail="El dataset no está disponible o no fue cargado correctamente.")

        # --- Filtrar por zona seleccionada ---
        df_zona = df[df["pickup_zone"] == zona]

        if df_zona.empty:
            raise HTTPException(status_code=404, detail=f"No se encontraron viajes desde la zona '{zona}'.")

        # --- Limitar el número de puntos ---
        df_zona = df_zona.sample(min(len(df_zona), limite), random_state=42)

        # --- Seleccionar solo las columnas necesarias ---
        df_flujos = df_zona[[
            "pickup_latitude", "pickup_longitude",
            "dropoff_latitude", "dropoff_longitude"
        ]].rename(columns={
            "pickup_latitude": "lat_origen",
            "pickup_longitude": "lon_origen",
            "dropoff_latitude": "lat_destino",
            "dropoff_longitude": "lon_destino"
        })

        # --- Convertir a lista JSON serializable ---
        data = df_flujos.to_dict(orient="records")

        return {
            "message": f"✅ {len(data):,} flujos obtenidos desde la zona '{zona}'.",
            "count": len(data),
            "zone": zona,
            "data": data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener flujos: {str(e)}")