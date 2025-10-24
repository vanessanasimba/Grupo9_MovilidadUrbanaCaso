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
            'tpep_dropoff_datetime':'dropoff_datetime'
        }
    )
    return df_renombrado