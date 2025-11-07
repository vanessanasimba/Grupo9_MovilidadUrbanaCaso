import pandas as pd

def crear_columna_hora_pickup(df):
    """
    Crea una nueva columna 'pickup_hour' que contiene la hora del día en que se realizó la recogida.

    Args:
        df (pd.DataFrame): DataFrame con la columna 'pickup_datetime'.  
    """
    print("Creando la columna 'pickup_hour'...")
    
    df['pickup_hour'] = df['pickup_datetime'].dt.hour
    
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
    print("Asignando zonas de viaje según coordenadas...")

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
    Asigna una zona aproximada (pickup_zone) según las coordenadas.
    Zonas de ejemplo: JFK_Airport, Midtown, Downtown, Other.
    """
    print("Asignando zonas de viaje según coordenadas...")

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

    df["dropoff_zone"] = df.apply(lambda row: obtener_zona(row["dropoff_latitude"], row["dropoff_longitude"]), axis=1)
    return df