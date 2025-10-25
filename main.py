import os
# Importar las funciones desde los scripts
from scripts.data_loader import cargar_datos
from scripts.data_cleaning import (limpiar_nombres_columnas, convertir_tipos_fechas,eliminar_coordenadas_invalidas)
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
       print("Iniciando el proceso de limpieza de datos...")
       # Limpiar los nombres de las columnas
       df_limpio = limpiar_nombres_columnas(df_movilidad)
       df_limpio = convertir_tipos_fechas(df_limpio)
       df_limpio = eliminar_coordenadas_invalidas(df_limpio)
    else:
        print("No se pudieron cargar los datos. Terminando el script.")


