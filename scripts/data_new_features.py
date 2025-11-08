import pandas as pd
import numpy as np


def crear_columna_hora_pickup(df):
    """
    Crea una nueva columna 'pickup_hour' que contiene la hora del día en que se realizó la recogida.

    Args:
        df (pd.DataFrame): DataFrame con la columna 'pickup_datetime'.  
    """
    print("Creando la columna 'pickup_hour'...")
    
    df['pickup_hour'] = df['pickup_datetime'].dt.hour
    
    return df
def crear_columna_hora_dropof(df):
    """
    Crea una nueva columna 'pickup_hour' que contiene la hora del día en que se realizó la recogida.

    Args:
        df (pd.DataFrame): DataFrame con la columna 'dropoff_datetime'.  
    """
    print("Creando la columna 'dropoff_hour'...")
    
    df['dropoff_hour'] = df['dropoff_datetime'].dt.hour
    
    return df
def crear_columna_dia_semana_pickup(df):
    """
    Crea una nueva columna 'pickup_day_of_week' que contiene el día de la semana en que se realizó la recogida.

    Args:
        df (pd.DataFrame): DataFrame con la columna 'pickup_datetime'.  
    """
    print("Creando la columna 'pickup_day_of_week'...")
    
    df['pickup_day_of_week'] = df['pickup_datetime'].dt.day_name()
    
    return df

def crear_columna_fecha_pickup(df):
    """
    Crea una nueva columna 'pickup_date' que contiene solo la fecha (sin hora) de la recogida.

    Args:
        df (pd.DataFrame): DataFrame con la columna 'pickup_datetime'.  
    """
    print("Creando la columna 'pickup_date'...")
    
    if not pd.api.types.is_datetime64_any_dtype(df['pickup_datetime']):
        df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'], errors='coerce')

    # Crear la columna solo con la fecha (sin hora)
    df['pickup_date'] = df['pickup_datetime'].dt.normalize()

    # Asegurar tipo datetime64[ns]
    df['pickup_date'] = pd.to_datetime(df['pickup_date'], errors='coerce')

    print("Columna 'pickup_date' creada en formato datetime64[ns].")

    return df

def crear_columna_fecha_dropoff(df):
    """
    Crea una nueva columna 'dropoff_date' que contiene solo la fecha (sin hora) de la recogida.

    Args:
        df (pd.DataFrame): DataFrame con la columna 'dropoff_datetime'.  
    """
    print("Creando la columna 'dropoff_date'...")
    
    if not pd.api.types.is_datetime64_any_dtype(df['dropoff_datetime']):
        df['dropoff_datetime'] = pd.to_datetime(df['dropoff_datetime'], errors='coerce')

    # Crear la columna solo con la fecha (sin hora)
    df['dropoff_date'] = df['dropoff_datetime'].dt.normalize()

    # Asegurar tipo datetime64[ns]
    df['dropoff_date'] = pd.to_datetime(df['dropoff_date'], errors='coerce')

    print("Columna 'dropoff_date' creada en formato datetime64[ns].")

    return df

def crear_columna_viaje_duracion(df):
    """
    Crea una nueva columna 'trip_duration' que contiene la duración del viaje en minutos.

    Args:
        df (pd.DataFrame): DataFrame con las columnas 'pickup_datetime' y 'dropoff_datetime'.  
    """
    print("Creando la columna 'trip_duration'...")
    
    df['trip_duration'] = (df['dropoff_datetime'] - df['pickup_datetime']).dt.total_seconds() / 60.0
    
    return df
def crear_columna_hora_pico(df):
    """
    Crea una nueva columna 'is_peak_hour' que indica si la recogida se realizó en hora pico (7-9 AM o 4-6 PM).

    Args:
        df (pd.DataFrame): DataFrame con la columna 'pickup_datetime'.  
    """
    print("Creando la columna 'is_peak_hour'...")
    
    df['is_peak_hour'] =df['pickup_hour'].between(7,9) | df['pickup_hour'].between(17,19)
    
    return df

def crear_zona_viaje_pickup(df):
    """
    Asigna una zona aproximada (pickup_zone) según las coordenadas.
    Zonas de ejemplo: JFK_Airport, Midtown, Downtown, Other.
    """
    print("Asignando zonas pickup de viaje según coordenadas...")

    def obtener_zona(lat, lon):
        if 40.63 <= lat <= 40.65 and -73.79 <= lon <= -73.76:
            return "JFK Airport"
        elif 40.76 <= lat <= 40.78 and -73.89 <= lon <= -73.86:
            return "LaGuardia Airport"
        elif 40.70 <= lat <= 40.72 and -74.02 <= lon <= -74.00:
            return "Downtown Manhattan"
        elif 40.755 <= lat <= 40.76 and -73.99 <= lon <= -73.98:
            return "Times Square"
        elif 40.750 <= lat <= 40.753 and -73.979 <= lon <= -73.974:
            return "Grand Central Terminal"
        elif 40.748 <= lat <= 40.752 and -73.996 <= lon <= -73.990:
            return "Penn Station"
        else:
            return "Otra zona"
    
    df["pickup_zone"] = df.apply(lambda row: obtener_zona(row["pickup_latitude"], row["pickup_longitude"]), axis=1)

    return df

def crear_zona_viaje_dropoff(df):
    """
    Asigna una zona aproximada (dropoff_zone) según las coordenadas.
    Usa operaciones vectorizadas para evitar problemas de memoria con .apply().
    """
    print("Asignando zonas dropoff de viaje según coordenadas (modo optimizado)...")

    # Inicializar con valor por defecto
    df["dropoff_zone"] = "Otra zona"

    # Crear condiciones vectorizadas
    condiciones = [
        (df["dropoff_latitude"].between(40.63, 40.65)) & (df["dropoff_longitude"].between(-73.79, -73.76)),
        (df["dropoff_latitude"].between(40.76, 40.78)) & (df["dropoff_longitude"].between(-73.89, -73.86)),
        (df["dropoff_latitude"].between(40.70, 40.72)) & (df["dropoff_longitude"].between(-74.02, -74.00)),
        (df["dropoff_latitude"].between(40.755, 40.76)) & (df["dropoff_longitude"].between(-73.99, -73.98)),
        (df["dropoff_latitude"].between(40.750, 40.753)) & (df["dropoff_longitude"].between(-73.979, -73.974)),
        (df["dropoff_latitude"].between(40.748, 40.752)) & (df["dropoff_longitude"].between(-73.996, -73.990))
    ]

    valores = [
        "JFK Airport",
        "LaGuardia Airport",
        "Downtown Manhattan",
        "Times Square",
        "Grand Central Terminal",
        "Penn Station"
    ]

    # Asignar con np.select
    df["dropoff_zone"] = np.select(condiciones, valores, default="Otra zona")

    return df