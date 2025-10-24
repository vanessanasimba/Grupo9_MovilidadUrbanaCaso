import os
# Importar las funciones desde los scripts
from scripts.data_loader import cargar_datos
from scripts.data_cleaning import limpiar_nombres_columnas
from scripts.data_saving import guardar_datos_limpios

#ruta absoluta de la carpeta donde esta el script (./)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
#construccion de la ruta absoluta de la carpeta data donde se encuentra el dataset (./data)
DATA_PATH = os.path.join(SCRIPT_DIR, "data", "yellow_tripdata_2015-01.csv")

# nueva ruta de salida para el archivo limpio
OUTPUT_CLEANED_PATH = os.path.join(SCRIPT_DIR, "data", "processed", "tripdata_cleaned.csv")

if __name__ == "__main__":
    print(f"Ejecutando el script desde: {os.path.abspath(__file__)}")
    
    # Cargar los datos
    df_movilidad = cargar_datos(DATA_PATH)
    
    if df_movilidad is not None:
        print("\n===Primeras 5 filas del DataFrame cargado ======")
        print(df_movilidad.head())
        
        print(f"\n=======Información del DataFrame antes de limpiar columnas ======")
        df_movilidad.info()
        
        # Limpiar los nombres de las columnas
        df_movilidad_limpio = limpiar_nombres_columnas(df_movilidad)
        
        print("\n===Primeras 5 filas del DataFrame con columnas limpias ======")
        print(df_movilidad_limpio.head())
        
        print(f"\n=======Información del DataFrame después de limpiar columnas ======")
        df_movilidad_limpio.info()
    else:
        print("No se pudieron cargar los datos. Terminando el script.")


