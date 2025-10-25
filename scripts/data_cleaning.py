import pandas as pd

def limpiar_nombres_columnas(df):
    """
    Limpia los nombres de las columnas del DataFrame eliminando espacios en blanco
    y convirtiéndolos a minúsculas.

    Args:
        df (pd.DataFrame): DataFrame cuyas columnas se van a limpiar.

    Returns:
        pd.DataFrame: DataFrame con los nombres de las columnas limpiados.
    """
    print("Limpiando los nombres de las columnas...")
    
    df_renombrado  = df.rename(
        columns={
            'tpep_pickup_datetime':'pickup_datetime',
            'tpep_dropoff_datetime':'dropoff_datetime',
            'passenger_count': 'passengers',
            'trip_distance': 'distance'
        }
    )
    df_renombrado.columns = df_renombrado.columns.str.strip().str.lower();
    
    return df_renombrado

def convertir_tipos_fechas(df):
    """
    Convierte las columnas de fechas a tipo datetime.

    Args:
        df (pd.DataFrame): DataFrame con las columnas de fechas a convertir.

    Returns:
        pd.DataFrame: DataFrame con las columnas de fechas convertidas a datetime.
    """
    print("Convirtiendo columnas de fechas a tipo datetime...")
    
    df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'], errors='coerce')
    df['dropoff_datetime'] = pd.to_datetime(df['dropoff_datetime'], errors='coerce')
    
    return df

def eliminar_coordenadas_invalidas(df):
    """
    Elimina filas con coordenadas inválidas (0,0) en las columnas de latitud y longitud.

    Args:
        df (pd.DataFrame): DataFrame del cual se eliminarán las filas con coordenadas inválidas.

    Returns:
        pd.DataFrame: DataFrame sin las filas con coordenadas inválidas.
    """
    print("Eliminando filas con coordenadas inválidas...")
    
    df = df[
        (df['pickup_longitude'] != 0) & 
        (df['pickup_latitude'] != 0) &
        (df['dropoff_longitude'] != 0) &
        (df['dropoff_latitude'] != 0)
    ]
        
    return df

