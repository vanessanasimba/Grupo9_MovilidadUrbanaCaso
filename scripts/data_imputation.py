import pandas as pd

def rellenar_valores_pasajeros_en_cero(df):
    """
    Rellena los valores de la columna 'passengers' que son cero con la mediana de la columna.

    Args:
        df (pd.DataFrame): DataFrame con la columna 'passengers'.

    Returns:
        pd.DataFrame: DataFrame con los valores de 'passengers' rellenados.
    """
    print("Rellenando valores de 'passengers' que son cero con la mediana...")
    
    mediana_pasajeros = df['passengers'].median()
    df['passengers'] = df['passengers'].replace(0, mediana_pasajeros)
    
    return df
def eliminar_coordenadas_null(df):
    
    print("eliminar valores en na de lad coordenadas")
    df = df.dropna(subset=['pickup_latitude', 'pickup_longitude'])
    df = df.dropna(subset=['dropoff_longitude', 'dropoff_latitude'])
    
    print(f"Registros después de limpieza: {len(df):,}")
    return df
