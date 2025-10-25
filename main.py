import os
# Importar las funciones desde los scripts
from scripts.data_loader import cargar_datos
from scripts.data_cleaning import (limpiar_nombres_columnas, convertir_tipos_fechas,eliminar_coordenadas_invalidas,filtar_rango_geografico_valido)
from scripts.data_new_features import (crear_columna_dia_semana_pickup, crear_columna_hora_pickup, crear_columna_fecha_pickup, crear_columna_viaje_duracion, crear_columna_hora_pico)
from scripts.data_imputation import rellenar_valores_pasajeros_en_cero
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
        df_limpio = filtar_rango_geografico_valido(df_limpio)
        
        print("\n---LIMPIEZA DE DATOS TERMINADO---")
        
        # MÓDULO IMPUTACIÓN DE DATOS
        print("\n---INICIANDO IMPUTACIÓN DE DATOS---")
        df_procesado = rellenar_valores_pasajeros_en_cero(df_limpio)
        
        print("\n---IMPUTACIÓN DE DATOS TERMINADO---")
        
        print("\n---INICIANDO AGREGACIÓN NUEVAS COLUMNAS---")
        df_final = crear_columna_hora_pickup(df_procesado)
        df_final = crear_columna_dia_semana_pickup(df_procesado)    
        df_final = crear_columna_fecha_pickup(df_procesado)
        df_final = crear_columna_viaje_duracion(df_procesado)
        df_final = crear_columna_hora_pico(df_procesado)
            
        print("\n---AGREGACIÓN NUEVAS COLUMNAS TERMINADO---")
        
        # GUARDAR DATOS
        guardar_datos_limpios(df_final, OUTPUT_CLEANED_PATH)
            
        # AQUÍ TERMINÓ EL PIPELINE DE LIMPIEZA
        print("\n---PIPELINE TERMINADO---")
            
        print("\n---Información del DataFrame---")
        df_final.info(show_counts=True)
       
    else:
        print("No se pudieron cargar los datos. Terminando el script.")


