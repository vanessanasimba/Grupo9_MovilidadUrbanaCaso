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