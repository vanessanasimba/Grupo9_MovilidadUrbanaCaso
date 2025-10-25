import pandas as pd
import os

# ruta absoluta de la carpeta donde esta el script (../scripts)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# ruta absoluta de la carpeta data donde se encuntra el dataset (../data)
DATA_PATH = os.path.join(SCRIPT_DIR, "..", "data","yellow_tripdata_2015-01.csv")

# creacion de la funcion para cargar los datos
def cargar_datos(path):
    """
    Carga el dataset de movilidad urbana desde un archivo CSV.

    Args:
        path (str): Ruta al archivo CSV del dataset.

    Returns:
        pd.DataFrame: DataFrame de pandas que contiene los datos cargados.
    """
    print(f"Cargando datos desde: {path}")
    
    try:
        df = df = pd.read_csv(path, sep=',', encoding='utf-8', low_memory=False)
        print("Datos cargados exitosamente.")
        return df
    except FileNotFoundError:
        print(f"El archivo no se encontró en la ruta especificada: {path}")
        print(f"segurate de tener el archivo en la carpeta 'data'.")
        return None
    except pd.errors.EmptyDataError:
        print("El archivo está vacío.")
        return None
    except pd.errors.ParserError:
        print("Error al parsear el archivo CSV.")
        return None
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        return None