import pandas as pd
import os

def guardar_datos_limpios(df, path):
    """
    Guarda el DataFrame limpio en un archivo CSV.

    Args:
        df (pd.DataFrame): DataFrame limpio a guardar.
        path (str): Ruta donde se guardará el archivo CSV.
    """
    print(f"Guardando el DataFrame limpio en: {path}")
    try:
        print("Se esta creando el archivo limpio...  ")
        
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        df.to_csv(path, index=False)
        print("Archivo guardado exitosamente.")
        print(f"Ruta del archivo guardado: {os.path.abspath(path)}")
        return True
    except Exception as e:
        print(f"Ocurrió un error al guardar el archivo: {e}")
        return
  